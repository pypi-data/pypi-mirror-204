from __future__ import annotations
from dataclasses import dataclass
from pathlib import Path
from typing import List, Literal, Optional

import orjson
import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F

from ned.candidate_ranking.cr_dataset import CRDataset, NoCacheCRDataset
from ned.candidate_ranking.cr_method import CandidateRankingMethod, ModelOutput
from ned.candidate_ranking.dataset.basic_features import (
    N_EXTRA_FEATURES,
    N_PAIRWISE_FEATURES,
)
from ned.candidate_ranking.helpers.dataset import MyDataset
from ned.data_models.prelude import DatasetCandidateEntities, NEDExample


@dataclass
class GenDatasetArgs:
    # whether to use the matched property with other columns as features
    feature_matched_prop: bool = True
    training_add_missing_gold: Literal["no", "multiple"] = "multiple"
    training_topk: int = 20


@dataclass
class PairwiseModelArgs(GenDatasetArgs):
    loss: Literal["nll"] = "nll"
    class_weight: int = 0  # 0 means balanced, 1 means uniform.


class PairwiseModel(CandidateRankingMethod):
    """CHANGELOG:

    - 101: fix dataset generation
    - 102: update pairwise dataset to use top 20 candidates
    - 103: migrate away from huggingface datasets
    - 104: reserve for a potential bug fixing
    - 110: add feature_matched_prop
    - 111: add class_weight
    """

    VERSION = 115
    EXPECTED_ARGS = {"label", "features"}
    EXPECTED_EVAL_ARGS = {"features"}
    EVAL_BATCH_SIZE = 1000

    def __init__(self, n_features: int, args: PairwiseModelArgs):
        super().__init__()

        self.args = args
        assert args.loss == "nll"

        self.cmp = nn.Sequential(
            nn.Linear(n_features, 2 * n_features),
            nn.ReLU(),
            nn.Linear(2 * n_features, n_features),
            nn.ReLU(),
            nn.Linear(n_features, n_features),
            nn.ReLU(),
            nn.Linear(n_features, 2),
        )
        self.class_weights = torch.FloatTensor([1, 1])

    @staticmethod
    def from_args(args: PairwiseModelArgs):
        if args.feature_matched_prop:
            n_features = N_PAIRWISE_FEATURES + N_EXTRA_FEATURES + 1
        else:
            n_features = N_PAIRWISE_FEATURES + N_EXTRA_FEATURES
        return PairwiseModel(n_features=n_features, args=args)

    def to(self, device):
        out = super().to(device)
        out.class_weights = out.class_weights.to(device)
        return out

    def forward(self, features, label=None) -> ModelOutput:
        logits = self.cmp(features)

        if label is not None:
            loss = F.nll_loss(
                input=F.log_softmax(logits, dim=1),
                target=label,
                weight=self.class_weights,
            )
        else:
            loss = None

        return ModelOutput(loss=loss, probs=F.softmax(logits, dim=1)[:, 1])

    def generate_dataset(
        self,
        examples: List[NEDExample],
        candidates: DatasetCandidateEntities,
        num_proc: Optional[int] = None,
        for_training: bool = False,
        cache_dir: Optional[Path] = None,
        return_candidates: bool = False,
    ) -> MyDataset | tuple[MyDataset, DatasetCandidateEntities]:
        crds = CRDataset(cache_dir) if cache_dir is not None else NoCacheCRDataset()
        # crds = NoCacheCRDataset()
        provenance = ""

        if for_training:
            # select top k candidates, the order is important for caching to work correctly (controlled by provenance)
            topk = self.args.training_topk
            crcan_base = crds.base_can(examples, candidates, provenance)
            crcan_features = crds.can_features(candidates, crcan_base, provenance)

            if self.args.training_add_missing_gold == "no":
                crents = None
            else:
                crents = crds.base_ent(examples, candidates, provenance)

            provenance = orjson.dumps(
                {"topk": topk, "add_gold": self.args.training_add_missing_gold}
            ).decode()
            candidates = crds.heuristic_scoring(candidates, crcan_features)
            candidates, crcan_features, crcan_base = crds.can_topk(
                candidates, crcan_features, crcan_base, crents, topk, provenance
            )
            assert crcan_features is not None and crcan_base is not None
            label = crcan_base.is_correct.astype(np.int64)
        else:
            crcan_base = crds.base_can(examples, candidates, provenance)
            crcan_features = crds.can_features(candidates, crcan_base, provenance)
            label = None

        features = crcan_features.features
        if self.args.feature_matched_prop:
            crcan_matched_props = crds.can_matched_props(
                examples, candidates, provenance
            )
            features = np.concatenate(
                [features, crcan_matched_props.matched_props], axis=1
            )

        obj = {
            "features": features,
            "cell": crcan_base.cell_id,
        }
        if label is not None:
            obj["label"] = label

        ds = MyDataset(obj, {"features": np.float32})
        if not return_candidates:
            # make sure this is no training dataset, so the candidates are consistent with the dataset
            assert not for_training
            return ds

        return ds, candidates

    def get_generating_dataset_args(self):
        return GenDatasetArgs(
            self.args.feature_matched_prop,
            self.args.training_add_missing_gold,
            self.args.training_topk,
        )
