from __future__ import annotations
from ned.candidate_ranking.helpers.training_helper import SklearnClassifier
import numpy as np
from dataclasses import dataclass, field
from pathlib import Path
from typing import Literal, Optional
from ned.candidate_ranking.helpers.dataset import MyDataset, MyDatasetDict
from ned.data_models.pymodels import NEDExample
from ned.entity_recognition.model_data.main import (
    ERFeature,
    ERModelData,
    NoCacheERModelData,
)
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import precision_recall_fscore_support, recall_score
from ned.entity_recognition.er_model_interface import ERModelInterface


@dataclass
class GenDatasetArgs:
    features: Optional[list[ERFeature]] = field(
        default=None,
        metadata={
            "help": "Features to use in entity recognition model",
        },
    )


@dataclass
class EnsembleModelArgs(GenDatasetArgs):
    classifier: Literal["random_forest", "xgboost"] = field(
        default="random_forest",
        metadata={
            "help": "Ensemble model to use",
        },
    )
    n_estimators: int = field(
        default=100,
        metadata={
            "help": "Number of estimators in the ensemble model",
        },
    )
    min_recall: float = field(
        default=0.95,
        metadata={
            "help": "Minimum recall that the ensemble model should achieve, this is used to tune the threshold.",
        },
    )


class EnsembleModel(SklearnClassifier, ERModelInterface):
    VERSION = 101
    TRAIN_ARGS = ["label", "features"]
    EVAL_ARGS = ["features"]
    METRIC_REF_ARGS = {
        "Precision": {"references": "label", "predictions": "predictions"},
        "Recall": {"references": "label", "predictions": "predictions"},
        "F1": {"references": "label", "predictions": "predictions"},
    }

    def __init__(self, args: EnsembleModelArgs):
        assert args.classifier == "random_forest"
        self.args = args
        self.classifier = RandomForestClassifier(n_estimators=args.n_estimators)
        # a threshold that is used to convert probability to label, the threshold is tuned
        # based on the minimum recall
        self.threshold = 0.5

    def fit(self, features: np.ndarray, label: np.ndarray):
        self.classifier.fit(features, label)
        # tuning the threshold based on the recall
        prob = self.classifier.predict_proba(features)[:, 1]
        threshold = 1
        while threshold > 0:
            ypred = (prob > threshold).astype(np.int32)
            recall = recall_score(label, ypred)
            if recall >= self.args.min_recall:
                self.threshold = threshold
                break
            threshold -= 0.05

    def predict(self, features: np.ndarray):
        prob = self.classifier.predict_proba(features)[:, 1]
        ypred = (prob > self.threshold).astype(np.int32)
        return ypred

    def predict_proba(self, features: np.ndarray):
        return self.classifier.predict_proba(features)[:, 1]

    def state_dict(self):
        return {
            "classifier": self.classifier,
            "threshold": self.threshold,
        }

    def load_state_dict(self, state_dict: dict):
        self.classifier = state_dict["classifier"]
        self.threshold = state_dict["threshold"]

    def gen_data(
        self,
        examples: list[NEDExample],
        for_training: bool = False,
        cache_dir: Path | None = None,
    ):
        ermd = ERModelData(cache_dir) if cache_dir is not None else NoCacheERModelData()
        feature_store = ermd.feature_store(examples)

        return MyDataset(
            {
                "id": feature_store.id,
                "features": feature_store.features,
                "label": feature_store.label,
            }
        )

    def get_gen_data_args(self):
        return GenDatasetArgs(self.args.features)

    def predict_data(
        self, examples: list[NEDExample], ds: MyDataset
    ) -> list[list[int]]:
        entity_columnss = []
        ypred = self.predict(ds.examples["features"])

        # the iter order must match with the order in feature score
        count = 0
        for example in examples:
            start = count
            end = count + len(example.table.columns)
            count = end

            entity_columns = np.arange(len(example.table.columns))[
                ypred[start:end]
            ].tolist()
            entity_columnss.append(entity_columns)

        return entity_columnss
