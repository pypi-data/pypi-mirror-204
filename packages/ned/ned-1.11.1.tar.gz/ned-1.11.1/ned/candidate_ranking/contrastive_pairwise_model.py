from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Optional
from ned.candidate_ranking.cr_method import CandidateRankingMethod, ModelOutput
from ned.candidate_ranking.helpers.dataset import MyDataset
from ned.data_models.prelude import NEDExample, DatasetCandidateEntities
import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F
from ned.candidate_ranking.cr_dataset import (
    CRDataset,
    NoCacheCRDataset,
)
from ned.candidate_ranking.dataset.basic_features import (
    N_EXTRA_FEATURES,
    N_PAIRWISE_FEATURES,
)


@dataclass
class ContrastivePairwiseModelArgs:
    margin: float = 1.0


class ContrastivePairwiseModel(CandidateRankingMethod):
    VERSION = 100
    EXPECTED_ARGS = {"pos_features", "neg_features", "neg_size"}
    EXPECTED_EVAL_ARGS = {"pos_features"}
    EVAL_BATCH_SIZE = 1000

    def __init__(self, n_features: int, args: ContrastivePairwiseModelArgs):
        super().__init__()

        self.args = args
        self.cmp = nn.Sequential(
            nn.Linear(n_features, 2 * n_features),
            nn.ReLU(),
            nn.Linear(2 * n_features, n_features),
            nn.ReLU(),
            nn.Linear(n_features, n_features),
            nn.ReLU(),
            nn.Linear(n_features, 2),
        )

    @staticmethod
    def from_args(args: ContrastivePairwiseModelArgs):
        return ContrastivePairwiseModel(
            n_features=N_PAIRWISE_FEATURES + N_EXTRA_FEATURES, args=args
        )

    def forward(self, pos_features, neg_features=None, neg_size=None) -> ModelOutput:
        poslogits = self.cmp(pos_features)
        if neg_features is not None:
            assert neg_size is not None
            assert torch.sum(neg_size) == neg_features.shape[0]
            repeated_poslogits = torch.repeat_interleave(
                pos_features, neg_size, dim=0, output_size=neg_features.shape[0]
            )
            # calculate loss if neg features are provided
            neglogits = self.cmp(neg_features)

            posdistance = -F.log_softmax(repeated_poslogits, dim=1)[:, 1]
            negdistance = -F.log_softmax(neglogits, dim=1)[:, 0]

            loss = torch.max(
                posdistance - negdistance + self.args.margin,
                torch.zeros_like(posdistance),
            )
            loss = torch.mean(loss)
        else:
            loss = None

        return ModelOutput(loss=loss, probs=F.softmax(poslogits, dim=1)[:, 1])

    def generate_dataset(
        self,
        examples: list[NEDExample],
        candidates: DatasetCandidateEntities,
        num_proc: Optional[int] = None,
        for_training: bool = False,
        cache_dir: Optional[Path] = None,
    ) -> MyDataset:
        crds = CRDataset(cache_dir) if cache_dir is not None else NoCacheCRDataset()
        obj = crds.contrastive_pairwise_1(
            candidates=candidates,
            crents=crds.base_ent(examples, candidates),
            crcans=crds.base_can(examples, candidates),
            crcan_features=crds.can_features(examples, candidates),
            triplet_format=for_training,
        )

        if for_training:
            dtypes = {"pos_features": np.float32, "neg_features": np.float32}
            collate_fn = CRDataset.contrastive_pairwise_triplet_collate_fn
        else:
            dtypes = {"pos_features": np.float32}
            collate_fn = None

        return MyDataset(obj, dtypes, collate_fn)
