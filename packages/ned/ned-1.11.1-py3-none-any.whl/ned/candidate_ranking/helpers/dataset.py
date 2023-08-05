from __future__ import annotations

import pickle, numpy as np, pandas as pd
from typing import Any, Dict, Optional, Union, Callable
import orjson
from torch.utils.data import Dataset
from pathlib import Path
from ream.dataset_helper import DatasetDict


class ColumnarDataset(Dataset):
    """A columnar dataset"""

    def __init__(
        self,
        columns: dict[str, np.ndarray | list],
        dtypes: Optional[dict[str, Any]] = None,
        collate_fn: Optional[Callable] = None,
    ):
        self.collate_fn = collate_fn
        self.columns = columns
        self.size = len(next(iter(self.columns.values())))
        self.dtypes = dtypes

        if dtypes is not None:
            for name, feat in self.columns.items():
                if name in dtypes and isinstance(feat, np.ndarray):
                    self.columns[name] = feat.astype(dtypes[name])
                    dtypes.pop(name)

    def __len__(self):
        return self.size

    def __getitem__(self, idx: int):
        return {name: feat[idx] for name, feat in self.columns.items()}

    def to_df(self):
        cols = {}
        for name, feat in self.columns.items():
            if not isinstance(feat, np.ndarray):
                raise ValueError(
                    f"Column {name} is not a numpy array, cannot convert dataset to dataframe"
                )
            if len(feat.shape) > 2:
                raise ValueError(
                    f"Column {name} has more than 2 dimensions, cannot convert dataset to dataframe"
                )
            if len(feat.shape) == 2:
                for i in range(feat.shape[1]):
                    cols[f"{name}_{i}"] = feat[:, i]
            else:
                cols[name] = feat
        return pd.DataFrame(cols)


class MyDataset(Dataset):
    """A columnar dataset"""

    def __init__(
        self,
        examples: Union[dict, list],
        dtypes: Optional[Dict[str, Any]] = None,
        collate_fn: Union[Callable, None] = None,
    ):
        self.is_dict = isinstance(examples, dict)
        self.collate_fn = collate_fn

        if self.is_dict:
            self.examples = examples.copy()
            self.size = len(next(iter(self.examples.values())))

            if dtypes is not None:
                for name, feat in self.examples.items():
                    if name in dtypes and isinstance(feat, np.ndarray):
                        self.examples[name] = feat.astype(dtypes[name])
                        dtypes.pop(name)
        else:
            self.examples = examples
            self.size = len(self.examples)

        self.dtypes = dtypes

    def __len__(self):
        return self.size

    def __getitem__(self, idx: int):
        if self.is_dict:
            out = {name: feat[idx] for name, feat in self.examples.items()}
        else:
            out = self.examples[idx]

        if self.dtypes is not None:
            for name, dtype in self.dtypes.items():
                out[name] = out[name].astype(dtype)
        return out

    @staticmethod
    def load_from_disk(path: Path):
        with open(str(path), "rb") as f:
            return pickle.load(f)

    def save_to_disk(self, path: Path):
        with open(str(path), "wb") as f:
            pickle.dump(self, f)


class MyDatasetDict(DatasetDict[Dataset]):
    serde = (MyDataset.save_to_disk, MyDataset.load_from_disk, "pkl")

    @property
    def shape(self):
        return {subset: len(dataset) for subset, dataset in self.items()}
