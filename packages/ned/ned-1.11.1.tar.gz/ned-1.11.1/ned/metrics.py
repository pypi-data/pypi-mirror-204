from __future__ import annotations
from dataclasses import dataclass
from typing import Optional, Protocol, Sequence, TypedDict, Union, cast
from typing_extensions import TypeGuard

from ned.candidate_generation.common import CandidateEntity
from ned.data_models.pymodels import NIL_ENTITY, NO_ENTITY
import numpy as np
from sm.misc.matrix import Matrix
from sm.evaluation.prelude import PrecisionRecallF1, recall_at_k


@dataclass
class ConfusionMatrix:
    tp: int = 0  # true positive
    fn: int = 0  # false negative
    fp: int = 0  # false positive
    tn: int = 0  # true negative

    def total(self):
        return self.tp + self.fn + self.fp + self.tn

    def precision(self):
        if self.total() == 0:
            return 1.0
        # the system must always predict something. NO_ENTITY is treated as a prediction
        if self.tp + self.fp > 0:
            return self.tp / (self.tp + self.fp)
        return 0.0

    def recall(self):
        if self.total() == 0:
            return 1.0
        # the system must always predict something. NO_ENTITY is treated as a prediction
        if self.tp + self.fn > 0:
            return self.tp / (self.tp + self.fn)
        return 0.0

    def f1(self):
        p = self.precision()
        r = self.recall()
        if p + r == 0:
            return 0.0
        return 2 * p * r / (p + r)

    def __add__(self, another: ConfusionMatrix):
        return ConfusionMatrix(
            self.tp + another.tp,
            self.fn + another.fn,
            self.fp + another.fp,
            self.tn + another.tn,
        )


def inkb_eval_table(
    gold_ents: Matrix[set[str]],
    pred_ents: Matrix[list[str]],
    k: Optional[Union[int, Sequence[Optional[int]]]] = None,
) -> tuple[dict[str, PrecisionRecallF1], dict[str, ConfusionMatrix]]:
    """Evaluate entity linking performance on a table using InKB metrics. As defined in Gerbil framework, InKB metrics
    only consider entities in KB as correct entities, NIL entity or entities outside of KB are consider incorrect and eliminated.

    This evaluation assumes that no pred entity is still a prediction (NO_ENTITY). Therefore, the system will never be able to
    achieve 1.0 precision by not predicting anything.

    Args:
        gold_ents: Matrix of gold entities for each cell. If the set of entities of a cell is empty, the
            cell does not contain any entity (no entity in KB).
        pred_ents: Matrix of predicted entities for each cell. If the list of candidate entities of a
            cell is empty, we do not predict any entity for the cell. Candidates in the list are sorted by
            their likelihood in descending order.
    """
    nrows, ncols = gold_ents.shape()
    name2k: dict[str, Optional[int]] = {"perf@all": None}
    if k is not None:
        for ki in k if isinstance(k, Sequence) else [k]:
            if ki is not None:
                name2k[f"perf@{ki}"] = ki

    confusion_matrices = {name: ConfusionMatrix() for name in name2k}

    for i in range(nrows):
        for j in range(ncols):
            if len(gold_ents[i, j]) == 0:
                if len(pred_ents[i, j]) == 0:
                    # no entity in gold, no entity in pred, so no example
                    continue
                for name in name2k:
                    confusion_matrices[name].fp += 1
            else:
                ytrue = gold_ents[i, j]
                ypreds = pred_ents[i, j]

                assert len(ytrue.intersection((NO_ENTITY, NIL_ENTITY))) == 0
                assert len(set(ypreds).intersection((NO_ENTITY, NIL_ENTITY))) == 0

                for name, k in name2k.items():
                    if len(ytrue.intersection(ypreds[:k])) > 0:
                        confusion_matrices[name].tp += 1
                    else:
                        confusion_matrices[name].fn += 1

    output = {}
    for name, ki in name2k.items():
        cm = confusion_matrices[name]
        output[name] = PrecisionRecallF1(
            recall=cm.recall(),
            precision=cm.precision(),
            f1=cm.f1(),
        )

    return output, confusion_matrices


def recall(
    ytrue: list[str] | list[set[str]],
    ypreds: Union[list[list[CandidateEntity]], list[list[str]]],
    k: Optional[Union[int, Sequence[Optional[int]]]] = None,
):
    """Calculate recall@k for a list of queries.

    To support NIL and non entity predictions for this metrics, we use two special
    identifiers: NIL_ENTITY and NO_ENTITY in `ned.data_models`.

    Args:
        ytrue: List of true entities for each query. When there are more than one true entities of a query, we classify
            the prediction as correct if the prediction is one of the true entities.
        ypreds: List of predicted (candidate) entities for each query, sorted by their likelihood in decreasing order.
        k: Number of predicted (candidate) entities to consider. If None, all predicted entities are considered.
    """
    ypreds = _norm_ypreds(ypreds)
    return recall_at_k(ytrue, ypreds, k)


def mrr(
    ytrue: list[str] | list[set[str]],
    ypreds: list[list[CandidateEntity]] | list[list[str]],
) -> float:
    """Calculate MRR for a list of queries.

    NOTE: This function does not support evaluating NIL predictions yet.
    """
    if len(ytrue) == 0:
        return 0.0

    ypreds = _norm_ypreds(ypreds)
    out = 0.0

    if isinstance(ytrue[0], str):
        ytrue = cast(list[str], ytrue)
        for i in range(len(ytrue)):
            y = ytrue[i]
            out += next(
                (1 / j for j, ypred in enumerate(ypreds[i], start=1) if ypred == y), 0
            )
    else:
        ytrue = cast(list[set[str]], ytrue)
        for i in range(len(ytrue)):
            y = ytrue[i]
            out += next(
                (1 / j for j, ypred in enumerate(ypreds[i], start=1) if ypred in y), 0
            )
    return out / max(len(ytrue), 1)


def _norm_ypreds(
    ypreds: Union[list[list[CandidateEntity]], list[list[str]]]
) -> list[list[str]]:
    """Normalize the predictions to a list of candidate entities for each query"""
    if any(isinstance(ypred[0], CandidateEntity) for ypred in ypreds if len(ypred) > 0):
        return [
            [c.entity.id for c in ypred]
            for ypred in cast(list[list[CandidateEntity]], ypreds)
        ]
    else:
        return cast(list[list[str]], ypreds)
