from __future__ import annotations
from collections import Counter
import functools
import os
from dataclasses import dataclass
from pathlib import Path
from typing import List, Optional, Union

from ned.candidate_generation.pyserini.configuration import (
    PyseriniConfiguration,
    IndexSettings,
)
from ned.candidate_generation.pyserini.document import LuceneDocument
import orjson
from pyserini.search.lucene import LuceneSearcher
from pyserini.search.lucene._searcher import JArrayList
from pyserini.search import JQuery
from pyserini.search.lucene.querybuilder import (
    JBoostQuery,
    JTermQuery,
    autoclass,
    JTerm,
    Analyzer,
    get_lucene_analyzer,
    get_boolean_query_builder,
    JBooleanClauseOccur,
)
import serde.json


FuzzyQuery = autoclass("org.apache.lucene.search.FuzzyQuery")
SpanNearQuery = autoclass("org.apache.lucene.search.spans.SpanNearQuery")
SpanMultiTermQueryWrapper = autoclass(
    "org.apache.lucene.search.spans.SpanMultiTermQueryWrapper"
)


class PyseriniSearcher:
    """Searching for entities using Lucene's index."""

    """CHANGELOG:
    - 101: update search return type to include the original lucene document
    """
    VERSION = "101"

    def __init__(
        self, index: Union[str, Path], cfg: Optional[PyseriniConfiguration] = None
    ):
        self.index_dir = Path(index)
        self.searcher = LuceneSearcher(str(index))
        self.index_settings = IndexSettings.from_dict(
            serde.json.deser(self.index_dir / "_SUCCESS")
        )
        self.cfg = cfg or PyseriniConfiguration.get_instance()
        self.searcher.set_bm25(self.cfg.bm25_k1, self.cfg.bm25_b)
        self.analyzer = self.index_settings.get_analyzer()
        self.lucene_analyzer = Analyzer(get_lucene_analyzer())
        n_processes = os.cpu_count()
        assert isinstance(n_processes, int)
        self.n_processes = n_processes

    def search(
        self, query: Union[str, JQuery], limit: int = 10, pre_analyzed: bool = False
    ) -> List[SearchReturnType]:
        if not pre_analyzed:
            query = self.analyzer(query)
        res = self.searcher.search(query, k=limit)
        return [
            SearchReturnType(
                docid=x.docid, score=x.score, docraw=x.raw, contents=x.contents
            )
            for x in res
        ]

    def batch_search(
        self,
        queries: List[Union[str, JQuery]],
        limit: int = 10,
        pre_analyzed: bool = False,
    ) -> List[List[SearchReturnType]]:
        if not pre_analyzed:
            queries = [self.analyzer(query) for query in queries]

        query_ids = [str(i) for i in range(len(queries))]

        if len(queries) > 0 and isinstance(queries[0], str):
            pyserini_result = self.searcher.batch_search(
                queries, query_ids, k=limit, threads=self.n_processes
            )
        else:
            # ====================================
            # code of pyserini._search
            query_strings = JArrayList()
            qid_strings = JArrayList()
            for query in queries:
                query_strings.add(query)
            for qid in query_ids:
                qid_strings.add(qid)

            results = self.searcher.object.batchSearchWithQueries(
                query_strings, qid_strings, limit, self.n_processes
            )
            pyserini_result = {
                r.getKey(): r.getValue() for r in results.entrySet().toArray()
            }
            # ====================================

        return [
            [
                SearchReturnType(
                    docid=x.docid, score=x.score, docraw=x.raw, contents=x.contents
                )
                for x in pyserini_result[qid]
            ]
            for qid in query_ids
        ]

    def analyze(self, text: str):
        return self.analyzer(text)

    def __getstate__(self):
        return {"index_dir": self.index_dir}

    def __setstate__(self, state):
        self.__init__(state["index_dir"])

    def bow_query(self, query: str, field: str) -> str:
        """Generate a default bag-of-words query in Pyserini"""
        query = self.analyzer(query)
        terms = Counter(self.lucene_analyzer.analyze(query))

        builder = get_boolean_query_builder()
        for term, freq in terms.items():
            q = JBoostQuery(JTermQuery(JTerm(field, term)), freq)
            builder.add(q, JBooleanClauseOccur.should.value)
        return builder.build()

    def fuzzy_query(self, query: str, field: str) -> JQuery:
        """Generate a fuzzy query"""
        query = self.analyzer(query)
        terms = self.lucene_analyzer.analyze(query)

        # using SpanNearQuery as suggested by https://stackoverflow.com/questions/18100233/lucene-fuzzy-search-on-a-phrase-fuzzyquery-spanquery
        # does not work for Mount Eveest
        # clauses = []
        # for term in terms:
        #     c = FuzzyQuery(JTerm(field, term), 2)
        #     c = SpanMultiTermQueryWrapper(c)
        #     clauses.append(c)
        # return SpanNearQuery(clauses, 0, False)

        builder = get_boolean_query_builder()
        for term in terms:
            c = FuzzyQuery(JTerm(field, term), 2)
            builder.add(c, JBooleanClauseOccur.should.value)
        return builder.build()


@dataclass
class SearchReturnType:
    """A placeholder for the return type of the search function."""

    docid: str
    score: float
    docraw: str
    contents: str

    @functools.cached_property
    def doc(self) -> LuceneDocument:
        return LuceneDocument.from_dict(orjson.loads(self.docraw))
