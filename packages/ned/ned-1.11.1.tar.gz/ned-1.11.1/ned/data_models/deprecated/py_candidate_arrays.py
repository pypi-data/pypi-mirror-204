from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List, Tuple

from ned.data_models.prelude import CandidateEntity
from sm.misc import deserialize_jl, serialize_jl


@dataclass
class PyCellCandidateEntities:
    candidates: List[CandidateEntity]

    @property
    def id(self):
        return [can.entity.id for can in self.candidates]


class PyCandidateEntities:
    __slots__ = ["candidates"]

    def __init__(
        self, candidates: Dict[str, Dict[int, Dict[int, List[CandidateEntity]]]]
    ):
        self.candidates = candidates

    @staticmethod
    def from_py_candidates(
        candidates: Dict[str, Dict[int, Dict[int, List[CandidateEntity]]]],
        table_shape: Dict[str, Tuple[int, int]],
    ) -> PyCandidateEntities:
        return PyCandidateEntities(candidates)

    def get_cell_candidates(
        self, table: str, row: int, col: int
    ) -> PyCellCandidateEntities:
        """Get candidate entities of a cell"""
        return PyCellCandidateEntities(self.candidates[table][col][row])

    def save(self, path):
        lst = []
        for tbl, tmp1 in self.candidates.items():
            for col, tmp2 in tmp1.items():
                for row, cans in tmp2.items():
                    lst.append((tbl, col, row, [c.to_dict() for c in cans]))
        serialize_jl(lst, path)

    @staticmethod
    def load(path):
        candidates = {}
        for tbl, col, row, cans in deserialize_jl(path):
            if tbl not in candidates:
                candidates[tbl] = {}
            if col not in candidates[tbl]:
                candidates[tbl][col] = {}
            candidates[tbl][col][row] = [CandidateEntity.from_dict(c) for c in cans]
        return PyCandidateEntities(candidates)
