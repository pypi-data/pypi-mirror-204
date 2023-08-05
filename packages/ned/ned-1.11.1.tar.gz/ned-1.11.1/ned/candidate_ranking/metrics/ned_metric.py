"""Precision, Recall, and F1 metrics for NED."""
from __future__ import annotations

import torch
import evaluate
import datasets
from sklearn.metrics import accuracy_score

_DESCRIPTION = """
In our problem, each example is a cell and list of its candidate entities.
For each cell, we select the candidate entity with the highest score as the prediction
of the cell. Then, we apply the accuracy metric.
"""

_KWARGS_DESCRIPTION = """
Args:
    predictions (`list` of `float`): Predicted likelihood of candidate entities.
    references (`list` of `int`): Ground truth labels.
    cells (`list` of `int`): Cell Ids.

Returns:
    total (`int`): Total number of cells.
    mrr (`float`)
    recall@1 (`float`)
    recall@5 (`float`)
    recall@10 (`float`)
    recall@20 (`float`)
"""


@evaluate.utils.file_utils.add_start_docstrings(_DESCRIPTION, _KWARGS_DESCRIPTION)
class NEDMetrics(evaluate.EvaluationModule):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.threshold = kwargs.get("threshold", 0.0)

    def _info(self):
        return evaluate.EvaluationModuleInfo(
            description=_DESCRIPTION,
            citation="",
            inputs_description=_KWARGS_DESCRIPTION,
            features=datasets.Features(
                {
                    "predictions": datasets.Value("float32"),
                    "references": datasets.Value("int32"),
                    "cells": datasets.Value("int32"),
                }
            ),
            reference_urls=[
                "https://scikit-learn.org/stable/modules/generated/sklearn.metrics.precision_recall_fscore_support.html"
            ],
        )

    def _compute(
        self,
        predictions: list[float],
        references: list[int],
        cells: list[int],
    ):
        # group predictions and references by cell
        return compute_ned_metrics(
            torch.tensor(predictions),
            torch.tensor(references),
            torch.tensor(cells),
            self.threshold,
        )


def compute_ned_metrics(
    predictions: torch.Tensor,
    references: torch.Tensor,
    cells: torch.Tensor,
    threshold: float,
):
    # group predictions and references by cell

    # using stable sort to make sure we have closest results to evaluating
    # outside of training
    cells, reorder_index = torch.sort(cells, stable=True)
    predictions = predictions[reorder_index]
    references = references[reorder_index]

    # get [start, end) boundaries of each cell
    range = (cells[:-1] != cells[1:]).nonzero() + 1
    groups = []
    start = 0
    for end in range:
        end = end.item()
        groups.append((start, end))
        start = end
    groups.append((start, predictions.shape[0]))

    # go through each group, and calculate mrr and other metrics
    mrr = 0.0
    recall = [0.0, 0.0, 0.0, 0.0]

    for start, end in groups:
        # don't use descending to make sure it has the same order as our other code
        preds, reorder = torch.sort(-predictions[start:end], stable=True)
        preds = -preds
        refs = references[start:end][reorder]

        gt_rank = refs.nonzero(as_tuple=True)[0] + 1
        if gt_rank.shape[0] == 0:
            # no ground-truth, predict when the top preds is less than a threshold
            if preds[0] < threshold:
                # predict correctly
                mrr += 1
                recall[0] += 1
                recall[1] += 1
                recall[2] += 1
                recall[3] += 1
        else:
            # have ground-truth, we need to filter out the preds that are less than a threshold
            gt_rank = gt_rank[preds[gt_rank - 1] >= threshold]
            mrr += 1 / gt_rank.max().item()
            recall[0] += (gt_rank == 1).sum().item()
            recall[1] += (gt_rank <= 5).sum().item()
            recall[2] += (gt_rank <= 10).sum().item()
            recall[3] += (gt_rank <= 20).sum().item()

    n = max(1, len(groups))
    mrr /= n
    recall = [r / n * 100 for r in recall]
    return {
        "total": n,
        "mrr": mrr,
        "recall@1": recall[0],
        "recall@5": recall[1],
        "recall@10": recall[2],
        "recall@20": recall[3],
    }
