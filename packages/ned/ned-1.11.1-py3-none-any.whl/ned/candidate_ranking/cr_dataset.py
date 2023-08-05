from __future__ import annotations

from typing import Literal, Optional
from kgdata.wikidata.db import WikidataDB

import numpy as np
import ray
import torch
from loguru import logger
from ream.actor_state import ActorState
from ream.actors.base import BaseActor
from ream.cache_helper import (
    Cache,
    Cacheable,
    unwrap_cache_decorators,
)
from ream.dataset_helper import DatasetQuery
from ream.helper import orjson_dumps
from ream.params_helper import NoParams
from slugify import slugify
from tqdm import tqdm

from ned.actors.candidate_generation import CanGenActor
from ned.actors.dataset.prelude import NEDDatasetActor
from ned.candidate_ranking.cr_method import CandidateRankingMethod
from ned.candidate_ranking.dataset.base import (
    CRDatasetCan,
    CRDatasetEnt,
)
from ned.candidate_ranking.dataset.basic_features import CRDatasetFeatures
from ned.candidate_ranking.dataset.matched_prop_feature import CRDatasetMatchedProps
from ned.candidate_ranking.dataset.types import CRDatasetTypes
from ned.candidate_ranking.helpers.dataset import MyDatasetDict
from ned.data_models.prelude import DatasetCandidateEntities
from ned.data_models.pymodels import NEDExample


class CRDataset(Cacheable):
    @Cache.cls.dir(
        cls=CRDatasetEnt,
        cache_args=["provenance"],
        mem_persist=True,
        compression="lz4",
    )
    def base_ent(
        self,
        examples: list[NEDExample],
        candidates: DatasetCandidateEntities,
        provenance: str = "",
    ):
        return CRDatasetEnt.create(WikidataDB.get_instance(), examples, candidates)

    @Cache.cls.dir(
        cls=CRDatasetCan,
        cache_args=["provenance"],
        mem_persist=True,
        compression="lz4",
    )
    def base_can(
        self,
        examples: list[NEDExample],
        candidates: DatasetCandidateEntities,
        provenance: str = "",
    ):
        return CRDatasetCan.create(examples, candidates)

    @Cache.cls.dir(
        cls=CRDatasetFeatures,
        cache_args=["provenance"],
        mem_persist=True,
        compression="lz4",
    )
    def can_features(
        self,
        candidates: DatasetCandidateEntities,
        basecan: CRDatasetCan,
        provenance: str = "",
    ):
        return CRDatasetFeatures.create(
            basecan.cell, candidates.label, candidates.aliases, candidates.popularity
        )

    @Cache.cls.dir(
        cls=[DatasetCandidateEntities, CRDatasetFeatures, CRDatasetCan],
        cache_args=["top_k", "provenance"],
        mem_persist=True,
    )
    def can_topk(
        self,
        candidates: DatasetCandidateEntities,
        can_feats: Optional[CRDatasetFeatures] = None,
        can_base: Optional[CRDatasetCan] = None,
        baseent: Optional[CRDatasetEnt] = None,
        top_k: int = 100,
        remove_nil_entity: bool = False,
        provenance: str = "",
    ) -> tuple[
        DatasetCandidateEntities, Optional[CRDatasetFeatures], Optional[CRDatasetCan]
    ]:
        # assume that the candidates's scores are already computed.
        newcandidates, index_remap = candidates.top_k_candidates(
            top_k, baseent, return_index_remap=True, remove_nil_entity=remove_nil_entity
        )
        if can_feats is None and can_base is None:
            return newcandidates, None, None

        newidx = np.arange(len(newcandidates))
        ent_item_flag = index_remap == -1
        can_item_flag = index_remap != -1

        # reconstruct the index of added entities
        impute_pos = newidx[ent_item_flag]
        impute_ptr = 0
        ent_index = np.zeros(impute_pos.shape[0], dtype=np.int32)
        if impute_pos.shape[0] > 0:
            assert baseent is not None
            for tbl, (tstart, tend, tindex) in newcandidates.index.items():
                for ci, (cstart, cend, cindex) in tindex.items():
                    if cend < impute_pos[impute_ptr]:
                        # skip this candidate because the next impute position is after this candidate
                        continue
                    for ri, (rstart, rend) in cindex.items():
                        if rend > impute_pos[impute_ptr]:
                            # the gold entity is added to the candidates of this cell, since it is added to the bottom,
                            # we need to retrieve all added ents, which index is always less than rend.
                            tmp_i = impute_ptr + 1
                            while tmp_i < len(impute_pos) and rend > impute_pos[tmp_i]:
                                tmp_i += 1
                            # the gold entities added to this cell is between [imputed_pos[imputed_ptr], imputed_pos[tmp_i - 1] + 1)
                            erstart, erend = baseent.index[tbl][ci][ri]
                            ent_index[impute_ptr:tmp_i] = np.arange(erstart, erend)
                            impute_ptr = tmp_i
                            if impute_ptr >= len(impute_pos):
                                break
                    if impute_ptr >= len(impute_pos):
                        break
                if impute_ptr >= len(impute_pos):
                    break

        if can_feats is not None:
            if baseent is not None and impute_pos.shape[0] > 0:
                newcan_feats = np.zeros(
                    (len(newcandidates), can_feats.features.shape[1]),
                    dtype=can_feats.features.dtype,
                )
                newcan_feats[newidx[can_item_flag]] = can_feats.features[
                    index_remap[can_item_flag]
                ]
                ent_features = CRDatasetFeatures.create(
                    baseent.cell[ent_index],
                    baseent.entity_label[ent_index],
                    baseent.entity_aliases[ent_index],
                    baseent.entity_popularity[ent_index],
                )
                newcan_feats[impute_pos] = ent_features.features
            else:
                newcan_feats = can_feats.features[index_remap]

            can_feats = CRDatasetFeatures(newcan_feats)

        if can_base is not None:
            if baseent is not None and impute_pos.shape[0] > 0:
                cell = np.empty(len(newcandidates), dtype=can_base.cell.dtype)
                cell_id = np.empty(len(newcandidates), dtype=can_base.cell_id.dtype)
                table_index = np.empty(
                    len(newcandidates), dtype=can_base.table_index.dtype
                )
                row_index = np.empty(len(newcandidates), dtype=can_base.row_index.dtype)
                col_index = np.empty(len(newcandidates), dtype=can_base.col_index.dtype)
                is_correct = np.empty(
                    len(newcandidates), dtype=can_base.is_correct.dtype
                )

                can_index = newidx[can_item_flag]
                can_old_index = index_remap[can_item_flag]
                cell[can_index] = can_base.cell[can_old_index]
                cell_id[can_index] = can_base.cell_id[can_old_index]
                table_index[can_index] = can_base.table_index[can_old_index]
                row_index[can_index] = can_base.row_index[can_old_index]
                col_index[can_index] = can_base.col_index[can_old_index]
                is_correct[can_index] = can_base.is_correct[can_old_index]

                cell[impute_pos] = baseent.cell[ent_index]
                cell_id[impute_pos] = baseent.cell_id[ent_index]
                table_index[impute_pos] = baseent.table_index[ent_index]
                row_index[impute_pos] = baseent.row_index[ent_index]
                col_index[impute_pos] = baseent.col_index[ent_index]
                is_correct[impute_pos] = 1
                can_base = CRDatasetCan(
                    cell, cell_id, table_index, row_index, col_index, is_correct
                )
            else:
                can_base = CRDatasetCan(
                    can_base.cell[index_remap],
                    can_base.cell_id[index_remap],
                    can_base.table_index[index_remap],
                    can_base.row_index[index_remap],
                    can_base.col_index[index_remap],
                    can_base.is_correct[index_remap],
                )

        return newcandidates, can_feats, can_base

    @Cache.cls.dir(
        cls=CRDatasetTypes,
        cache_args=["extended_mode", "provenance"],
        mem_persist=True,
    )
    def can_types(
        self,
        examples: list[NEDExample],
        candidates: DatasetCandidateEntities,
        extended_mode: Literal[
            "no", "parent1", "child_parent2prime", "clustered_parent1"
        ] = "no",
        provenance: str = "",
    ):
        return CRDatasetTypes.create(examples, candidates, extended_mode=extended_mode)

    @Cache.cls.dir(
        cls=CRDatasetMatchedProps,
        cache_args=["provenance"],
        mem_persist=True,
    )
    def can_matched_props(
        self,
        examples: list[NEDExample],
        candidates: DatasetCandidateEntities,
        provenance: str = "",
    ):
        return CRDatasetMatchedProps.create(examples, candidates)

    def heuristic_scoring(
        self, candidates: DatasetCandidateEntities, can_features: CRDatasetFeatures
    ):
        feats = can_features.features
        score = (np.sum(feats[:, :-1], axis=1) + feats[:, -1] * 20) / feats.shape[1]
        return candidates.replace("score", score)

    def columnwise_1(
        self,
        candidates: DatasetCandidateEntities,
        crents: CRDatasetEnt,
        crcans: CRDatasetCan,
        crcan_features: CRDatasetFeatures,
        crent_features: CRDatasetFeatures,
        crcan_types: CRDatasetTypes,
        crent_types: CRDatasetTypes,
        crcan_matched_props: Optional[CRDatasetMatchedProps] = None,
        crent_matched_props: Optional[CRDatasetMatchedProps] = None,
        add_missing_gold: Literal["no", "singleonly", "multiple"] = "no",
        top_k: Optional[int] = 100,
    ):
        out_features = []
        out_labels = []
        out_cells = []
        out_types = []
        out_masks = []
        out_can_idx = []  # to keep track of the candidate ids for later reconstruction

        # matched_props must be present for both or for none
        assert (crcan_matched_props is not None) == (crent_matched_props is not None)

        if top_k is None:
            # find the max number of candidates
            ndsize = 0
            for tstart, tend, tindex in candidates.index.values():
                for cstart, cend, cindex in tindex.values():
                    ndsize = max(
                        ndsize, max(end - start for start, end in cindex.values())
                    )
        else:
            ndsize = top_k

        for tbl, (tstart, tend, tindex) in tqdm(
            candidates.index.items(), desc="columnwise dataset: prep"
        ):
            for ci, (cstart, cend, cindex) in tindex.items():
                col_features = []
                col_labels = []
                col_cells = []
                col_types = []
                col_masks = []
                col_can_idx = []

                for ri, (start, end) in cindex.items():
                    s, e = crents.index[tbl][ci][ri]
                    entities_id = crents.entity_id[s:e]
                    candidates_id = candidates.id[start:end]
                    features = crcan_features.features[start:end]

                    can_scores = (
                        np.sum(features[:, :-1], axis=1) + features[:, -1] * 20
                    ) / features.shape[1]
                    sortedindex = np.argsort(can_scores, kind="stable")[::-1]
                    if top_k is not None:
                        sortedindex = sortedindex[:top_k]

                    tmp_feats = features[sortedindex]
                    if crcan_matched_props is not None:
                        extra_features = crcan_matched_props.matched_props[start:end][
                            sortedindex
                        ]
                        tmp_feats = np.concatenate([tmp_feats, extra_features], axis=1)

                    tmp_labels = np.isin(
                        candidates_id[sortedindex], entities_id
                    ).astype(np.uint8)
                    tmp_ids = crcans.cell_id[start:end][sortedindex]
                    tmp_types = crcan_types.types[start:end][sortedindex]
                    tmp_masks = np.ones((ndsize,), dtype=bool)
                    tmp_can_idx = sortedindex + start
                    if tmp_feats.shape[0] < ndsize:
                        pad_size = (0, ndsize - tmp_feats.shape[0])
                        tmp_masks[tmp_feats.shape[0] :] = 0
                        tmp_feats = np.pad(
                            tmp_feats,
                            (pad_size, (0, 0)),  # type: ignore
                        )
                        tmp_labels = np.pad(tmp_labels, pad_size)
                        tmp_ids = np.pad(tmp_ids, pad_size)
                        tmp_types = list(tmp_types)
                        tmp_can_idx = np.pad(tmp_can_idx, pad_size)
                        for _ in range(pad_size[1]):
                            tmp_types.append([])

                    # no gold entities and we want to add missing gold entities
                    if (
                        tmp_labels.sum() == 0
                        and add_missing_gold != "no"
                        and len(entities_id) > 0
                    ):
                        ngolds = len(entities_id)
                        if add_missing_gold == "multiple":
                            # set the missing gold entities to the last entries
                            tmp_labels[-ngolds:] = 1
                            tmp_ids[-ngolds:] = crents.cell_id[s:e]
                            tmp_types[-ngolds:] = crent_types.types[s:e]
                            tmp_masks[-ngolds:] = 1
                            # can_idx is for debugging purposes, so we set it to -1 to indicate that it's not in the candidate list
                            tmp_can_idx[-ngolds:] = -1
                            if crent_matched_props is not None:
                                tmp_feats[-ngolds:] = np.concatenate(
                                    [
                                        crent_features.features[s:e],
                                        crent_matched_props.matched_props[s:e],
                                    ],
                                    axis=1,
                                )
                            else:
                                tmp_feats[-ngolds:] = crent_features.features[s:e]
                        else:
                            raise NotImplementedError()

                    col_features.append(tmp_feats)
                    col_labels.append(tmp_labels)
                    col_cells.append(tmp_ids)
                    col_types.append(tmp_types)
                    col_masks.append(tmp_masks)
                    col_can_idx.append(tmp_can_idx)

                out_features.append(np.stack(col_features))
                out_labels.append(np.stack(col_labels))
                out_cells.append(np.stack(col_cells))
                out_types.append(col_types)
                out_masks.append(np.stack(col_masks))
                out_can_idx.append(np.stack(col_can_idx))

        if top_k is None:
            assert sum(col_masks.sum() for col_masks in out_masks) == len(candidates)

        # transform col types into a vector multi-hot encoding
        # this is not an ideal way to do it, but we temporary doing it here as we still use huggingface datasets
        n_types = max(
            max(len(cell_types) for cell_types in col_types) for col_types in out_types
        )
        # assert n_types <= 16

        new_out_types = []
        type_encoding = []

        for col_types in tqdm(
            out_types, desc="columnwise dataset: encoding candidate types"
        ):
            # remap the index
            type2index = {}
            new_types = []
            for i, cell_types in enumerate(col_types):
                lst1 = []
                for can_types in cell_types:
                    lst2 = []
                    for t in can_types:
                        if t not in type2index:
                            type2index[t] = len(type2index)
                        lst2.append(type2index[t])
                    lst1.append(np.array(lst2, dtype=np.uint8))
                new_types.append(lst1)

            new_col_types = np.zeros(
                (len(new_types), len(new_types[0]), len(type2index)), dtype=np.int32
            )
            for i, cell_types in enumerate(new_types):
                for j, can_types in enumerate(cell_types):
                    new_col_types[i, j, can_types] = 1

            type_encoding.append(np.array(list(type2index), dtype=np.int32))
            new_out_types.append(new_col_types)

        return {
            "features": out_features,
            "label": out_labels,
            "cell": out_cells,
            "can_idx": out_can_idx,
            "mask": out_masks,
            "types": new_out_types,
            "type_encoding": type_encoding,
        }

    @staticmethod
    def contrastive_pairwise_triplet_collate_fn(batch):
        pos_features = []
        neg_features = []
        neg_size = []
        for b in batch:
            pos_features.append(torch.as_tensor(b["pos_features"]))
            neg_features.append(torch.as_tensor(b["neg_features"]))
            neg_size.append(b["neg_size"])
        pos_features = torch.stack(pos_features)
        neg_features = torch.concat(neg_features)
        neg_size = torch.tensor(neg_size)
        return {
            "pos_features": pos_features,
            "neg_features": neg_features,
            "neg_size": neg_size,
        }


class NoCacheCRDataset(CRDataset):
    def __init__(self):
        pass


unwrap_cache_decorators(NoCacheCRDataset)


class CanRankDataset(BaseActor[str, NoParams]):
    """CHANGELOG:
    - 200: switch to new ream version
    """

    VERSION = 216

    def __init__(
        self,
        cangen_actor: CanGenActor,
        dataset_actor: NEDDatasetActor,
    ):
        super().__init__(NoParams(), dep_actors=[cangen_actor, dataset_actor])
        self.cangen_actor = cangen_actor
        self.dataset_actor = dataset_actor

    def run_without_cache(
        self,
        method: CandidateRankingMethod,
        dsquery: str,
        for_training: bool = False,
        num_proc: Optional[int] = None,
    ):
        wfs = self.get_working_fs()
        dsquery_ = DatasetQuery.from_string(dsquery)
        # a build directory that is unique to the dataset query and can be shared across methods
        builddir = wfs.get(
            dsquery_.dataset + "_build", {"query": dsquery}, save_key=True
        )

        if builddir.exists():
            builddir_path = builddir.get()
        else:
            with builddir.reserve_and_track() as builddir_path:
                pass
        self.logger.debug(
            "Cache common sub-datasets to a build directory: {}", builddir_path
        )

        self.logger.debug("Retrieve candidates of dataset: {}", dsquery)
        dsdict = self.dataset_actor.run_dataset(dsquery)
        cangen_dsdict = self.cangen_actor.run_dataset(dsquery)
        # # fmt: off
        # from pathlib import Path
        # Path("/tmp/test.csv").write_text("\n".join(cangen_dsdict['train'].id))
        # # fmt: on
        self.logger.debug("Extract features of dataset: {}", dsquery)
        canrank_dsdict = MyDatasetDict(dsquery_.dataset, {})
        for split, candidates in cangen_dsdict.items():
            self.logger.debug("\tSubset: {}", split)
            examples = dsdict[split]
            myds, newcans = method.generate_dataset(
                examples,
                candidates,
                num_proc=num_proc,
                for_training=for_training,
                cache_dir=builddir_path / split,
                return_candidates=True,
            )
            # uncomment for debugging purpose
            # setattr(myds, "candidates", newcans)
            canrank_dsdict[split] = myds

        return canrank_dsdict

    def get_cache_key(
        self: CanRankDataset,
        method: CandidateRankingMethod,
        dsquery: str,
        for_training: bool = False,
        num_proc: Optional[int] = None,
    ):
        deps = [actor.get_actor_state() for actor in self.dep_actors]
        state = ActorState.create(
            method.__class__, method.get_generating_dataset_args(), dependencies=deps
        )
        return orjson_dumps(
            {"state": state.to_dict(), "dsquery": dsquery, "for_training": for_training}
        )

    def get_cache_dirname(
        self: CanRankDataset,
        method: CandidateRankingMethod,
        dsquery: str,
        for_training: bool = False,
        num_proc: Optional[int] = None,
    ):
        return slugify(
            f"{method.__class__.__name__}_{getattr(method, 'VERSION')}_{dsquery}_{for_training}"
        ).replace("-", "_")


# CanRankDataset.run = CanRankDataset.run_without_cache
CanRankDataset.run_dataset = Cache.cls.dir(
    cls=MyDatasetDict,
    cache_key=CanRankDataset.get_cache_key,
    dirname=CanRankDataset.get_cache_dirname,
)(CanRankDataset.run_without_cache)
