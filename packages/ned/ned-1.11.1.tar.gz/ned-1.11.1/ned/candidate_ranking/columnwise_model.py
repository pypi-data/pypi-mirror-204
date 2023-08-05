from dataclasses import dataclass
from pathlib import Path
from typing import List, Literal, Optional

import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.utils.data import DataLoader, Dataset

from ned.candidate_ranking.cr_dataset import (
    CRDataset,
    NoCacheCRDataset,
)
from ned.candidate_ranking.dataset.basic_features import (
    N_EXTRA_FEATURES,
    N_PAIRWISE_FEATURES,
)
from ned.candidate_ranking.cr_method import CandidateRankingMethod, ModelOutput
from ned.candidate_ranking.helpers.dataset import MyDataset
from ned.data_models.prelude import DatasetCandidateEntities, NEDExample
from tqdm import tqdm


@dataclass
class GenDatasetArgs:
    # whether to use the matched property with other columns as features
    feature_matched_prop: bool = True
    extended_types: Literal[
        "exact", "child_parent2prime", "parent1", "clustered_parent1"
    ] = "exact"
    training_add_missing_gold: Literal["no", "singleonly", "multiple"] = "multiple"
    training_topk: Optional[int] = 20


@dataclass
class ColumnwiseModelArgs(GenDatasetArgs):
    loss: Literal["nll", "triplet"] = "nll"
    class_weight: int = 0  # 0 means balanced, 1 means uniform.
    p_y_given_tx: Literal["aux_feat", "hard"] = "aux_feat"


class ColumnwiseModel(CandidateRankingMethod):
    """CHANGELOG:
    - 21x: change the model to use mask.
    - 221: add p_y_given_tx configuration, soft means we add I(t \in type(x)) as a feature while hard means we multiply with I(t \in type(x))
    """

    VERSION = 221
    EXPECTED_ARGS = {"label", "features", "mask", "types"}
    EXPECTED_EVAL_ARGS = {"features", "mask", "types"}
    EVAL_BATCH_SIZE = 1
    EVAL_ON_CPU = False

    def __init__(self, xdim: int, args: ColumnwiseModelArgs):
        super().__init__()

        self.args = args
        assert args.loss == "nll"

        self.logits_s_ij = nn.Sequential(
            nn.Linear(xdim, 2 * xdim),
            nn.ReLU(),
            nn.Linear(2 * xdim, xdim),
            nn.ReLU(),
            nn.Linear(xdim, xdim),
            nn.ReLU(),
            nn.Linear(xdim, 1),
        )
        if self.args.p_y_given_tx == "aux_feat":
            aug_xdim = xdim + 1
        else:
            aug_xdim = xdim
        self.logits_f_ij = nn.Sequential(
            nn.Linear(aug_xdim, 2 * aug_xdim),
            nn.ReLU(),
            nn.Linear(2 * aug_xdim, aug_xdim),
            nn.ReLU(),
            nn.Linear(aug_xdim, aug_xdim),
            nn.ReLU(),
            nn.Linear(aug_xdim, 2),
        )
        self.class_weights = torch.FloatTensor([1, 1])

    @staticmethod
    def from_args(args: ColumnwiseModelArgs):
        if args.feature_matched_prop:
            n_features = N_PAIRWISE_FEATURES + N_EXTRA_FEATURES + 1
        else:
            n_features = N_PAIRWISE_FEATURES + N_EXTRA_FEATURES
        return ColumnwiseModel(xdim=n_features, args=args)

    def to(self, device):
        out = super().to(device)
        out.class_weights = out.class_weights.to(device)
        return out

    def forward(
        self,
        features: torch.Tensor,
        types: torch.Tensor,
        mask: torch.Tensor,
        label: Optional[torch.Tensor] = None,
    ):
        """Make a forward pass and compute column types as well as linked entities

        Arguments:
            features: 1 x I x J x F
            types: 1 x I x J x T
            mask: 1 x I x J
            label: 1 x I x J
        """
        # convert to I x J x <>
        features = features.squeeze(0)
        types = types.squeeze(0)
        mask = mask.squeeze(0)
        mask_3d = mask.unsqueeze(2)
        mask_4d = mask_3d.unsqueeze(3)

        # # I x J x 1 -- the difference between x1 and x2?
        logits_s_ij = self.logits_s_ij(features)
        logits_s_ij = torch.sigmoid(logits_s_ij)
        logits_s_ij = (
            logits_s_ij * mask_3d
        )  # multiply to set the value of masked entries to 0
        logits_s_ij.shape

        # I x T
        logits_t_given_x, logits_t_given_x_max_j_index = (logits_s_ij * types).max(
            dim=1
        )
        logits_t_given_x.shape

        # T x 1 -- the probability of each type,
        p_t_given_x = F.softmax(logits_t_given_x.sum(0), dim=0)
        p_t_given_x.shape
        # p_t_given_x = torch.zeros((types.shape[2],)).to(types.device)
        # p_t_given_x[1] = 1.0

        log_probs = None
        if self.args.p_y_given_tx == "aux_feat":
            new_feats = features.reshape(
                features.shape[0], features.shape[1], 1, features.shape[2]
            )
            new_feats = new_feats.expand(
                features.shape[0],
                features.shape[1],
                p_t_given_x.shape[0],
                features.shape[2],
            )
            # I x J x T x F
            new_feats.shape
            transpose_cand_types = types
            # I x J x T x 1
            transpose_cand_types = torch.unsqueeze(transpose_cand_types, 3)
            transpose_cand_types.shape
            # I x J x T x (F+1)
            merged_feat = torch.cat([new_feats, transpose_cand_types], dim=3)
            merged_feat.shape

            # I x J x T x 2
            p_y_given_tx = F.softmax(self.logits_f_ij(merged_feat), dim=3)
            p_y_given_tx.shape

            # I x J x 2
            probs = (
                p_y_given_tx
                * mask_4d
                * p_t_given_x.reshape(1, 1, p_t_given_x.shape[0], 1)
            ).sum(2)
            probs.shape

            if label is not None:
                # calculate log prob related to the mask
                log_probs = (
                    torch.log(
                        (
                            p_y_given_tx
                            * p_t_given_x.reshape(1, 1, p_t_given_x.shape[0], 1)
                        ).sum(2)
                    )
                    * mask_3d
                )
                # log_y_given_tx = torch.log(p_y_given_tx) * mask_4d
                # # log_p_t_given_x = torch.log(p_t_given_x)
                # # log_probs = log_y_given_tx + log_p_t_given_x.reshape(
                # #     1, 1, p_t_given_x.shape[0], 1
                # # )
                # # log_probs = log_probs.sum(2)
                # log_probs = torch.log(probs)
        elif self.args.p_y_given_tx == "hard":
            # I x J x 2
            score_y_given_tx = F.softmax(self.logits_f_ij(features), dim=2)
            score_y_given_tx.shape

            p_t_given_xij = p_t_given_x.reshape(1, 1, p_t_given_x.shape[0])
            p_t_in_dij = (p_t_given_xij * types).sum(dim=2, keepdim=True)
            p_t_in_dij.shape
            p_t_not_in_dij = 1 - p_t_in_dij
            p_t_not_in_dij.shape

            default = (
                torch.FloatTensor([0.99, 0.01])
                .to(score_y_given_tx.device)
                .reshape(1, 1, 2)
            )
            default.shape

            # diff = (
            #     torch.FloatTensor([0.5, -0.5])
            #     .to(score_y_given_tx.device)
            #     .reshape(1, 1, 2)
            # )
            # score_y_given_tx

            probs = score_y_given_tx * p_t_in_dij + default * p_t_not_in_dij
            probs.shape

            if label is not None:
                log_probs = torch.log(probs)
            # (probs.sum(dim=2) < 1.0).nonzero()
            # # I x J x T x 2
            # score_y_given_tx = self.logits_f_ij(new_feats)
            # p_y_given_tx = F.softmax(score_y_given_tx, dim=3)
            # # set t not \in x to 0 for y = 1 and to 1 for y = 0
            # p_y_given_tx = p_y_given_tx * torch.unsqueeze(types, dim=3) + torch.stack(
            #     [(1 - types), torch.zeros_like(types)], dim=3
            # )
        else:
            raise NotImplementedError()

        if label is None:
            loss = None
        else:
            assert log_probs is not None
            label = torch.squeeze(label, dim=0)
            # filter = p_t_in_dij[:, :, 0] > 0
            # label = label[filter]
            # probsx = probs[filter]
            # output = score_y_given_tx[filter]
            # output = probs
            # probs = score_y_given_tx
            # label.shape
            # assert mask.sum() == mask.numel()
            # loss = F.nll_loss(
            #     torch.log(output.reshape(-1, output.shape[-1])),
            #     label.reshape(-1),
            #     weight=torch.FloatTensor([1, 6]).to(output.device),
            #     # reduction="none",
            # )
            # loss is (I x J) as reduction is None
            # self.class_weights = torch.FloatTensor([1, 6]).to(probs.device)
            loss = F.nll_loss(
                log_probs.reshape(-1, log_probs.shape[-1]),
                label.reshape(-1),
                weight=self.class_weights,
                reduction="none",
            )
            # loss = F.cross_entropy(
            #     probs.reshape(-1, probs.shape[-1]),
            #     label.reshape(-1),
            #     weight=self.class_weights,
            #     reduction="none",
            # )
            tmp = label.type(torch.int64).reshape(-1, 1)
            weights = self.class_weights.reshape(1, -1)
            weights = weights.expand(tmp.shape[0], -1)
            mask1d = mask.reshape(-1)
            # normalize by the weighted examples
            Z = (torch.gather(weights, 1, tmp)[:, 0] * mask1d).sum()
            loss = (loss * mask1d).sum() / Z
            # assert not torch.isnan(loss)

        return ModelOutput(loss=loss, probs=probs[:, :, 1])

    def generate_dataset(
        self,
        examples: List[NEDExample],
        candidates: DatasetCandidateEntities,
        num_proc: Optional[int] = None,
        for_training: bool = False,
        cache_dir: Optional[Path] = None,
    ) -> Dataset:
        crds = CRDataset(cache_dir) if cache_dir is not None else NoCacheCRDataset()
        crents = crds.base_ent(examples, candidates)
        if self.args.feature_matched_prop:
            crent_matched_props = crds.ent_matched_props(examples, crents)
            crcan_matched_props = crds.can_matched_props(examples, candidates)
        else:
            crent_matched_props = None
            crcan_matched_props = None

        crcan_types = crds.can_types(
            examples,
            candidates,
            extended_mode="no"
            if self.args.extended_types == "exact"
            else self.args.extended_types,
        )
        crent_types = crds.ent_types(
            examples,
            crents,
            extended_mode="no"
            if self.args.extended_types == "exact"
            else self.args.extended_types,
        )

        obj = crds.columnwise_1(
            candidates=candidates,
            crents=crds.base_ent(examples, candidates),
            crcans=crds.base_can(examples, candidates),
            crent_features=crds.ent_features(crents),
            crcan_features=crds.can_features(examples, candidates),
            crcan_matched_props=crcan_matched_props,
            crent_matched_props=crent_matched_props,
            crcan_types=crcan_types,
            crent_types=crent_types,
            add_missing_gold="no"
            if not for_training
            else self.args.training_add_missing_gold,
            top_k=self.args.training_topk if for_training else None,
        )
        ds = MyDataset(obj, {"features": np.float32})
        return ds

    def get_generating_dataset_args(self):
        return GenDatasetArgs(
            self.args.feature_matched_prop,
            self.args.extended_types,
            self.args.training_add_missing_gold,
            self.args.training_topk,
        )

    def rank_datasets(
        self,
        examples: List[NEDExample],
        candidates: DatasetCandidateEntities,
        dataset: Dataset,
        verbose: bool = False,
    ) -> DatasetCandidateEntities:
        self.eval()
        params = next(self.parameters())
        device = params.device

        dloader = DataLoader(
            dataset,
            batch_size=self.EVAL_BATCH_SIZE,
            shuffle=False,
            pin_memory=params.is_cuda,
        )

        with torch.no_grad():
            probs = []
            can_idx = []
            for batch in tqdm(dloader, total=len(dloader), disable=not verbose):
                kwargs = {}
                for arg in self.EXPECTED_EVAL_ARGS:
                    kwargs[arg] = batch[arg].to(device)
                output = self.forward(**kwargs)

                mask = batch["mask"].reshape(-1)
                # TODO: fix me!
                # as batch size is now forced to be 1, probs has the shape: I x J
                probs.append(output.probs.cpu().reshape(-1)[mask])
                # batch['can_idx'] has the shape: B x I x J
                can_idx.append(batch["can_idx"].reshape(-1)[mask])

            probs = torch.cat(probs).numpy()
            can_idx = torch.cat(can_idx).numpy()

        assert candidates.score.shape == probs.shape
        score = np.zeros_like(candidates.score)
        score[can_idx] = probs
        return candidates.replace("score", score)
