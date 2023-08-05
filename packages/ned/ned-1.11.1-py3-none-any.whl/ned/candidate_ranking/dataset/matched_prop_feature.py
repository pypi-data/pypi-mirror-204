from __future__ import annotations
from operator import itemgetter

from grams.algorithm.literal_matchers.literal_match import (
    LiteralMatch,
    LiteralMatchConfigs,
)
from grams.algorithm.literal_matchers.text_parser import TextParser
from kgdata.wikidata.db import WikidataDB
from kgdata.wikidata.models.wdentity import WDEntity
import numpy as np
import ray
from nptyping import NDArray, Object, Shape
from ream.data_model_helper import NumpyDataModel

from ned.data_models.prelude import DatasetCandidateEntities
from ned.data_models.pymodels import NEDExample
from sm.misc.ray_helper import get_instance, ray_map, ray_put


class CRDatasetMatchedProps(NumpyDataModel):
    __slots__ = ["matched_props"]
    # the order of this object is the same as candidates/entities
    # each item is a list of tuple of (prop id, column id, score)
    matched_props: NDArray[Shape["*,*"], Object]

    @staticmethod
    def create(examples: list[NEDExample], candidates: DatasetCandidateEntities):
        example_refs = {ex.table.table_id: ray_put(ex) for ex in examples}
        db_dir_ref = ray_put(WikidataDB.get_instance().database_dir)
        args = []
        for tid, (tstart, tend, tindex) in candidates.index.items():
            for ci, (cstart, cend, cindex) in tindex.items():
                cindex = [
                    (ri, (rstart - cstart, rend - cstart))
                    for ri, (rstart, rend) in cindex.items()
                ]
                args.append(
                    (
                        db_dir_ref,
                        example_refs[tid],
                        ci,
                        candidates.id[cstart:cend],
                        cindex,
                    )
                )

        resp = ray_map(
            match_props.remote,
            args,
            verbose=True,
            desc="matching properties of candidates with other columns",
        )
        arr = np.concatenate([x for x in resp if x.shape[0] > 0], axis=0)
        assert arr.shape[0] == len(candidates)
        return CRDatasetMatchedProps(arr)


@ray.remote
def match_props(
    database_dir,
    example: NEDExample,
    column_index: int,
    column_can_ids: NDArray[Shape["*"], Object],
    cindex: list[tuple[int, tuple[int, int]]],
):
    """Match the properties of entities/candidates with other columns."""
    # gather all the entities in this column
    db = get_instance(
        lambda: WikidataDB(database_dir).wdentities,
        f"ned.candidate_ranking.dataset.wdentities",
    ).cache()
    textparser = TextParser.default()
    literal_match = LiteralMatch(db, LiteralMatchConfigs())

    other_columns = [
        col for j, col in enumerate(example.table.columns) if j != column_index
    ]
    output = []
    for ri, (rstart, rend) in cindex:
        can_ids = column_can_ids[rstart:rend]
        for can_id in can_ids:
            can = db[can_id]
            can_matches = []
            for col in other_columns:
                value = col.values[ri]
                parsed_value = textparser.parse(value)
                matches = value_search(can, literal_match, parsed_value)
                if len(matches) == 0:
                    can_matches.append((None, None, 0.0))
                else:
                    propid, score = max(matches, key=itemgetter(1))
                    can_matches.append((propid, col.index, score))

            can_matched_score = [x[2] for x in can_matches]
            output.append([np.sum(can_matched_score)])

    return np.array(output)


def value_search(ent: WDEntity, literal_match: LiteralMatch, value):
    """Find property/qualifier of an entity that matches the value. If the match one is qualifier, prepend with the property id.

    For now, this function hasn't considered matched qualifiers.
    """
    matches = []
    for p, stmts in ent.props.items():
        if p == "P31":
            # no need to search in the instanceOf property, as the ontology is removed from the databased as they are huge
            continue

        for stmt_i, stmt in enumerate(stmts):
            has_stmt_value = False
            for fn, (match, confidence) in literal_match.match(
                stmt.value, value, skip_unmatch=True
            ):
                matches.append((p, confidence))
                has_stmt_value = True

            for q, qvals in stmt.qualifiers.items():
                for qval in qvals:
                    for fn, (match, confidence) in literal_match.match(
                        qval, value, skip_unmatch=True
                    ):
                        matches.append((f"{p}/{q}", confidence))
    return matches


CRDatasetMatchedProps.init()
