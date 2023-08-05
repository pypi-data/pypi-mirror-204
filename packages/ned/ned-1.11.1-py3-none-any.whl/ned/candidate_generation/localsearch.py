from __future__ import annotations
from kgdata.wikidata.db import WikidataDB
from loguru import logger
from ned.actors.db import to_wikidata_db
import numpy as np
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional
from ned.candidate_generation.common import populate
from ned.data_models.npmodels import (
    CellCandidateEntities,
    DatasetCandidateEntities,
    TableCandidateEntities,
)
from ned.data_models.pymodels import CellLink, NEDExample

from ream.cache_helper import Cacheable
from ream.fs import FS
from sm.inputs.column import Column
from sm.misc.ray_helper import enhance_error_info, ray_map, ray_put
import grams.core as gcore
import grams.core.table as gcore_table
import grams.core.steps as gcoresteps
from timer import watch_and_report


@dataclass
class LocalSearchArgs:
    similarity: str = field(
        default="levenshtein",
        metadata={
            "help": "augment candidate entities discovered from matching entity properties with values in the same row. "
            "Using the similarity function and threshold to filter out irrelevant candidates. "
        },
    )
    threshold: float = field(
        default=2.0,
        metadata={
            "help": "add candidate entities discovered from matching entity properties with values in the same row. "
            "Any value greater than 1.0 mean we do not apply the similarity function"
        },
    )
    use_column_name: bool = field(
        default=False,
        metadata={
            "help": "add column name to the search text. This is useful for value such as X town, Y town, Z town. "
        },
    )
    search_all_columns: bool = field(
        default=False,
        metadata={"help": "search all columns instead of just the entity columns."},
    )


class LocalSearch:
    VERSION = 100

    def __init__(self, args: LocalSearchArgs, db: WikidataDB):
        self.args = args
        self.db = db

    def augment_candidates(
        self, examples: list[NEDExample], candidates: DatasetCandidateEntities
    ):
        using_ray = len(examples) > 1
        dbref = ray_put(self.db.database_dir, using_ray)
        paramref = ray_put(self.args, using_ray)

        table_cans = ray_map(
            rust_augment_candidates,
            [
                (
                    dbref,
                    ex,
                    candidates.get_table_candidates(ex.table.table_id),
                    paramref,
                    not using_ray,
                )
                for ex in examples
            ],
            verbose=True,
            desc="augmenting candidates",
            using_ray=using_ray,
            is_func_remote=False,
        )
        return DatasetCandidateEntities.from_table_candidates(
            {ex.table.table_id: tcans for ex, tcans in zip(examples, table_cans)}
        )


@enhance_error_info("1.table.table_id")
def rust_augment_candidates(
    data_dir: Path,
    example: NEDExample,
    candidates: TableCandidateEntities,
    params: LocalSearchArgs,
    verbose: bool,
):
    cfg = gcoresteps.CandidateLocalSearchConfig(
        params.similarity,
        params.threshold,
        params.use_column_name,
        None,
        params.search_all_columns,
    )
    gcore.GramsDB.init(str(data_dir))
    cdb = gcore.GramsDB.get_instance()

    db = to_wikidata_db(data_dir)

    newtable = to_rust_table(example, candidates)
    with watch_and_report(
        "create algorithm context",
        preprint=True,
        print_fn=logger.debug,
        disable=not verbose,
    ):
        context = cdb.get_algo_context(newtable, n_hop=1)
    with watch_and_report(
        "Performing local search",
        preprint=True,
        print_fn=logger.debug,
        disable=not verbose,
    ):
        newtable = gcoresteps.candidate_local_search(newtable, context, cfg)

    nrows, ncols = example.table.shape()
    newcans = {}
    for ci in range(ncols):
        newcans[ci] = {}
        for ri in range(nrows):
            tmp_links = newtable.get_links(ri, ci)
            assert len(tmp_links) <= 1
            if len(tmp_links) == 0:
                assert (
                    not candidates.has_cell_candidates(ri, ci)
                    or len(candidates.get_cell_candidates(ri, ci)) == 0
                )
                continue

            tmp_link = tmp_links[0]
            if not candidates.has_cell_candidates(ri, ci):
                ids = [c.id.id for c in tmp_link.candidates]
                labels, descs, aliases, popularity = populate(db, ids)

                newcans[ci][ri] = CellCandidateEntities(
                    index=None,
                    id=np.array(ids, dtype=np.object_),
                    label=np.array(labels, dtype=np.object_),
                    description=np.array(descs, dtype=np.object_),
                    aliases=np.array(aliases, dtype=np.object_),
                    popularity=np.array(popularity, dtype=np.float64),
                    score=np.array(
                        [c.probability for c in tmp_link.candidates],
                        dtype=np.float64,
                    ),
                    provenance=np.array(["local_search"] * len(ids), dtype=np.object_),
                )
            else:
                cell_cans = candidates.get_cell_candidates(ri, ci)
                existing_ids = set(cell_cans.id)

                new_ids = []
                new_scores = []
                for c in tmp_link.candidates:
                    if c.id.id not in existing_ids:
                        new_ids.append(c.id.id)
                        new_scores.append(c.probability)

                if len(new_ids) > 0:
                    labels, descs, aliases, popularity = populate(db, new_ids)
                    newcans[ci][ri] = CellCandidateEntities(
                        index=None,
                        id=np.concatenate(
                            [cell_cans.id, np.array(new_ids, dtype=np.object_)]
                        ),
                        label=np.concatenate(
                            [cell_cans.label, np.array(labels, dtype=np.object_)]
                        ),
                        description=np.concatenate(
                            [
                                cell_cans.description,
                                np.array(descs, dtype=np.object_),
                            ]
                        ),
                        aliases=np.concatenate(
                            [cell_cans.aliases, np.array(aliases, dtype=np.object_)]
                        ),
                        popularity=np.concatenate(
                            [
                                cell_cans.popularity,
                                np.array(popularity, dtype=np.float64),
                            ]
                        ),
                        score=np.concatenate(
                            [cell_cans.score, np.array(new_scores, dtype=np.float64)]
                        ),
                        provenance=np.concatenate(
                            [
                                cell_cans.provenance,
                                np.array(
                                    ["local_search"] * len(new_ids),
                                    dtype=np.object_,
                                ),
                            ]
                        ),
                    )
                else:
                    newcans[ci][ri] = cell_cans

    return TableCandidateEntities.from_cell_candidates(newcans)


def to_rust_table(
    ex: NEDExample, cans: TableCandidateEntities
) -> gcore_table.LinkedTable:
    def to_col(col: Column) -> gcore_table.Column:
        values = []
        for v in col.values:
            if isinstance(v, str):
                values.append(v)
            elif v is None:
                values.append("")
            else:
                raise ValueError(f"Unsupported value type: {type(v)}")
        return gcore_table.Column(col.index, col.clean_multiline_name, values)

    def to_links(ri: int, ci: int, link: Optional[CellLink]) -> list[gcore_table.Link]:
        if cans.has_cell_candidates(ri, ci):
            cell_cans = cans.get_cell_candidates(ri, ci)
        else:
            cell_cans = None

        if link is None:
            if cell_cans is not None and len(cell_cans) > 0:
                return [
                    gcore_table.Link(
                        start=0,
                        end=len(ex.table[ri, ci]),
                        url=None,
                        entities=[],
                        candidates=[
                            gcore_table.CandidateEntityId(
                                gcore_table.EntityId(cell_cans.id[i]),
                                cell_cans.score[i],
                            )
                            for i in range(len(cell_cans))
                        ],
                    )
                ]
            return []

        assert cell_cans is not None
        return [
            gcore_table.Link(
                start=0,
                end=len(ex.table[ri, ci]),
                url=None,
                entities=[gcore_table.EntityId(entid) for entid in link.entities],
                candidates=[
                    gcore_table.CandidateEntityId(
                        gcore_table.EntityId(cell_cans.id[i]), cell_cans.score[i]
                    )
                    for i in range(len(cell_cans))
                ],
            )
        ]

    return gcore_table.LinkedTable(
        ex.table.table_id,
        [
            [to_links(ri, ci, cell) for ci, cell in enumerate(row)]
            for ri, row in enumerate(ex.cell_links.data)
        ],
        [to_col(col) for col in ex.table.columns],
        gcore_table.Context(
            None,
            None,
            [],
        ),
    )
