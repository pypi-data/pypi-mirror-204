from __future__ import annotations
from dataclasses import dataclass

from ned.candidate_generation.pyserini.analyzer import (
    AnalyzerType,
    DefaultEnglishAnalyzer,
    TrigramAnalyzer,
)


_PyseriniConfiguration = None


@dataclass
class PyseriniConfiguration:
    # by default, we are using bm25 similarity, below is its default parameters
    bm25_k1: float = 1.2
    bm25_b: float = 0.75

    @staticmethod
    def get_instance():
        global _PyseriniConfiguration
        if _PyseriniConfiguration is None:
            _PyseriniConfiguration = PyseriniConfiguration()
        return _PyseriniConfiguration

    def to_dict(self) -> dict:
        return {
            "version": 1,
            "bm25.k1": self.bm25_k1,
            "bm25.b": self.bm25_b,
        }

    @staticmethod
    def from_dict(o: dict) -> PyseriniConfiguration:
        assert o["version"] == 1
        return PyseriniConfiguration(
            bm25_k1=o["bm25.k1"],
            bm25_b=o["bm25.b"],
        )


@dataclass(eq=True)
class IndexSettings:
    analyzer: AnalyzerType = AnalyzerType.TrigramAnalyzer

    def get_analyzer(self):
        if self.analyzer == AnalyzerType.DefaultEnglishAnalyzer:
            return DefaultEnglishAnalyzer
        if self.analyzer == AnalyzerType.TrigramAnalyzer:
            return TrigramAnalyzer()
        raise NotImplementedError(f"Analyzer type {self.analyzer} is not implemented")

    def to_dict(self) -> dict:
        return {
            "version": 1,
            "analyzer": self.analyzer.value,
        }

    @staticmethod
    def from_dict(o: dict) -> IndexSettings:
        assert o["version"] == 1
        return IndexSettings(analyzer=AnalyzerType(o["analyzer"]))
