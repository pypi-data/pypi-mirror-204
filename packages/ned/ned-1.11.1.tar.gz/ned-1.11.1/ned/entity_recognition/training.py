from __future__ import annotations
from abc import abstractmethod
from typing import Callable, Generic, Protocol, Any, TypeVar
import evaluate
from loguru import logger
from ned.candidate_ranking.helpers.dataset import MyDatasetDict
import pickle
from ned.candidate_ranking.helpers.training_helper import (
    ModifiedTrainingArguments,
    SklearnClassifier,
    describe,
)


M = TypeVar("M", bound=SklearnClassifier)
T = TypeVar("T", contravariant=True)


class GenData(Protocol, Generic[T]):
    def __call__(
        self, method: T, dataset_query: str, for_training: bool
    ) -> MyDatasetDict:
        ...


def sklearn_train(
    model: M,
    gen_data: GenData[M],
    trainargs: ModifiedTrainingArguments,
    metrics: list[str],
) -> M:
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
