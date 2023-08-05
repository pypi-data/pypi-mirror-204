from collections import defaultdict
import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import List, Literal, Mapping, Optional, Union, Generator, Sequence
from kgdata.wikidata.db import WikidataDB
from kgdata.wikidata.models.wdentity import WDEntity
from ned.actors.db import to_wikidata_db
from ned.data_models.pymodels import CellLink

import numpy as np
from loguru import logger as glogger
from osin.apis.remote_exp import RemoteExpRun
from osin.types import OTable
from osin.types.primitive_type import NestedPrimitiveOutput
from osin.types.pyobject.html import OHTML, OListHTML
from sm.dataset import Example
from sm.misc.ray_helper import enhance_error_info
from sm.namespaces.wikidata import WikidataNamespace
from tqdm.auto import tqdm

import ned.metrics as ned_metrics
from ned.data_models.prelude import (
    DatasetCandidateEntities,
    NEDExample,
    NO_ENTITY,
    NIL_ENTITY,
    CellCandidateEntities,
)


@dataclass
class EvalArgs:
    dsqueries: List[str] = field(
        metadata={"help": "List of dataset queries to evaluate"}
    )
    exprun_type: Literal["cell", "table"] = field(
        default="table",
        metadata={
            "help": "If cell, then each example in Osin is a cell, if table, then each example is a table."
        },
    )
    eval_ignore_nil: bool = field(
        default=True,
        metadata={"help": "If True, ignore NIL entity when evaluating entity linking."},
    )
    eval_ignore_non_entity_cell: bool = field(
        default=True,
        metadata={
            "help": "If True, ignore non-entity cell when evaluating entity linking."
        },
    )


def evaluate(
    entities: Mapping[str, WDEntity],
    examples: List[NEDExample],
    entity_columns: List[List[int]],
    candidates: DatasetCandidateEntities,
    eval_ignore_nil: bool = True,
    eval_ignore_non_entity_cell: bool = True,
    dsname: str = "",
    logger=None,
    exprun: Optional[RemoteExpRun] = None,
    verbose: bool = True,
    report_unique: bool = True,
    exprun_type: Literal["cell", "table"] = "table",
    top_ks: list[int] = [1, 5, 20, 100, 1000],
):
    logger = logger or glogger
    queries, ytrue, ypreds = defaultdict(list), [], []

    for ei, example in enumerate(
        tqdm(
            examples,
            disable=not verbose,
            desc="evaluating" + (" " + dsname if dsname != "" else ""),
        )
    ):
        equery, eytrue, eypreds = evaluate_example(
            example,
            entity_columns[ei],
            candidates,
            eval_ignore_nil,
            eval_ignore_non_entity_cell,
        )
        ytrue.extend(eytrue)
        ypreds.extend(eypreds)

        if exprun is not None:
            if exprun_type == "cell":
                for expex in report_cell_level(
                    example,
                    entity_columns[ei],
                    candidates,
                    eval_ignore_nil,
                    eval_ignore_non_entity_cell,
                ):
                    exprun.update_example_output(**expex)
            elif exprun_type == "table":
                exprun.update_example_output(
                    **report_table_level(
                        entities, ei, example, candidates, eytrue, eypreds, top_ks
                    )
                )

        if report_unique:
            for i, query in enumerate(equery):
                if all(res["entities"] != eytrue[i] for res in queries.get(query, [])):
                    # same query but mapped to different entities, it is a new example
                    queries[query].append(
                        {
                            "entities": eytrue[i],
                            "candidate_ids": eypreds[i],
                        }
                    )

    # sort the candidates by their score (bigger is better)
    recall = ned_metrics.recall(ytrue, ypreds, k=top_ks)
    mrr = ned_metrics.mrr(ytrue, ypreds)
    logger.info(
        "dsname = {} | total = {} | mrr = {:.5f} | metrics: {}",
        dsname,
        len(ytrue),
        mrr,
        json.dumps(recall, indent=4),
    )
    # fmt: off
    logger.info(
        "for copying...\nrun-id\tmrr\t{}\n{}",
        "\t".join(f"{k}"for k in recall.keys()),
        ",".join(
            [str(0 if exprun is None else exprun.id)] +
            ["%.5f" % x for x in [mrr]] +
            ["%.2f" % x for x in recall.values()]
    ))
    # fmt: on

    if report_unique:
        unique_ytrue = []
        unique_ypreds = []
        for res in queries.values():
            for obj in res:
                unique_ytrue.append(obj["entities"])
                unique_ypreds.append(obj["candidate_ids"])

        unique_recall = ned_metrics.recall(unique_ytrue, unique_ypreds, k=top_ks)
        unique_mrr = ned_metrics.mrr(unique_ytrue, unique_ypreds)
        logger.info(
            "unique total = {} | unique mrr = {:.5f} | unique metrics: {}",
            len(unique_ytrue),
            unique_mrr,
            json.dumps(unique_recall, indent=4),
        )
        # fmt: off
        logger.info(
            "for copying...\nrun-id\tmrr\tunique-mrr\t{}\n{}",
            "\t".join(f"uni-{k}"for k in unique_recall.keys()),
            ",".join(
                [str(0 if exprun is None else exprun.id)] +
                ["%.5f" % x for x in [mrr, unique_mrr]] +
                ["%.2f" % x for x in unique_recall.values()]
        ))
        # fmt: on

    if exprun is not None:
        primitive = {
            "total": len(ytrue),
            "mrr": mrr,
            "recall": recall,
        }
        if report_unique:
            primitive.update(
                {
                    "unique_total": len(unique_ytrue),  # type: ignore
                    "unique_mrr": unique_mrr,  # type: ignore
                    "unique_recall": unique_recall,  # type: ignore
                }
            )
        exprun.update_output(
            primitive=primitive,
        )

    return {"recall": recall, "mrr": mrr, "total": len(ytrue)}


def evaluate_example(
    example: NEDExample,
    entity_columns: list[int],
    candidates: DatasetCandidateEntities,
    eval_ignore_nil: bool = True,
    eval_ignore_non_entity_cell: bool = True,
):
    equery = []
    eytrue = []
    eypreds = []

    for ri, ci, link in iter_eval_cell(
        example, entity_columns, eval_ignore_nil, eval_ignore_non_entity_cell
    ):
        if link is None:
            gold_entities = {NO_ENTITY}
        elif len(link.entities) == 0:
            gold_entities = {NIL_ENTITY}
        else:
            gold_entities = set(link.entities)

        query = str(example.table[ri, ci])
        if candidates.has_cell_candidates(example.table.table_id, ri, ci):
            cans = candidates.get_cell_candidates(example.table.table_id, ri, ci)
        else:
            cans = CellCandidateEntities.empty()

        # sort by negative score for stable descending order ([::-1] won't work correctly)
        sortedindex = np.argsort(-cans.score, kind="stable")
        can_ids = cans.id[sortedindex]

        assert len(gold_entities) > 0, "Does not handle NIL yet"
        equery.append(query)
        eytrue.append(gold_entities)
        eypreds.append(can_ids)

    return equery, eytrue, eypreds


def report_cell_level(
    example: NEDExample,
    entity_columns: list[int],
    candidates: DatasetCandidateEntities,
    eval_ignore_nil: bool = True,
    eval_ignore_non_entity_cell: bool = True,
) -> list[dict]:
    exp_examples = []

    for ri, ci, link in iter_eval_cell(
        example, entity_columns, eval_ignore_nil, eval_ignore_non_entity_cell
    ):
        query = str(example.table[ri, ci])

        if link is None:
            gold_entities = {NO_ENTITY}
        elif len(link.entities) == 0:
            gold_entities = {NIL_ENTITY}
        else:
            gold_entities = set(link.entities)

        if candidates.has_cell_candidates(example.table.table_id, ri, ci):
            cans = candidates.get_cell_candidates(example.table.table_id, ri, ci)
        else:
            cans = CellCandidateEntities.empty()

        # sort by negative score for stable descending order ([::-1] won't work correctly)
        sortedindex = np.argsort(-cans.score, kind="stable")

        # each exp example is a cell
        max_rank = max(10000, len(cans) + 100)
        rank = max_rank
        otable = []
        for i, idx in enumerate(sortedindex):
            can_id = cans.id[idx]
            otable.append(
                {
                    "id": can_id,
                    "table": example.table.table_id,
                    "row": ri,
                    "label": str(cans.label[idx]),
                    "score": float(cans.score[idx]),
                    "found": can_id in gold_entities,
                }
            )
            if can_id in gold_entities:
                rank = i + 1

        exp_examples.append(
            {
                "example_id": query.replace("/", "-slash-")
                if query != ""
                else "<empty>",
                "example_name": query,
                "primitive": {
                    "id": " | ".join(gold_entities),
                    "found": rank < max_rank,
                    "rank": rank,
                },
                "complex": {"candidates": OTable(otable)},
            }
        )

    return exp_examples


def report_table_level(
    entities: Mapping[str, WDEntity],
    example_index: int,
    example: NEDExample,
    candidates: DatasetCandidateEntities,
    eytrue: list[set[str]],
    eypreds: list[list[str]],
    top_ks: Sequence[Optional[int]],
) -> dict:

    return {
        "example_id": "%03d" % example_index,
        "example_name": example.table.table_id,
        "primitive": {
            "total": len(eytrue),
            "mrr": ned_metrics.mrr(eytrue, eypreds),
            "recall": ned_metrics.recall(eytrue, eypreds, top_ks),
        },
        "complex": {
            "table": AuxComplexTableObject(entities).get_table(example, candidates),
            "columns": OTable(
                [
                    {
                        "column": example.table.columns[ci].clean_name or "",
                        "column_index": ci,
                        "type_id": ctype.entity,
                        "type_name": entities[ctype.entity].label,
                    }
                    for ci, ctypes in zip(
                        example.entity_columns, example.entity_column_types
                    )
                    for ctype in ctypes
                ]
            ),
        },
    }


def iter_eval_cell(
    example: NEDExample,
    entity_columns: list[int],
    eval_ignore_nil: bool = True,
    eval_ignore_non_entity_cell: bool = True,
) -> Generator[tuple[int, int, Optional[CellLink]], None, None]:
    nrows, ncols = example.cell_links.shape()
    for ci in set(entity_columns).union(example.entity_columns):
        for ri in range(nrows):
            link = example.cell_links[ri, ci]

            if eval_ignore_non_entity_cell and link is None:
                # link is None, the cell is not linked to any entity
                continue

            if eval_ignore_nil and link is not None and len(link.entities) == 0:
                # the cell is linked to NIL entity
                continue

            yield ri, ci, link


class AuxComplexTableObject:
    def __init__(
        self,
        entities: Mapping[str, WDEntity],
    ) -> None:
        self.wdns = WikidataNamespace.create()
        self.entities = entities

    def get_table(
        self, example: NEDExample, ex_candidates: Optional[DatasetCandidateEntities]
    ) -> OTable:
        nrows, ncols = example.table.shape()
        columns = [
            f"{ci}. " + (c.clean_name or "")
            for ci, c in enumerate(example.table.columns)
        ]
        return OTable(
            [
                {
                    columns[ci]: self._get_cell(example, ex_candidates, ri, ci)
                    for ci in range(ncols)
                }
                for ri in range(nrows)
            ]
        )

    def _get_cell(
        self,
        example: NEDExample,
        ex_candidates: Optional[DatasetCandidateEntities],
        row: int,
        col: int,
    ):
        from htbuilder import a, b, code, div, li, pre, span, ul

        cell_link = example.cell_links[row, col]
        if cell_link is None:
            return str(example.table[row, col])

        cell = str(example.table[row, col])
        ent_el = []
        can_el = []

        for entid in cell_link.entities:
            for start, end in cell_link.mentions[entid]:
                x = div(style="margin-left: 8px")(
                    "-&nbsp;",
                    a(href=self.wdns.get_entity_abs_uri(entid))(f"{cell[start:end]}: "),
                    span(
                        a(href=self.wdns.get_entity_abs_uri(entid))(entid),
                    ),
                )
                popx = div(self.get_ent_label_with_description(entid))
                ent_el.append(OHTML(str(x), str(popx)))

        gold_ents = set(cell_link.entities)

        if ex_candidates is not None:
            # showing the top 5 candidates, as longer won't give more info.
            cans = ex_candidates.get_cell_candidates(example.table.table_id, row, col)
            # sort by negative score for stable descending order ([::-1] won't work correctly)
            sortedindex = np.argsort(-cans.score, kind="stable")
            discans = [
                (i, cans.get_candidate_by_index(oi))
                for i, oi in enumerate(sortedindex[:5])
            ]
            if all(can.entity.id not in gold_ents for _, can in discans):
                # add missing pred gold
                discans.extend(
                    [
                        (i, cans.get_candidate_by_index(oi))
                        for i, oi in enumerate(sortedindex)
                        if cans.id[oi] in gold_ents
                    ]
                )

            for i, canid in discans:
                x = div(style="margin-left: 8px")(
                    f"- {i}.&nbsp;",
                    span(
                        "(",
                        code(style="color: green; font-weight: bold")("C"),
                        ")&nbsp;",
                    )
                    if canid.entity.id in gold_ents
                    else "",
                    a(href=self.wdns.get_entity_abs_uri(canid.entity.id))(
                        canid.entity.id
                    ),
                    ": ",
                    span(title=canid.score)(round(canid.score, 4)),
                )
                popx = self.get_ent_label_with_description(canid.entity.id)
                can_el.append(OHTML(str(x), str(popx)))

        items = [
            OHTML(
                str(
                    span(
                        b("Cell: "),
                        cell,
                    )
                ),
            ),
            OHTML(str(b("Ground-truth: "))),
            *ent_el,
            OHTML(str(b("Candidates: "))),
            *can_el,
        ]
        return OListHTML(items)

    def get_ent_label_with_description(self, entid: str):
        if entid not in self.entities:
            return entid
        ent = self.entities[entid]
        return f"{ent.label} ({entid}): {ent.description}"
