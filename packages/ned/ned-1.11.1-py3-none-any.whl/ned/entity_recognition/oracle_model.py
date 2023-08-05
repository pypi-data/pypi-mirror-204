from __future__ import annotations
from dataclasses import dataclass, field

from pathlib import Path
from ned.candidate_ranking.helpers.dataset import MyDataset
from ned.data_models.prelude import NEDExample
from ream.params_helper import NoParams
from ned.entity_recognition.er_model_interface import ERModelInterface


@dataclass
class OracleERModelArgs:
    include_should_be_entity_columns: bool = field(
        default=False,
        metadata={
            "help": "Whether to include should_be_entity_columns in the prediction",
        },
    )


class OracleERModel(ERModelInterface):
    VERSION = 101

    def __init__(self, args: OracleERModelArgs):
        self.args = args

    def gen_data(
        self,
        examples: list[NEDExample],
        for_training: bool = False,
        cache_dir: Path | None = None,
    ):
        entity_columns = [e.entity_columns for e in examples]
        should_be_entity_columns = [e.should_be_entity_columns for e in examples]

        return MyDataset(
            {
                "entity_columns": entity_columns,
                "should_be_entity_columns": should_be_entity_columns,
                "example_id": [e.table.table_id for e in examples],
            }
        )

    def get_gen_data_args(self):
        return NoParams()

    def predict_data(
        self, examples: list[NEDExample], ds: MyDataset
    ) -> list[list[int]]:
        assert isinstance(ds.examples, dict)
        example_id = ds.examples["example_id"]
        entity_columns = ds.examples["entity_columns"]

        assert example_id == [e.table.table_id for e in examples]
        if self.args.include_should_be_entity_columns:
            should_be_entity_columns = ds.examples["should_be_entity_columns"]
            return entity_columns + should_be_entity_columns
        return entity_columns

    def state_dict(self) -> dict:
        return {}

    def load_state_dict(self, state_dict: dict):
        pass
