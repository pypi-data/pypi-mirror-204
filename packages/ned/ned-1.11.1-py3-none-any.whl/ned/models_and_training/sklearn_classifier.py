from abc import abstractmethod
from collections import Sequence
from typing import (
    Generic,
    Mapping,
    Protocol,
    TypeVar,
)

import evaluate
from ream.dataset_helper import DatasetDict
from loguru import logger

from ned.candidate_ranking.helpers.dataset import MyDataset
from ned.candidate_ranking.helpers.training_helper import (
    ModifiedTrainingArguments,
    describe,
)


class SklearnClassifier:
    """Represent a sklearn classifier"""

    TRAIN_ARGS: Sequence[str]
    EVAL_ARGS: Sequence[str]
    # mapping from metric class name to metric auxiliary args (no predictions) to dataset args
    METRIC_REF_ARGS: Mapping[str, Mapping[str, str]]

    @abstractmethod
    def fit(self, **kwargs):
        """Fit the model with arguments obtained from the training dataset.
        The arguments are specified by the TRAIN_ARGS attribute."""
        pass

    @abstractmethod
    def predict(self, **kwargs):
        """Predict the labels of the examples in the evaluation dataset."""
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


M = TypeVar("M", bound=SklearnClassifier)
T = TypeVar("T", contravariant=True)


class GenData(Protocol, Generic[T]):
    def __call__(
        self, method: T, dataset_query: str, for_training: bool
    ) -> DatasetDict[MyDataset]:
        ...


def sklearn_train(
    model: M,
    gen_data: GenData[M],
    trainargs: ModifiedTrainingArguments,
    metrics: list[str],
) -> M:
    """Function to train a sklearn classifier"""
    dsdict = gen_data(model, trainargs.dataset, for_training=True)
    eval_dsdict = dsdict

    train_ds = dsdict["train"]
    eval_dss = [dsdict[ds] for ds in eval_dsdict.keys()]

    logger.info("Train the model")
    assert isinstance(
        train_ds.examples, dict
    ), "Examples of training dataset must be in a columnar format"
    model.fit(**{name: train_ds.examples[name] for name in model.TRAIN_ARGS})

    logger.info("Evaluate the model")
    metric_fns = [evaluate.load(metric) for metric in metrics]

    for ds in eval_dss:
        assert isinstance(ds.examples, dict)
        output = {}
        for metric in metric_fns:
            preds = model.predict(
                **{name: ds.examples[name] for name in model.EVAL_ARGS}
            )
            extraargs = {
                metricarg: ds.examples[dsarg] if dsarg != "predictions" else preds
                for metricarg, dsarg in model.METRIC_REF_ARGS[
                    metric.__class__.__name__
                ].items()
            }
            tmp = metric.compute(**extraargs)
            assert tmp is not None
            output.update(tmp)

        describe("Evaluation results", output)

    return model
