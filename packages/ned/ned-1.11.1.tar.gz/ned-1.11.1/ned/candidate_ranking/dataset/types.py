from __future__ import annotations
from typing import Callable, Literal, overload

import numpy as np
import ray
from hugedict.prelude import HugeMutableMapping
from nptyping import NDArray, Object, Shape
from ream.data_model_helper import ContiguousIndexChecker, NumpyDataModel

from kgdata.wikidata.db import WikidataDB
from kgdata.wikidata.models.wdclass import WDClass
from ned.candidate_generation.oracle_semtyper import _get_class_ancestors
from ned.candidate_ranking.dataset.base import CRDatasetEnt
from ned.candidate_ranking.helpers.db_helper import _gather_entities_attr
from ned.data_models.prelude import DatasetCandidateEntities
from ned.data_models.pymodels import NEDExample
from sm.misc.ray_helper import get_instance, ray_map, ray_put
from collections import defaultdict


class CRDatasetTypes(NumpyDataModel):
    __slots__ = ["types"]
    # the order of this object is the same as candidates
    # each item is a list of numbers, for wikidata entities, it is the id without Q
    types: NDArray[Shape["*"], Object]

    @overload
    @staticmethod
    def create(
        examples: list[NEDExample],
        candidates: DatasetCandidateEntities,
        extended_mode: Literal[
            "no", "parent1", "child_parent2prime", "clustered_parent1"
        ],
        explain: Literal[False] = False,
    ) -> CRDatasetTypes:
        ...

    @overload
    @staticmethod
    def create(
        examples: list[NEDExample],
        candidates: DatasetCandidateEntities,
        extended_mode: Literal["clustered_parent1"],
        explain: Literal[True],
    ) -> tuple[CRDatasetTypes, CRDatasetTypeEncoder]:
        ...

    @staticmethod
    def create(
        examples: list[NEDExample],
        candidates: DatasetCandidateEntities,
        extended_mode: Literal[
            "no", "parent1", "child_parent2prime", "clustered_parent1"
        ] = "no",
        explain: bool = False,
    ):
        # using a checker to make sure that the order of this object and candidates are the same
        idx_checker = ContiguousIndexChecker()
        args = []
        db_dir_ref = ray_put(WikidataDB.get_instance().database_dir)
        for example in examples:
            tstart, tend, tindex = candidates.index[example.table.table_id]
            for ci, ctypes in zip(example.entity_columns, example.entity_column_types):
                cstart, cend, cindex = tindex[ci]
                idx_checker.next(cstart, cend)
                if extended_mode == "child_parent2prime":
                    ctype_ids = {ctype.id for ctype in ctypes}
                    args.append((db_dir_ref, candidates.id[cstart:cend], ctype_ids))
                else:
                    args.append((db_dir_ref, candidates.id[cstart:cend]))

        if extended_mode == "no":
            func = gather_encoded_instanceof.remote
        elif extended_mode == "child_parent2prime":
            func = gather_encoded_extended_child_parent2prime_instanceof.remote
        elif extended_mode == "parent1":
            func = gather_encoded_extended_parent1_instanceof.remote
        elif extended_mode == "clustered_parent1":
            func = gather_encoded_extended_clustered_parent1_instanceof.remote
        else:
            raise ValueError(f"unknown extended_mode: {extended_mode}")

        types = ray_map(
            func,
            args,
            verbose=True,
            desc=f"extract candidate types (extended={extended_mode})",
        )

        if extended_mode == "clustered_parent1" and explain:
            out0 = []
            out0_newtypes = []

            for lst in types:
                out0.extend(lst[0])
                out0_newtypes.append(lst[1])

            out2_index = {}
            count = 0
            for example in examples:
                table_id = example.table.table_id
                out2_index[table_id] = {}
                for ci in candidates.index[table_id][2]:
                    out2_index[table_id][ci] = count
                    count += 1

            out = np.asarray(out0, dtype=np.object_)
            if len(out) != len(candidates):
                raise ValueError(f"{len(out)} != {len(candidates)}")
            return CRDatasetTypes(out), CRDatasetTypeEncoder(out2_index, out0_newtypes)
        else:
            out0 = []
            for lst in types:
                out0.extend(lst)
            out = np.asarray(out0, dtype=np.object_)
            if len(out) != len(candidates):
                raise ValueError(f"{len(out)} != {len(candidates)}")
            return CRDatasetTypes(out)

    @overload
    @staticmethod
    def encode_column_types(
        column_types: list[list[list[int]]],
    ) -> tuple[np.ndarray, list[int]]:
        ...

    @overload
    @staticmethod
    def encode_column_types(
        column_types: list[list[list[int]]],
        type_decoder: Callable[[int], list[str]]
        | dict[int, list[str]]
        | list[list[str]],
    ) -> tuple[np.ndarray, list[list[str]], list[list[str]]]:
        ...

    @staticmethod
    def encode_column_types(
        column_types: list[list[list[int]]],
        type_decoder: Callable[[int], list[str]]
        | dict[int, list[str]]
        | list[list[str]]
        | None = None,
    ):
        """Encode types of candidate entities in a column to a 3D tensor: R x C x T."""
        wdclasses = WikidataDB.get_instance().wdclasses.cache()

        type2index = {}
        new_types = []
        dim2 = 0
        for i, cell_types in enumerate(column_types):
            lst1 = []
            for can_types in cell_types:
                lst2 = []
                for t in can_types:
                    if t not in type2index:
                        type2index[t] = len(type2index)
                    lst2.append(type2index[t])
                lst1.append(np.array(lst2, dtype=np.uint8))
            dim2 = max(len(lst1), dim2)
            new_types.append(lst1)

        new_col_types = np.zeros(
            (len(new_types), dim2, len(type2index)), dtype=np.int32
        )
        for i, cell_types in enumerate(new_types):
            for j, can_types in enumerate(cell_types):
                new_col_types[i, j, can_types] = 1

        if type_decoder is None:
            index2type = [0] * len(type2index)
            for t, i in type2index.items():
                index2type[i] = t
            return new_col_types, index2type

        index2type = [[]] * len(type2index)
        index2label = [[]] * len(type2index)
        for t, i in type2index.items():
            if callable(type_decoder):
                tids = type_decoder(t)
            else:
                tids = type_decoder[t]
            index2type[i] = tids
            index2label[i] = [wdclasses[tid].label for tid in tids]
        return new_col_types, index2type, index2label


class CRDatasetTypeEncoder(NumpyDataModel):
    __slots__ = ["index", "encoder"]
    # the order of this object is not the same as candidates, therefore it needs an index
    # to map from table_id to (tstart, tend, { column id to position })
    index: dict[str, dict[int, int]]
    # each encoder is a mapping (represented by a list) from new type id (index of a the list) to list of old type ids
    encoder: NDArray[Shape["*"], Object]


CRDatasetTypes.init()
CRDatasetTypeEncoder.init()


@ray.remote
def gather_encoded_instanceof(database_dir, col_ents):
    id2types: dict[str, list[str]] = _gather_entities_attr(
        database_dir, set(col_ents), "instanceof"
    )
    type2index = {}
    for types in id2types.values():
        for t in types:
            if t not in type2index:
                type2index[t] = encoded_type(t)

    return [[type2index[t] for t in id2types[eid]] for eid in col_ents]


@ray.remote
def gather_encoded_extended_parent1_instanceof(database_dir, col_ents):
    id2types: dict[str, list[str]] = _gather_entities_attr(
        database_dir, set(col_ents), "instanceof"
    )
    wdclasses: HugeMutableMapping[str, WDClass] = get_instance(
        lambda: WikidataDB(database_dir).wdclasses,
        f"kgdata.wikidata.db[{database_dir}]",
    ).cache()

    for id, types in id2types.items():
        newtypes = set(types)
        type_levels = _get_class_ancestors(wdclasses, newtypes, 1)
        for level in type_levels[1:]:
            newtypes.update(level)
        id2types[id] = sorted(newtypes)

    type2index = {}
    for types in id2types.values():
        for t in types:
            if t not in type2index:
                type2index[t] = encoded_type(t)

    return [[type2index[t] for t in id2types[eid]] for eid in col_ents]


@ray.remote
def gather_encoded_extended_clustered_parent1_instanceof(database_dir, col_ents):
    id2types: dict[str, list[str]] = _gather_entities_attr(
        database_dir, set(col_ents), "instanceof"
    )
    wdclasses: HugeMutableMapping[str, WDClass] = get_instance(
        lambda: WikidataDB(database_dir).wdclasses,
        f"kgdata.wikidata.db[{database_dir}]",
    ).cache()

    for id, types in id2types.items():
        newtypes = set(types)
        type_levels = _get_class_ancestors(wdclasses, newtypes, 1)
        for level in type_levels[1:]:
            newtypes.update(level)
        id2types[id] = sorted(newtypes)

    # if a type is seen together in the same entity, we merge them
    cluster_id = 0
    type_remap = {}
    for id, types in id2types.items():
        cluster_ids = {type_remap[type] for type in types if type in type_remap}
        if len(cluster_ids) == 0:
            # we haven't seen those type, so they got a new id
            cluster_id += 1
            for type in types:
                type_remap[type] = cluster_id
        elif len(cluster_ids) == 1:
            # all of them are in the same cluster, we're good
            old_cluster_id = next(iter(cluster_ids))
            for type in types:
                if type not in type_remap:
                    type_remap[type] = old_cluster_id
        else:
            # some of them are in one cluster, some of them are in another cluster, so we have to merge those cluster
            cluster_id += 1
            for type in types:
                if type not in type_remap:
                    type_remap[type] = cluster_id
            for type, old_cluster_id in type_remap.items():
                if old_cluster_id in cluster_ids:
                    type_remap[type] = cluster_id

    type2index = {}
    cluster_id_remap = {}

    for type, cluster_id in type_remap.items():
        if cluster_id not in cluster_id_remap:
            cluster_id_remap[cluster_id] = len(cluster_id_remap)
        type2index[type] = cluster_id_remap[cluster_id]

    newtypes = [[] for _ in range(len(cluster_id_remap))]
    for type, index in type2index.items():
        newtypes[index].append(type)

    return (
        [list({type2index[t] for t in id2types[eid]}) for eid in col_ents],
        newtypes,
    )


@ray.remote
def gather_encoded_extended_child_parent2prime_instanceof(
    database_dir, col_ents, col_types: set[str]
):
    # TODO: fix me, cause currently we can't get the child types of a type yet.
    id2types: dict[str, list[str]] = _gather_entities_attr(
        database_dir, set(col_ents), "instanceof"
    )
    wdclasses: HugeMutableMapping[str, WDClass] = get_instance(
        lambda: WikidataDB(database_dir).wdclasses,
        f"kgdata.wikidata.db[{database_dir}]",
    ).cache()

    parent_coltypes = _get_class_ancestors(wdclasses, col_types, 1)[1]

    for id, types in id2types.items():
        newtypes = set(types)
        if len(parent_coltypes.intersection(types)) > 0:
            newtypes.update(col_types)

        cantype_levels = _get_class_ancestors(wdclasses, newtypes, 2)
        for level in cantype_levels:
            newtypes.update(level)

        id2types[id] = list(newtypes)

    type2index = {}
    for types in id2types.values():
        for t in types:
            if t not in type2index:
                type2index[t] = encoded_type(t)

    return [[type2index[t] for t in id2types[eid]] for eid in col_ents]


def encoded_type(type: str):
    assert type.startswith("Q") and type[1:].isdigit()
    index = int(type[1:])
    assert index < 2000000000
    return index
