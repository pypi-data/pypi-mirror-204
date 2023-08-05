from __future__ import annotations
import struct
import orjson
from pathlib import Path
from ned.data_models.pymodels import CandidateEntity, Entity
import numpy as np
from nptyping import Float64, NDArray, Shape, UInt32
from nptyping.typing_ import Object
from typing import List, Optional, Tuple, Dict
import pyarrow as pa
import pyarrow.parquet as pq
import lz4.frame


class TableIndex:
    __slots__ = ("index",)

    def __init__(self, index: Dict[str, Tuple[int, int]]):
        self.index = index

    def to_bytes(self):
        return orjson.dumps(self.index)

    @staticmethod
    def from_bytes(d):
        return TableIndex(orjson.loads(d))


class CellIndex:
    __slots__ = ("index",)

    def __init__(
        self,
        index: Dict[str, Dict[int, Dict[int, Tuple[int, int]]]],
    ):
        # table id => col => row => (start, end)
        self.index = index

    def get_column_range(self, table_id: str, col: int) -> Tuple[int, int]:
        it = iter(self.index[table_id][col].values())
        start, end = next(it)
        for new_start, new_end in it:
            if new_start != end:
                raise ValueError("Ranges are not contiguous")
            end = new_end
        return start, end

    def to_bytes(self):
        return orjson.dumps(
            {
                id: [
                    (ci, [(ri, range) for ri, range in tmp2.items()])
                    for ci, tmp2 in tmp1.items()
                ]
                for id, tmp1 in self.index.items()
            }
        )

    @staticmethod
    def from_bytes(d):
        return CellIndex(
            {
                id: {ci: {ri: range for ri, range in tmp2} for ci, tmp2 in tmp1}
                for id, tmp1 in orjson.loads(d).items()
            }
        )


class NumpySubsetCandidateEntities:
    __slots__ = (
        "offset",
        "idx",
        "id",
        "label",
        "description",
        "aliases",
        "popularity",
        "score",
        "provenance",
    )

    def __init__(
        self,
        offset: int,
        idx: NDArray[Shape["*"], UInt32],
        id: NDArray[Shape["*"], Object],
        label: NDArray[Shape["*"], Object],
        description: NDArray[Shape["*"], Object],
        aliases: NDArray[Shape["*"], Object],
        popularity: NDArray[Shape["*"], Float64],
        score: NDArray[Shape["*"], Float64],
        provenance: NDArray[Shape["*"], Object],
    ):
        self.offset = offset
        self.idx = idx
        self.id = id
        self.label = label
        self.description = description
        self.aliases = aliases
        self.popularity = popularity
        self.score = score
        self.provenance = provenance

    def __len__(self):
        return len(self.idx)

    def swap(self, i: int, j: int):
        """Swap the position of two candidate entities at index i and j"""
        for field in [
            self.idx,
            self.id,
            self.label,
            self.description,
            self.aliases,
            self.popularity,
            self.score,
            self.provenance,
        ]:
            field[i], field[j] = field[j], field[i]

    def get_candidate_by_id(self, id: str) -> Optional[CandidateEntity]:
        e = np.argwhere(self.id == id)
        if len(e) == 0:
            return None
        i = e[0, 0]
        return CandidateEntity(
            entity=Entity(
                id=self.id[i],
                label=self.label[i],
                description=self.description[i],
                aliases=self.aliases[i],
                popularity=self.popularity[i],
            ),
            score=self.score[i],
            provenance=self.provenance[i],
        )


class NumpyCandidateEntities:
    __slots__ = (
        "table_index",
        "cell_index",
        "idx",
        "id",
        "label",
        "description",
        "aliases",
        "popularity",
        "score",
        "provenance",
    )

    def __init__(
        self,
        table_index: TableIndex,
        cell_index: CellIndex,
        idx: NDArray[Shape["*"], UInt32],
        id: NDArray[Shape["*"], Object],
        label: NDArray[Shape["*"], Object],
        description: NDArray[Shape["*"], Object],
        aliases: NDArray[Shape["*"], Object],
        popularity: NDArray[Shape["*"], Float64],
        score: NDArray[Shape["*"], Float64],
        provenance: NDArray[Shape["*"], Object],
    ):
        self.table_index = table_index
        self.cell_index = cell_index
        self.idx = idx
        self.id = id
        self.label = label
        self.description = description
        self.aliases = aliases
        self.popularity = popularity
        self.score = score
        self.provenance = provenance

    @classmethod
    def from_py_candidates(
        cls,
        candidates: Dict[str, Dict[int, Dict[int, List[CandidateEntity]]]],
        table_shape: Dict[str, Tuple[int, int]],
    ):
        id = []
        idx = []
        label = []
        description = []
        aliases = []
        popularity = []
        score = []
        provenance = []

        tbl_index = {}
        cell_index = {}
        for table, tmp1 in candidates.items():
            cell_index[table] = {}
            shp = table_shape[table]
            tbl_start = len(id)
            tbl_end = tbl_start
            for col, tmp2 in tmp1.items():
                cell_index[table][col] = {}
                for row, cans in tmp2.items():
                    cell_index[table][col][row] = (len(id), len(id) + len(cans))
                    tbl_end += len(cans)
                    cell_idx = np.ravel_multi_index((row, col), shp)
                    idx.extend([cell_idx] * len(cans))
                    id.extend(c.entity.id for c in cans)
                    label.extend(c.entity.label for c in cans)
                    description.extend(c.entity.description for c in cans)
                    aliases.extend(c.entity.aliases for c in cans)
                    popularity.extend(c.entity.popularity for c in cans)
                    score.extend(c.score for c in cans)
                    provenance.extend(c.provenance for c in cans)

            tbl_index[table] = (tbl_start, tbl_end)

        return cls(
            table_index=TableIndex(tbl_index),
            cell_index=CellIndex(cell_index),
            id=np.array(id, dtype=np.object_),
            idx=np.array(idx, dtype=np.uint32),
            label=np.array(label, dtype=np.object_),
            description=np.array(description, dtype=np.object_),
            aliases=np.array(aliases, dtype=np.object_),
            popularity=np.array(popularity, dtype=np.float64),
            score=np.array(score, dtype=np.float64),
            provenance=np.array(provenance, dtype=np.object_),
        )

    def get_cell_candidates(
        self, table: str, row: int, col: int
    ) -> NumpySubsetCandidateEntities:
        """Get candidate entities of a cell"""
        start, end = self.cell_index.index[table][col][row]
        return NumpySubsetCandidateEntities(
            offset=start,
            idx=self.idx[start:end],
            id=self.id[start:end],
            label=self.label[start:end],
            description=self.description[start:end],
            aliases=self.aliases[start:end],
            popularity=self.popularity[start:end],
            score=self.score[start:end],
            provenance=self.provenance[start:end],
        )

    def get_table_candidates(self, table: str) -> NumpySubsetCandidateEntities:
        """Get candidate entities of a table"""
        start, end = self.table_index.index[table]
        return NumpySubsetCandidateEntities(
            offset=start,
            idx=self.idx[start:end],
            id=self.id[start:end],
            label=self.label[start:end],
            description=self.description[start:end],
            aliases=self.aliases[start:end],
            popularity=self.popularity[start:end],
            score=self.score[start:end],
            provenance=self.provenance[start:end],
        )

    def __len__(self):
        return len(self.idx)

    def get_candidate_by_id(self, id: str) -> Optional[CandidateEntity]:
        e = np.argwhere(self.id == id)
        if len(e) == 0:
            return None
        i = e[0]
        return CandidateEntity(
            entity=Entity(
                id=self.id[i],
                label=self.label[i],
                description=self.description[i],
                aliases=self.aliases[i],
                popularity=self.popularity[i],
            ),
            score=self.score[i],
            provenance=self.provenance[i],
        )

    def swap(self, i: int, j: int):
        """Swap the position of two candidate entities at index i and j"""
        for field in [
            self.idx,
            self.id,
            self.label,
            self.description,
            self.aliases,
            self.popularity,
            self.score,
            self.provenance,
        ]:
            field[i], field[j] = field[j], field[i]

    def replace_score(
        self, score: NDArray[Shape["*"], Float64]
    ) -> NumpyCandidateEntities:
        assert len(score) == len(self.score)
        return NumpyCandidateEntities(
            table_index=self.table_index,
            cell_index=self.cell_index,
            idx=self.idx,
            id=self.id,
            label=self.label,
            description=self.description,
            aliases=self.aliases,
            popularity=self.popularity,
            score=score,
            provenance=self.provenance,
        )

    def save(self, file: Path):
        pq.write_table(
            pa.table(
                {
                    "idx": self.idx,
                    "id": self.id,
                    "label": self.label,
                    "description": self.description,
                    "aliases": self.aliases,
                    "popularity": self.popularity,
                    "score": self.score,
                    "provenance": self.provenance,
                }
            ),
            str(file),
            compression="lz4",
        )

        with lz4.frame.open(
            str(file.parent / (file.stem + ".index.lz4")), mode="wb"
        ) as f:
            tb = self.table_index.to_bytes()
            cb = self.cell_index.to_bytes()

            size = struct.pack("<II", len(tb), len(cb))
            f.write(size)  # type: ignore
            f.write(tb)  # type: ignore
            f.write(cb)  # type: ignore

    @classmethod
    def load(
        cls,
        file: Path,
    ):
        with lz4.frame.open(
            str(file.parent / (file.stem + ".index.lz4")), mode="rb"
        ) as f:
            tb_size, cb_size = struct.unpack("<II", f.read(8))  # type: ignore
            tb = f.read(tb_size)  # type: ignore
            cb = f.read(cb_size)  # type: ignore
            tbl_idx = TableIndex.from_bytes(tb)
            cell_idx = CellIndex.from_bytes(cb)

        tbl = pq.read_table(str(file))
        return cls(
            table_index=tbl_idx,
            cell_index=cell_idx,
            idx=tbl.column("idx").to_numpy(),
            id=tbl.column("id").to_numpy(),
            label=tbl.column("label").to_numpy(),
            description=tbl.column("description").to_numpy(),
            aliases=tbl.column("aliases").to_numpy(),
            popularity=tbl.column("popularity").to_numpy(),
            score=tbl.column("score").to_numpy(),
            provenance=tbl.column("provenance").to_numpy(),
        )
