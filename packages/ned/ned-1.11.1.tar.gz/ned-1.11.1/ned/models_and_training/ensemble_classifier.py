from __future__ import annotations
from dataclasses import dataclass, field
from typing import Literal, Optional

from ned.models_and_training.sklearn_classifier import SklearnClassifier
import numpy as np

from sklearn.ensemble import RandomForestClassifier
from xgboost import XGBClassifier
from sklearn.metrics import precision_recall_fscore_support, recall_score


@dataclass
class EnsembleClassifierArgs:
    features: Optional[list[str]] = field(
        default=None,
        metadata={
            "help": "Features to use in the classifier",
        },
    )
    classifier: Literal["random_forest", "xgboost"] = field(
        default="xgboost",
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
    min_recall: Optional[float] = field(
        default=None,
        metadata={
            "help": "Minimum recall that the ensemble model should achieve, this is used to tune the threshold.",
        },
    )


class EnsembleClassifier(SklearnClassifier):
    VERSION = 101
    TRAIN_ARGS = ["label", "features"]
    EVAL_ARGS = ["features"]
    METRIC_REF_ARGS = {
        "Precision": {"references": "label", "predictions": "predictions"},
        "Recall": {"references": "label", "predictions": "predictions"},
        "F1": {"references": "label", "predictions": "predictions"},
    }

    def __init__(self, args: EnsembleClassifierArgs):
        self.args = args
        # a threshold that is used to convert probability to label, the threshold is tuned
        # based on the minimum recall
        self.threshold = 0.5

        if args.classifier == "random_forest":
            self.classifier = RandomForestClassifier(n_estimators=args.n_estimators)
        elif args.classifier == "xgboost":
            self.classifier = XGBClassifier(n_estimators=args.n_estimators)
        else:
            raise ValueError(f"Unknown classifier {args.classifier}")

    def fit(self, features: np.ndarray, label: np.ndarray):
        self.classifier.fit(features, label)
        # tuning the threshold based on the recall
        prob = self.classifier.predict_proba(features)[:, 1]

        if self.args.min_recall is not None:
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
