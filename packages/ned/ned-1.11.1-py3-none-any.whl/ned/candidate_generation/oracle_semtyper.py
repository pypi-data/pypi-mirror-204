from __future__ import annotations
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path
from typing import Literal, Mapping
from hugedict.prelude import HugeMutableMapping
from kgdata.wikidata.db import WikidataDB
from kgdata.wikidata.models.wdclass import WDClass
from ned.candidate_generation.common import CandidateRankingComplexMethod
from ned.candidate_generation.pyserini_wrapper import PyseriniArgs, PyseriniWrapper
from ned.candidate_ranking.helpers.db_helper import _gather_entities_attr
from ned.data_models.prelude import (
    DatasetCandidateEntities,
    ColumnCandidateEntities,
    CellCandidateEntities,
    NEDExample,
)
import ray
from ream.data_model_helper import ContiguousIndexChecker
from sm.misc.ray_helper import get_instance, ray_map, ray_put


FilterMode = Literal[
    "exact",
    "child1",
    "parent1",
    "parent2",
    "child2",
    "child_parent1",
    "child_parent2",
    "limited_freepath2",
]


@dataclass
class OracleSemTyperArgs(PyseriniArgs):
    filter_mode: FilterMode = "exact"


class OracleSemTyper(CandidateRankingComplexMethod):
    VERSION = PyseriniWrapper.VERSION

    def __init__(
        self,
        pyserini_wrapper: PyseriniWrapper,
        db: WikidataDB,
        args: OracleSemTyperArgs,
    ):
        self.pyserini_wrapper = pyserini_wrapper
        self.args = args
        self.db = db

    def get_candidates(
        self, examples: list[NEDExample], entity_columns: list[list[int]]
    ) -> DatasetCandidateEntities:
        candidates = self.pyserini_wrapper.get_candidates(examples, entity_columns)
        indexchecker = ContiguousIndexChecker()

        if not ray.is_initialized():
            ray.init()

        # filter out candidates that don't belong to the same column type
        rayargs = []
        provenanceargs = []
        dbref = ray_put(self.db.database_dir)
        for ei, example in enumerate(examples):
            tid = example.table.table_id
            entity_column_types = dict(
                zip(example.entity_columns, example.entity_column_types)
            )
            for ci in entity_columns[ei]:
                if ci not in entity_column_types:
                    entity_column_types[ci] = []

            for ci, (cstart, cend, cindex) in candidates.index[tid][-1].items():
                indexchecker.next(cstart, cend)
                cans = candidates.get_column_candidates(tid, ci)
                # filter_column_candidates_by_types(
                #     self.db.database_dir,
                #     cans,
                #     {ent.id for ent in entity_column_types[ci]},
                #     self.args.filter_mode,
                # )
                rayargs.append(
                    (
                        dbref,
                        cans,
                        {ent.entity for ent in entity_column_types[ci]},
                        self.args.filter_mode,
                    )
                )
                provenanceargs.append((tid, ci))

        resp = ray_map(filter_column_candidates_by_types.remote, rayargs)
        filtered_cans = defaultdict(dict)
        for (tid, ci), row2cans in zip(provenanceargs, resp):
            filtered_cans[tid][ci] = row2cans

        return DatasetCandidateEntities.from_npmodel_candidates(filtered_cans)


@ray.remote
def filter_column_candidates_by_types(
    database_dir: Path,
    candidates: ColumnCandidateEntities,
    coltypes: set[str],
    filtermode: FilterMode,
) -> dict[int, CellCandidateEntities]:
    id2types: dict[str, list[str]] = _gather_entities_attr(
        database_dir, candidates.id, "instanceof"
    )
    wdclasses: HugeMutableMapping[str, WDClass] = get_instance(
        lambda: WikidataDB(database_dir).wdclasses,
        f"kgdata.wikidata.db[{database_dir}]",
    ).cache()

    if filtermode != "exact" and (
        filtermode.find("child") != -1 or filtermode.startswith("limited_freepath")
    ):
        # gather all ancestors of the column types
        distance = int(filtermode[-1])
        coltype_levels = _get_class_ancestors(wdclasses, coltypes, distance)
    else:
        coltype_levels = [coltypes]

    newcans = {}
    for ri in candidates.index.index.keys():
        cans = candidates.get_cell_candidates(ri)
        can_ids = cans.id
        subset = []
        for i in range(can_ids.shape[0]):
            celltypes = id2types[can_ids[i]]
            if filtermode == "exact":
                if len(coltypes.intersection(celltypes)) > 0:
                    # we keep this candidate
                    subset.append(i)
            elif filtermode.startswith("parent"):
                # column type is a parent of the cell type
                distance = int(filtermode[-1])
                celltype_levels = _get_class_ancestors(
                    wdclasses, set(celltypes), distance
                )
                if any(
                    len(coltypes.intersection(level)) > 0 for level in celltype_levels
                ):
                    # keep this candidate
                    subset.append(i)
            elif filtermode.startswith("child_"):
                # column type can be a child of the cell type or parent of the cell type
                distance = int(filtermode[-1])
                celltype_levels = _get_class_ancestors(
                    wdclasses, set(celltypes), distance
                )
                if any(
                    len(coltypes.intersection(level)) > 0 for level in celltype_levels
                ):
                    # column type is a parent of the cell type
                    subset.append(i)
                elif any(
                    len(level.intersection(celltypes)) > 0 for level in coltype_levels
                ):
                    # column type is a child of the cell type
                    subset.append(i)
            elif filtermode.startswith("child"):
                # column type is a child of the cell type
                if any(
                    len(level.intersection(celltypes)) > 0 for level in coltype_levels
                ):
                    subset.append(i)
            else:
                assert filtermode.startswith("limited_freepath2")
                distance = 2
                celltype_levels = _get_class_ancestors(
                    wdclasses, set(celltypes), distance
                )
                if (
                    any(
                        len(coltypes.intersection(level)) > 0
                        for level in celltype_levels
                    )
                    or any(
                        len(level.intersection(celltypes)) > 0
                        for level in coltype_levels
                    )
                    or len(celltype_levels[1].intersection(coltype_levels[1])) > 0
                ):
                    subset.append(i)

        newcans[ri] = cans.select(subset)

    return newcans


def _get_class_ancestors(
    wdclasses: Mapping[str, WDClass], classids: set[str], distance: int
) -> list[set[str]]:
    """Get ancestors of a set of classes up until a level"""
    ancestor_levels = [classids]
    for i in range(distance):
        ancestors = set()
        for clsid in ancestor_levels[i]:
            cls = wdclasses[clsid]
            ancestors.update(cls.parents)
        ancestor_levels.append(ancestors)
    return ancestor_levels
