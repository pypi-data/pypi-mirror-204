from __future__ import annotations

from abc import abstractmethod, ABC
from pathlib import Path
from ned.candidate_ranking.helpers.dataset import MyDataset

from ned.data_models.pymodels import NEDExample


class ERModelInterface(ABC):
    @abstractmethod
    def gen_data(
        self,
        examples: list[NEDExample],
        for_training: bool = False,
        cache_dir: Path | None = None,
    ) -> MyDataset:
        pass

    @abstractmethod
    def get_gen_data_args(self):
        pass

    @abstractmethod
    def predict_data(
        self, examples: list[NEDExample], ds: MyDataset
    ) -> list[list[int]]:
        pass

    @abstractmethod
    def state_dict(self) -> dict:
        pass

    @abstractmethod
    def load_state_dict(self, state_dict: dict):
        pass
