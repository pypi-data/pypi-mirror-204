from __future__ import annotations
from abc import abstractmethod
from collections import Sequence
from dataclasses import _MISSING_TYPE, MISSING, dataclass, field
import functools
from pathlib import Path
from loguru import logger
from ned.candidate_ranking.helpers.dataset import MyDatasetDict
import numpy as np
from typing import List, Literal, Mapping, Optional, Protocol, Union
from sm.misc.funcs import get_incremental_path, get_latest_path, get_latest_version
import torch
from torch.utils.data import DataLoader
from torch.utils.data.dataset import Dataset
from tqdm import tqdm
from transformers.training_args import IntervalStrategy, TrainingArguments


class SmoothingMetric:
    def __init__(self, window_size: int = 7):
        self.lst: List[float] = [0] * window_size
        self.window_size = window_size
        self.counter = 0

    def __iadd__(self, x: float):
        self.lst[self.counter % self.window_size] = x
        self.counter += 1
        return self

    def mean(self):
        return np.mean(self.lst[: self.counter])


@dataclass
class CkptHelper:
    """Helper class to load, save, and resume training from a checkpoint"""

    # the root directory
    root: Path
    # the step to resume the training from, 0 means start from scratch, -1 means resume from the latest checkpoint
    fromstep: int
    # the file to resume the training from, can be relative to root. If provided, fromstep is ignored
    fromfile: Optional[str]

    @functools.cached_property
    def ckpt_dir(self):
        """Return a directory to save checkpoints"""
        traindir_pattern = self.root / "training_v"
        dir = get_latest_path(traindir_pattern)
        if (
            dir is not None
            and (dir / "checkpoints").exists()
            and not any(True for _ in (dir / "checkpoints").iterdir())
        ):
            # reuse the previous directory if it is empty
            ckpt_dir = dir / "checkpoints"
        else:
            ckpt_dir = (
                get_incremental_path(traindir_pattern, delimiter_char="")
                / "checkpoints"
            )
            ckpt_dir.mkdir(parents=True, exist_ok=True)
        return ckpt_dir

    @functools.cached_property
    def restore_ckpt_file(self):
        """Return a directory containing previous checkpoints, none means no previous checkpoints"""
        if self.fromfile is None and self.fromstep == 0:
            return None

        if self.fromfile is None:
            version = get_latest_version(self.root / "training_v*")
            # set it here to avoid the typing warning but it will be overwritten later
            ckpt_dir = self.root / f"training_v00" / "checkpoints"
            while version > 0:
                ckpt_dir = self.root / f"training_v{version:02d}" / "checkpoints"
                if ckpt_dir.exists() and any(True for _ in ckpt_dir.iterdir()):
                    # there are some checkpoints
                    break
                version -= 1
            if version == 0:
                return None

            if self.fromstep == -1:
                path = get_latest_path(ckpt_dir / f"step_.pt")
                if path is None:
                    # we can still have the case where the previous training was interrupted and no checkpoint was saved yet
                    return None
            else:
                path = ckpt_dir / f"step_{self.fromstep}.pt"
                assert path.exists(), f"Checkpoint {path} does not exist"

            return path

        # if fromfile is absolute, Path will handle that for us and discard the root.
        return (self.root / self.fromfile).absolute()

    def get_restore_training_dir(self):
        """Return the directory containing the previous checkpoints"""
        if self.restore_ckpt_file is None:
            return None
        traindir = self.restore_ckpt_file.parent.parent
        assert (
            traindir.name.startswith("training_v")
            and (traindir / "checkpoints").exists()
        )
        return traindir

    def get_training_dir(self):
        return self.ckpt_dir.parent

    def is_resuming(self):
        return self.restore_ckpt_file is not None

    def resume_if_needed(self, model, optimizer, device=None) -> int:
        if self.restore_ckpt_file is None:
            return 0

        # https://pytorch.org/tutorials/recipes/recipes/saving_and_loading_a_general_checkpoint.html
        ckpt = torch.load(self.restore_ckpt_file, map_location=device)
        model.load_state_dict(ckpt["model"])
        if optimizer is not None:
            optimizer.load_state_dict(ckpt["optimizer"])

        logger.info(
            "Resuming the training from step {} from checkpoint at {}",
            ckpt["step"],
            self.restore_ckpt_file,
        )
        return ckpt["step"]

    def skip_to_step(
        self,
        dl,
        step: int,
        progress_bar: ProgressBarProtocol,
        num_epoch_steps: Optional[int] = None,
    ):
        """Skip the dataloader to the given step.
        Note that step starts counting from 1.
        If step is 0, then it does nothing and works as expected"""
        prev_desc = progress_bar.desc
        progress_bar.set_description(f"Skipping to step {step}")
        if num_epoch_steps is None or num_epoch_steps > 1:
            # only repeat the dataloader if it does not contain only a single step
            for _ in range(step):
                next(dl)
                progress_bar.update(1)
        else:
            progress_bar.update(step)
        progress_bar.set_description(prev_desc)
        return dl

    def save(self, step, model, optimizer):
        savefile = self.ckpt_dir / f"step_{step}.pt"
        torch.save(
            {
                "step": step,
                "model": model.state_dict(),
                "optimizer": optimizer.state_dict(),
            },
            savefile,
        )
        return savefile


@dataclass
class ModifiedTrainingArguments(TrainingArguments):
    train_dataset: str = field(
        default="",
        metadata={
            "help": "The dataset to use for training. Following the ream.dataset_helper.DatasetQuery format"
        },
    )
    eval_datasets: list[str] = field(
        default_factory=list,
        metadata={
            "help": "The datasets used for evaluation. Following the ream.dataset_helper.DatasetQuery format"
        },
    )
    output_dir: str = ""
    # so that they do not generate this field automatically
    # making it difficult to cache
    logging_dir: str = "logs"
    train_eval_strategy: IntervalStrategy = IntervalStrategy.EPOCH
    train_eval_steps: int = field(
        default=2,
        metadata={"help": "Run an evaluation on the train set every X epochs."},
    )

    def get_steps(self, num_epoch_steps: int):
        if self.evaluation_strategy == "epoch":
            assert self.eval_steps is not None
            eval_steps = self.eval_steps * num_epoch_steps
        elif self.evaluation_strategy == "steps":
            assert self.eval_steps is not None
            eval_steps = self.eval_steps
        else:
            eval_steps = None

        if self.train_eval_strategy == "epoch":
            train_eval_steps = self.train_eval_steps * num_epoch_steps
        elif self.train_eval_strategy == "steps":
            train_eval_steps = self.train_eval_steps
        else:
            train_eval_steps = None

        if self.save_strategy == "epoch":
            save_steps = self.save_steps * num_epoch_steps
        elif self.save_strategy == "steps":
            save_steps = self.save_steps
        else:
            save_steps = None

        return eval_steps, train_eval_steps, save_steps


def loop_dl(dl: DataLoader, n: int):
    counter = 0
    while True:
        for batch in dl:
            yield batch
            counter += 1
            if counter >= n:
                break
        if counter >= n:
            break


def describe(msg, kwargs):
    logger.info("{}", msg)
    for k, v in kwargs.items():
        logger.info("\t{}: {}", k, v)


def calculate_balanced_class_weights(train_dl: DataLoader):
    pos, neg, total = 0, 0, 0
    for batch in train_dl:
        label = batch["label"]
        total += label.numel()
        bpos = (label == 1).sum()
        pos += bpos
        neg += label.numel() - bpos

    return torch.FloatTensor([1 - neg / total, 1 - pos / total])


def get_data_loader(dataset: Dataset, name, batch_size: int, shuffle: bool):
    logger.info(
        "{} dataset: #examples {} - batch size {}", name, len(dataset), batch_size
    )

    return DataLoader(
        dataset,
        batch_size=batch_size,
        shuffle=shuffle,
        collate_fn=dataset.collate_fn,
    )


class SklearnClassifier:
    TRAIN_ARGS: Sequence[str]
    EVAL_ARGS: Sequence[str]
    # mapping from metric class name to metric auxiliary args (no predictions) to dataset args
    METRIC_REF_ARGS: Mapping[str, Mapping[str, str]]

    @abstractmethod
    def fit(self, **kwargs):
        pass

    @abstractmethod
    def predict(self, **kwargs):
        pass

    @abstractmethod
    def predict_proba(self, **kwargs):
        pass

    @abstractmethod
    def state_dict(self) -> dict:
        pass

    @abstractmethod
    def load_state_dict(self, state_dict: dict):
        pass


class ProgressBarProtocol(Protocol):
    desc: str

    def update(self, n: int) -> Optional[bool]:
        ...

    def set_description(self, desc: str):
        ...
