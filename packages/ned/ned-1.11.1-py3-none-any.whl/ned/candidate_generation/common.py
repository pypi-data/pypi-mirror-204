from __future__ import annotations
import math, orjson
from operator import itemgetter
from ned.actors.db import to_wikidata_db
from pathlib import Path
from kgdata.wikidata.db import WikidataDB
import numpy as np
from abc import ABC, abstractmethod
from collections import MutableMapping, defaultdict
from dataclasses import dataclass
from typing import Dict, Iterable, List, Mapping, Optional

from loguru import logger
from sm.misc.funcs import batch, filter_duplication
from sm.misc.ray_helper import ray_map, ray_put
from tqdm.auto import tqdm
from kgdata.wikidata.models import WDEntity, WDEntityMetadata
from ned.data_models.prelude import (
    CandidateEntity,
    DatasetCandidateEntities,
    NEDExample,
)


class CandidateRankingComplexMethod(ABC):
    """Candidate ranking method that find candidates from a cell and its surrounding context"""

    @abstractmethod
    def get_candidates(
        self,
        examples: List[NEDExample],
        entity_columns: list[list[int]],
    ) -> DatasetCandidateEntities:
        pass


class CandidateGenerationBasicMethod(CandidateRankingComplexMethod):
    """Candidate generation method that find candidates from text"""

    def __init__(
        self,
        db: WikidataDB,
        kvstore: Optional[MutableMapping[str, list[tuple[str, float]]]] = None,
        batch_size: Optional[int] = None,
    ):
        self.db = db

        self.kvstore = kvstore
        self.batch_size = batch_size
        self.logger = logger.bind(name=self.__class__.__name__)

        self.method = self.__class__.__name__

    @abstractmethod
    def get_candidates_by_queries(
        self, queries: List[str]
    ) -> Dict[str, list[tuple[str, float]]]:
        """Generate list of candidate entities for each query."""
        pass

    def get_candidates(
        self, examples: List[NEDExample], entity_columns: list[list[int]]
    ) -> DatasetCandidateEntities:
        self.logger.debug("Create queries")
        queries = set()
        for ei, example in enumerate(examples):
            for ci in entity_columns[ei]:
                for cell in example.table.columns[ci].values:
                    queries.add(str(cell))

        self.logger.debug("find candidates")
        queries = list(queries)
        if self.kvstore is not None:
            original_queries = queries
            queries = [q for q in queries if q not in self.kvstore]
        else:
            original_queries = []

        if self.batch_size is None:
            batch_size = len(queries)
        else:
            batch_size = self.batch_size

        search_results: dict[str, list[tuple[str, float]]] = {}
        with tqdm(total=len(queries), desc="query candidates") as pbar:
            for i in range(0, len(queries), batch_size):
                subqueries = queries[i : i + batch_size]
                batch_search_results = self.get_candidates_by_queries(subqueries)
                if self.kvstore is not None:
                    for q in subqueries:
                        # sort the results by score and ids so that
                        # the order is always deterministic
                        self.kvstore[q] = sorted(
                            batch_search_results[q], key=lambda x: (-x[1], x[0])
                        )
                pbar.update(len(subqueries))

        if self.kvstore is not None:
            with tqdm(
                total=len(original_queries) - len(queries),
                desc="read queries from cache",
            ) as pbar:
                for q in original_queries:
                    if q not in search_results:
                        search_results[q] = self.kvstore[q]
                        pbar.update(1)

        self.logger.debug("find candidates... done! populating the results")
        can_id2index = {}
        for cans in search_results.values():
            for c in cans:
                if c[0] not in can_id2index:
                    can_id2index[c[0]] = len(can_id2index)
        can_labels, can_desc, can_aliases, can_popularity = self.populate(can_id2index)

        self.logger.debug("populating the results... done! creating the output")
        index = {}
        ids = []
        scores = []
        for ei, example in enumerate(examples):
            table_id = example.table.table_id
            tbl_start = len(ids)
            tbl_index = {}
            for ci in entity_columns[ei]:
                col_index = {}
                col_start = len(ids)
                for ri, cell in enumerate(example.table.columns[ci].values):
                    cell = example.table[ri, ci]
                    query = str(cell)
                    query_res = search_results[query]
                    col_index[ri] = (len(ids), len(ids) + len(query_res))
                    ids.extend([c[0] for c in query_res])
                    scores.extend([c[1] for c in query_res])
                tbl_index[ci] = (col_start, len(ids), col_index)
            index[table_id] = (tbl_start, len(ids), tbl_index)

        label = [can_labels[can_id2index[id]] for id in ids]
        description = [can_desc[can_id2index[id]] for id in ids]
        aliases = [can_aliases[can_id2index[id]] for id in ids]
        popularity = [can_popularity[can_id2index[id]] for id in ids]
        provenance = [self.method] * len(ids)

        return DatasetCandidateEntities(
            index=index,
            id=np.array(ids, dtype=np.object_),
            label=np.array(label, dtype=np.object_),
            description=np.array(description, dtype=np.object_),
            aliases=np.array(aliases, dtype=np.object_),
            popularity=np.array(popularity, dtype=np.float64),
            score=np.array(scores, dtype=np.float64),
            provenance=np.array(provenance, dtype=np.object_),
        )

    def populate(self, ids: dict[str, int]):
        dbref = ray_put(self.db.database_dir)
        batch_populated = ray_map(
            populate,
            [(dbref, x) for x in batch(1024, list(ids.keys()))],
            verbose=True,
            desc="populating the results",
            using_ray=True,
            is_func_remote=False,
        )

        label = []
        description = []
        aliases = []
        popularity = []
        for l, d, a, p in batch_populated:
            label.extend(l)
            description.extend(d)
            aliases.extend(a)
            popularity.extend(p)

        return label, description, aliases, popularity


def populate(db: WikidataDB | Path, ids: Iterable[str]):
    db = to_wikidata_db(db)
    entities = db.wdentity_metadata
    entity_popularity = db.wdpagerank

    label = []
    description = []
    aliases = []
    popularity = []

    for id in ids:
        ent = entities[id]

        label.append(ent.label)
        description.append(ent.description)
        aliases.append(orjson.dumps(ent.aliases.flatten()).decode())
        popularity.append(entity_popularity[id])

    return label, description, aliases, popularity
