from __future__ import annotations

from collections import defaultdict
from contextlib import contextmanager
from os import cpu_count
from pathlib import Path
from typing import TYPE_CHECKING, Literal, Optional, Tuple

import evaluate
from ned.candidate_ranking.cr_dataset import NoCacheCRDataset
from ned.data_models.pymodels import Entity
import orjson
import torch
from torch.utils.data import DataLoader
import wandb.util
from accelerate import Accelerator
from accelerate.utils import set_seed
from loguru import logger
from tqdm.auto import tqdm
import serde.json
import wandb
from ned.candidate_ranking.columnwise_model import ColumnwiseModel
from ned.candidate_ranking.cr_method import CandidateRankingMethod
from ned.candidate_ranking.helpers import SmoothingMetric, describe, loop_dl
from ned.candidate_ranking.helpers.training_helper import (
    CkptHelper,
    ModifiedTrainingArguments,
    calculate_balanced_class_weights,
    get_data_loader,
)
from ned.candidate_ranking.pairwise_model import PairwiseModel
from sm.prelude import M

if TYPE_CHECKING:
    from ned.actors.candidate_ranking import CanRankActor


def cr_training(
    actor: CanRankActor, ckpt_helper: CkptHelper, eval_ds_mode: Literal["train", "test"]
) -> Tuple[CandidateRankingMethod, Path]:
    """
    Args:
        actor: can rank actor from which we get all necessary information
        ckpt_helper: helper to deal with saving and resuming training
        eval_ds_mode: whether to create dev/test datasets for_training mode.
    """

    # --------------------------------------------------------------------------------
    # prepare parameters and configurations
    logger.info("Saving checkpoints to {}", ckpt_helper.ckpt_dir)

    params = actor.params
    trainargs = params.training

    assert trainargs is not None
    assert trainargs.logging_strategy == "steps"

    if params.method == "columnwise":
        trainargs.per_device_train_batch_size = 1
        trainargs.per_device_eval_batch_size = 1

    # --------------------------------------------------------------------------------
    # prepare datasets
    accelerator = Accelerator()
    set_seed(trainargs.seed)
    model = actor.get_method()

    with accelerator.main_process_first():
        train_ds = actor.canrank_dataset.run_dataset(
            model,
            trainargs.train_dataset,
            for_training=True,
        ).into_single_value()

        eval_dsdict = {}
        for eval_dsname in trainargs.eval_datasets:
            dsdict = actor.canrank_dataset.run_dataset(
                model,
                eval_dsname,
                for_training=eval_ds_mode == "train",
            )
            for name, ds in dsdict.items():
                assert name not in eval_dsdict
                eval_dsdict[name] = ds

        assert "train" in eval_dsdict, eval_dsdict.keys()

    train_dl = get_data_loader(
        train_ds, "train", trainargs.per_device_train_batch_size, shuffle=True
    )
    eval_dls = {
        split: get_data_loader(
            eval_ds, split, trainargs.per_device_eval_batch_size, shuffle=False
        )
        for split, eval_ds in eval_dsdict.items()
    }

    # --------------------------------------------------------------------------------
    # prepare the model

    # calculate the class weights
    if hasattr(model, "class_weights"):
        if params.method == "pairwise":
            assert params.pairwise is not None
            assert isinstance(model, PairwiseModel)
            cfg_class_weight = params.pairwise.class_weight
        elif params.method == "columnwise":
            assert params.columnwise is not None
            assert isinstance(model, ColumnwiseModel)
            cfg_class_weight = params.columnwise.class_weight
        elif params.method == "crv3":
            cfg_class_weight = 0
        else:
            raise NotImplementedError()

        if cfg_class_weight == 0:
            model.class_weights = calculate_balanced_class_weights(train_dl)
        else:
            assert len(model.class_weights) == 2
            total = 1 + cfg_class_weight
            model.class_weights[0] = 1 / total
            model.class_weights[1] = 1 - 1 / total

        logger.info(
            "Update the class weights of the model to be: {}", model.class_weights
        )

    use_wandb = "wandb" in M.assert_not_null(trainargs.report_to)
    with with_wandb(
        ckpt_helper,
        {"method": params.method, "dataset": trainargs.train_dataset},
        enable=use_wandb,
    ):
        return train_loop(
            model,
            ckpt_helper,
            accelerator,
            train_dl,
            eval_dls,
            trainargs,
            use_wandb,
        )


def train_loop(
    model: CandidateRankingMethod,
    ckpt_helper: CkptHelper,
    accelerator: Accelerator,
    train_dl: DataLoader,
    eval_dls: dict[str, DataLoader],
    trainargs: ModifiedTrainingArguments,
    use_wandb: bool = False,
):
    model_argnames = model.EXPECTED_ARGS
    model_evalargnames = model.EXPECTED_EVAL_ARGS

    metrics = [evaluate.load(str(Path(__file__).parent / "metrics/ned_metric.py"))]
    optimizer = torch.optim.AdamW(
        params=model.parameters(),
        lr=trainargs.learning_rate,
        weight_decay=trainargs.weight_decay,
    )

    start_step = ckpt_helper.resume_if_needed(model, optimizer)
    model, optimizer, train_dataloader = accelerator.prepare(model, optimizer, train_dl)

    tmp = list(eval_dls.items())
    eval_dataloaders = {
        key: dataloader
        for key, dataloader in zip(
            [x[0] for x in tmp], accelerator.prepare(*[x[1] for x in tmp])
        )
    }

    num_epoch_steps = len(train_dl)
    num_train_steps = num_epoch_steps * int(trainargs.num_train_epochs)
    num_eval_steps = sum(len(dl) for dl in eval_dataloaders.values())

    dev_check_interval, train_check_interval, ckpt_interval = trainargs.get_steps(
        num_epoch_steps
    )

    describe(
        "Config:",
        dict(
            device=accelerator.device,
            num_epoch_steps=num_epoch_steps,
            num_train_steps=num_train_steps,
            dev_check_interval=dev_check_interval,
            train_check_interval=train_check_interval,
            ckpt_interval=ckpt_interval,
            learning_rate=trainargs.learning_rate,
        ),
    )

    # lr_scheduler = get_linear_schedule_with_warmup(
    #     optimizer=optimizer,
    #     num_warmup_steps=100,
    #     num_training_steps=num_train_steps,
    # )

    progress_bar = tqdm(range(int(num_train_steps)))

    model.train()
    step_loss = SmoothingMetric()
    epoch_loss = 0
    postfix = {}
    step = 1
    latest_ckpt_file = None

    for step, batch in enumerate(
        ckpt_helper.skip_to_step(
            loop_dl(train_dataloader, num_train_steps),
            start_step,
            progress_bar,
            num_epoch_steps,
        ),
        start=start_step + 1,
    ):
        try:
            with accelerator.accumulate(model):
                outputs = model(**{name: batch[name] for name in model_argnames})
                loss = outputs.loss

                step_loss += loss.item()
                epoch_loss += loss.item()

                accelerator.backward(loss)
                optimizer.step()
                # lr_scheduler.step()
                optimizer.zero_grad()

            progress_bar.update(1)
            postfix["loss"] = step_loss.mean()

            if step % num_epoch_steps == 0:
                postfix["epoch_loss"] = epoch_loss / num_epoch_steps
                epoch_loss = 0

            progress_bar.set_postfix(postfix)
            if use_wandb and step % trainargs.logging_steps == 0:
                wandb.log(dict(step=step, loss=postfix["loss"]), step=step)

            if (dev_check_interval is not None and step % dev_check_interval == 0) or (
                train_check_interval is not None and step % train_check_interval == 0
            ):
                model.eval()
                # eval_outputs = defaultdict(lambda: defaultdict(list))
                eval_sets = []

                if (
                    train_check_interval is not None
                    and step % train_check_interval == 0
                ):
                    eval_sets.append(("train", eval_dataloaders["train"]))
                if dev_check_interval is not None and step % dev_check_interval == 0:
                    for k, dataloader in eval_dataloaders.items():
                        if k != "train":
                            eval_sets.append((k, dataloader))

                for stg, dl in eval_sets:
                    for batch in dl:
                        with torch.no_grad():
                            outputs = model(
                                **{name: batch[name] for name in model_evalargnames}
                            )

                        # for pairwise model, probs has shape B x 1, labels has shape B x 1
                        # for column-wise model, probs has shape I x J, (because B is 1), labels has shape B x I x J
                        if batch["label"].dim() == 3:
                            # column-wise model
                            # assert (
                            #     batch["mask"].sum() == batch["mask"].numel()
                            # ), "now you need to implement masking"
                            assert batch["label"].shape[0] == 1
                            mask = batch["mask"].reshape(-1)
                            predictions = outputs.probs.reshape(-1)[mask]
                            labels = batch["label"][0].reshape(-1)[mask]
                            cells = batch["cell"][0].reshape(-1)[mask]
                        else:
                            predictions = outputs.probs
                            labels = batch["label"]
                            cells = batch["cell"]
                        # TODO: handle the mask.

                        # preds = [l.item() for l in accelerator.gather(predictions)]
                        # refs = [l.item() for l in accelerator.gather(labels)]
                        # cells = [l.item() for l in accelerator.gather(cells)]
                        preds = accelerator.gather_for_metrics(predictions)
                        refs = accelerator.gather_for_metrics(labels)
                        cells = accelerator.gather_for_metrics(cells)

                        for metric in metrics:
                            metric.add_batch(
                                predictions=preds, references=refs, cells=cells
                            )

                        # eval_outputs[stg]["preds"].extend(preds)
                        # eval_outputs[stg]["labels"].extend(refs)
                        # eval_outputs[stg]["index"].extend(cells)

                    # DEBUG the metrics
                    # from ned.candidate_ranking.metrics.ned_metric import NEDMetrics
                    # NEDMetrics()._compute(
                    #     eval_outputs["train"]["preds"],
                    #     eval_outputs["train"]["labels"],
                    #     eval_outputs["train"]["index"],
                    # )
                    # NEDMetrics()._compute(preds, labels, cells)

                    kks = set()
                    for metric in metrics:
                        tmp = metric.compute()
                        assert tmp is not None
                        for k, v in tmp.items():
                            k = f"{stg}_{k}"
                            assert k not in kks, "Overlapping metric: {}".format(k)
                            postfix[k] = v
                            kks.add(k)

                progress_bar.set_postfix(postfix)
                accelerator.wait_for_everyone()

                if use_wandb:
                    wandb.log(
                        dict(
                            step=step,
                            **postfix,
                        ),
                        step=step,
                    )

                model.train()

            if ckpt_interval is not None and step % ckpt_interval == 0:
                unwrapped_model = accelerator.unwrap_model(model)
                latest_ckpt_file = ckpt_helper.save(step, unwrapped_model, optimizer)
        except KeyboardInterrupt:
            # gracefully handle CTRL+C, save the training to a file
            logger.info("KeyboardInterrupt, saving the model before stop...")
            unwrapped_model = accelerator.unwrap_model(model)
            latest_ckpt_file = ckpt_helper.save(step, unwrapped_model, optimizer)
            break
            # logger.info(
            #     "KeyboardInterrupt, saving the model before stop... finished! run evaluation now"
            # )

    unwrapped_model = accelerator.unwrap_model(model)
    if latest_ckpt_file is None or (
        ckpt_interval is not None and step % ckpt_interval != 0
    ):
        latest_ckpt_file = ckpt_helper.save(step, unwrapped_model, optimizer)

    return unwrapped_model, latest_ckpt_file


@contextmanager
def with_wandb(ckpt_helper: CkptHelper, metadata: dict, enable=True):
    if not enable:
        yield None
        return

    resume = None
    if ckpt_helper.is_resuming():
        restore_traindir = ckpt_helper.get_restore_training_dir()
        assert restore_traindir is not None
        if (restore_traindir / "wandb.json").exists():
            id = serde.json.deser(restore_traindir / "wandb.json")["id"]
            resume = "allow"

    if resume is None:
        id = wandb.util.generate_id()

    if not (ckpt_helper.get_training_dir() / "wandb.json").exists():
        (ckpt_helper.get_training_dir() / "wandb.json").write_bytes(
            orjson.dumps(
                {
                    "id": id,  # type: ignore
                }
            )
        )

    wandb.init(
        id=id,  # type: ignore
        project="ned",
        config={
            "ckpt_dir": ckpt_helper.ckpt_dir,
            **metadata,
        },
        resume=resume,
    )
    try:
        yield None
    finally:
        wandb.finish()
