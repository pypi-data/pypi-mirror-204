from __future__ import annotations
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List, Literal, MutableMapping, Optional, cast, overload
from kgdata.wikidata.db import WikidataDB

from ned.candidate_generation.common import CandidateGenerationBasicMethod
from ned.candidate_generation.pyserini.search import PyseriniSearcher
from ned.data_models.prelude import CandidateEntity, Entity


@dataclass
class PyseriniArgs:
    indice_dir: Path
    index_name: str
    limit: int = 1000
    query_types: List[Literal["default", "bow", "fuzzy"]] = field(
        default_factory=lambda: ["default"]
    )


class PyseriniWrapper(CandidateGenerationBasicMethod):
    __doc__ = PyseriniSearcher.__doc__
    VERSION = PyseriniSearcher.VERSION

    def __init__(
        self,
        args: PyseriniArgs,
        db: WikidataDB,
        kvstore: Optional[MutableMapping[str, list[tuple[str, float]]]] = None,
    ):
        super().__init__(db, kvstore, batch_size=512)
        self.args = args
        self.search = PyseriniSearcher(self.args.indice_dir / self.args.index_name)

    @overload
    def get_candidates_by_queries(
        self, queries: list[str], return_provenance: Literal[False] = False
    ) -> dict[str, list[tuple[str, float]]]:
        ...

    @overload
    def get_candidates_by_queries(
        self, queries: list[str], return_provenance: Literal[True]
    ) -> dict[str, list[tuple[str, float, str]]]:
        ...

    def get_candidates_by_queries(
        self, queries: list[str], return_provenance: bool = False
    ) -> dict[str, list[tuple[str, float, str]]] | dict[str, list[tuple[str, float]]]:
        search_res: dict[str, dict[str, tuple[float, str] | float]] = {}
        for query_type in self.args.query_types:
            if query_type == "default":
                subqueries2 = queries
                pre_analyzed = False
            elif query_type == "bow":
                subqueries2 = [
                    self.search.bow_query(query, field="contents") for query in queries
                ]
                pre_analyzed = True
            elif query_type == "fuzzy":
                subqueries2 = [
                    self.search.fuzzy_query(query, field="contents")
                    for query in queries
                ]
                pre_analyzed = True
            else:
                raise ValueError(f"Unknown query type {query_type}")

            res = self.search.batch_search(
                subqueries2, limit=self.args.limit, pre_analyzed=pre_analyzed
            )
            for query, cans in zip(queries, res):
                provenance = f"{self.args.index_name}:{query_type}:"
                if query not in search_res:
                    search_res[query] = {}

                for i, can in enumerate(cans):
                    if return_provenance:
                        search_res[query][can.docid] = (can.score, provenance + str(i))
                    else:
                        search_res[query][can.docid] = can.score
                    # doc = can.doc
                    # search_res[query][can.docid] = CandidateEntity(
                    #     entity=Entity(
                    #         id=can.docid,
                    #         label=doc.label,
                    #         description=doc.description,
                    #         aliases=doc.aliases,
                    #         popularity=doc.popularity,
                    #     ),
                    #     score=can.score,
                    #     provenance=provenance + str(i),
                    # )

        if return_provenance:
            return {
                query: [(k, v[0], v[1]) for k, v in cans.items()]
                for query, cans in cast(
                    dict[str, dict[str, tuple[float, str]]], search_res
                ).items()
            }
        return {
            query: list(cans.items())
            for query, cans in cast(dict[str, dict[str, float]], search_res).items()
        }
