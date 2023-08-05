from __future__ import annotations

from collections import Sequence
from copy import deepcopy
from typing import Generic, Literal, TypeVar, Optional, Union, Protocol, overload

import numpy as np
from nptyping import Float64, NDArray, Shape, Object
from ream.data_model_helper import (
    NumpyDataModel,
    NumpyDataModelHelper,
    OffsetIndex,
    ContiguousIndexChecker,
)

from ned.data_models.pymodels import CandidateEntity, Entity
from sm.misc.funcs import is_non_decreasing_sequence

# mapping from { row_index => [start, end] }
ColumnIndex = dict[int, tuple[int, int]]
# mapping from { col_index => [start, end, ColumnIndex] }
TableIndex = dict[int, tuple[int, int, ColumnIndex]]
# mapping from: { table_id => [start, end, TableIndex] }
DatasetIndex = dict[str, tuple[int, int, TableIndex]]

I = TypeVar(
    "I",
    DatasetIndex,
    OffsetIndex[TableIndex],
    OffsetIndex[ColumnIndex],
    None,
)


class DatasetGoldEntities(Protocol):
    # mapping from table_id => col_index => row_index => (start, end)
    index: dict[str, dict[int, dict[int, tuple[int, int]]]]
    entity_id: NDArray[Shape["*"], Object]
    entity_label: NDArray[Shape["*"], Object]
    entity_description: NDArray[Shape["*"], Object]
    entity_aliases: NDArray[Shape["*"], Object]
    entity_popularity: NDArray[Shape["*"], Object]


class CandidateEntities(NumpyDataModel, Generic[I]):
    # fmt: off
    __slots__ = ["index", "id", "label", "description", "aliases", "popularity", "score", "provenance"]    
    # fmt: on

    index: I
    id: NDArray[Shape["*"], Object]
    # label of the entity
    label: NDArray[Shape["*"], Object]
    # description of the entity
    description: NDArray[Shape["*"], Object]
    aliases: NDArray[Shape["*"], Object]
    popularity: NDArray[Shape["*"], Float64]
    score: NDArray[Shape["*"], Float64]
    provenance: NDArray[Shape["*"], Object]

    def __init__(
        self,
        index: I,
        id: NDArray[Shape["*"], Object],
        label: NDArray[Shape["*"], Object],
        description: NDArray[Shape["*"], Object],
        aliases: NDArray[Shape["*"], Object],
        popularity: NDArray[Shape["*"], Float64],
        score: NDArray[Shape["*"], Float64],
        provenance: NDArray[Shape["*"], Object],
    ):
        self.index = index
        self.id = id
        self.label = label
        self.description = description
        self.aliases = aliases
        self.popularity = popularity
        self.score = score
        self.provenance = provenance

    def get_candidate_by_id(self, id: str):
        e = np.argwhere(self.id == id)
        if len(e) == 0:
            return None
        # because e has shape (N, (self.id == id).ndim)
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

    def get_candidate_by_index(self, i: int) -> CandidateEntity:
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


class DatasetCandidateEntities(CandidateEntities[DatasetIndex]):
    index: DatasetIndex

    @classmethod
    def from_pymodel_candidates(
        cls,
        candidates: dict[str, dict[int, dict[int, list[CandidateEntity]]]],
    ):
        id = []
        label = []
        description = []
        aliases = []
        popularity = []
        score = []
        provenance = []

        index = {}
        for table, table_index in candidates.items():
            index[table] = {}
            tbl_start = len(id)
            for col, col_index in table_index.items():
                index[table][col] = {}
                col_start = len(id)
                for row, cans in col_index.items():
                    index[table][col][row] = (len(id), len(id) + len(cans))
                    id.extend(c.entity.id for c in cans)
                    label.extend(c.entity.label for c in cans)
                    description.extend(c.entity.description for c in cans)
                    aliases.extend(c.entity.aliases for c in cans)
                    popularity.extend(c.entity.popularity for c in cans)
                    score.extend(c.score for c in cans)
                    provenance.extend(c.provenance for c in cans)
                index[table][col] = (col_start, len(id), index[table][col])
            index[table] = (tbl_start, len(id), index[table])

        return cls(
            index=index,
            id=np.array(id, dtype=np.object_),
            label=np.array(label, dtype=np.object_),
            description=np.array(description, dtype=np.object_),
            aliases=np.array(aliases, dtype=np.object_),
            popularity=np.array(popularity, dtype=np.float64),
            score=np.array(score, dtype=np.float64),
            provenance=np.array(provenance, dtype=np.object_),
        )

    @classmethod
    def from_npmodel_candidates(
        cls, candidates: dict[str, dict[int, dict[int, CellCandidateEntities]]]
    ):
        index = {}

        id = []
        label = []
        description = []
        aliases = []
        popularity = []
        score = []
        provenance = []

        len_id = 0
        for table, table_index in candidates.items():
            index[table] = {}
            tbl_start = len_id
            for col, col_index in table_index.items():
                index[table][col] = {}
                col_start = len_id
                for row, cans in col_index.items():
                    index[table][col][row] = (len_id, len_id + len(cans))
                    id.append(cans.id)
                    label.append(cans.label)
                    description.append(cans.description)
                    aliases.append(cans.aliases)
                    popularity.append(cans.popularity)
                    score.append(cans.score)
                    provenance.append(cans.provenance)
                    len_id += len(cans)
                index[table][col] = (col_start, len_id, index[table][col])
            index[table] = (tbl_start, len_id, index[table])

        return cls(
            index=index,
            id=np.concatenate(id, axis=0),
            label=np.concatenate(label, axis=0),
            description=np.concatenate(description, axis=0),
            aliases=np.concatenate(aliases, axis=0),
            popularity=np.concatenate(popularity, axis=0),
            score=np.concatenate(score, axis=0),
            provenance=np.concatenate(provenance, axis=0),
        )

    @staticmethod
    def from_table_candidates(candidates: dict[str, TableCandidateEntities]):
        index = {}
        lst = []
        start = 0
        for table_id, table_cans in candidates.items():
            lst.append(table_cans)
            index[table_id] = (
                start,
                start + len(table_cans),
                NumpyDataModelHelper.offset_index(table_cans.index.index, start),
            )
            start += len(table_cans)
        ds = DatasetCandidateEntities(
            index=index,
            id=np.concatenate([c.id for c in lst]),
            label=np.concatenate([c.label for c in lst]),
            description=np.concatenate([c.description for c in lst]),
            aliases=np.concatenate([c.aliases for c in lst]),
            popularity=np.concatenate([c.popularity for c in lst]),
            score=np.concatenate([c.score for c in lst]),
            provenance=np.concatenate([c.provenance for c in lst]),
        )
        assert ds.score.shape == ds.id.shape, (ds.score.shape, ds.id.shape)
        return ds

    def get_row_index(self):
        row_index = np.zeros_like(self.id, dtype=np.int32)
        for tstart, tend, tindex in self.index.values():
            for cstart, cend, cindex in tindex.values():
                for ri, (rstart, rend) in cindex.items():
                    row_index[rstart:rend] = ri
        return row_index

    def has_cell_candidates(self, table: str, row: int, col: int) -> bool:
        return (
            table in self.index
            and col in self.index[table][2]
            and row in self.index[table][2][col][2]
        )

    def get_cell_candidates(self, table: str, row: int, col: int):
        start, end = self.index[table][2][col][2][row]
        return CellCandidateEntities(
            None,
            self.id[start:end],
            self.label[start:end],
            self.description[start:end],
            self.aliases[start:end],
            self.popularity[start:end],
            self.score[start:end],
            self.provenance[start:end],
        )

    def get_column_candidates(self, table: str, col: int):
        start, end, cindex = self.index[table][2][col]
        return ColumnCandidateEntities(
            OffsetIndex(cindex, start),
            self.id[start:end],
            self.label[start:end],
            self.description[start:end],
            self.aliases[start:end],
            self.popularity[start:end],
            self.score[start:end],
            self.provenance[start:end],
        )

    def get_table_candidates(self, table: str):
        start, end, tindex = self.index[table]
        return TableCandidateEntities(
            OffsetIndex(tindex, start),
            self.id[start:end],
            self.label[start:end],
            self.description[start:end],
            self.aliases[start:end],
            self.popularity[start:end],
            self.score[start:end],
            self.provenance[start:end],
        )

    @overload
    def top_k_candidates(
        self,
        k: int,
        gold_ents: Optional[
            Union[DatasetGoldEntities, dict[str, dict[int, dict[int, list[Entity]]]]]
        ] = None,
        return_index_remap: Literal[False] = False,
        remove_nil_entity: bool = False,
    ) -> DatasetCandidateEntities:
        ...

    @overload
    def top_k_candidates(
        self,
        k: int,
        gold_ents: Optional[
            Union[DatasetGoldEntities, dict[str, dict[int, dict[int, list[Entity]]]]]
        ] = None,
        return_index_remap: Literal[True] = True,
        remove_nil_entity: bool = False,
    ) -> tuple[DatasetCandidateEntities, np.ndarray]:
        ...

    def top_k_candidates(
        self,
        k: int,
        gold_ents: Optional[
            Union[DatasetGoldEntities, dict[str, dict[int, dict[int, list[Entity]]]]]
        ] = None,
        return_index_remap: bool = False,
        remove_nil_entity: bool = False,
    ):
        """Keep top K candidates for each cell based on the score. To customize the score, use
        the replace method, which returns a shallow copy of the dataset.

        Args:
            k: number of candidates per cell to keep.
            gold_ents: (optional) a dictionary of missing gold entities for each cell. If provided, will be added to
                the candidates if missing. The dictionary is of the form {table: {col: {row: [Entity]}}}.
            return_index_map: whether to return an array has the same shape of the new dataset and contains indices of the
                old elements, so that we can map between old elements and new elements. For each item where the new element
                is added from gold_ents, the value will be -1. This is useful when we want to reuse some data that is aligned
                with the old dataset.
            remove_nil_entity: whether to remove the NIL entity from the candidates. Applicable only when gold_ents is provided

        Returns:
            A new dataset with top K candidates per cell.
            (optionally) index maps of candidates
        """
        newindex = {}
        newid = []
        newlabel = []
        newdescription = []
        newaliases = []
        newpopularity = []
        newscore = []
        newprovenance = []

        tbloffset = 0
        coloffset = 0
        count = 0

        idx_map = []

        for table, (tstart, tend, tindex) in self.index.items():
            newtindex = {}
            for ci, (cstart, cend, cindex) in tindex.items():
                newcindex = {}
                for ri, (rstart, rend) in cindex.items():
                    sortedindex = np.argsort(-self.score[rstart:rend], kind="stable")
                    sortedindex = sortedindex[:k] + rstart

                    newid.append(self.id[sortedindex])
                    newlabel.append(self.label[sortedindex])
                    newdescription.append(self.description[sortedindex])
                    newaliases.append(self.aliases[sortedindex])
                    newpopularity.append(self.popularity[sortedindex])
                    newscore.append(self.score[sortedindex])
                    newprovenance.append(self.provenance[sortedindex])

                    if gold_ents is not None:
                        if isinstance(gold_ents, dict):
                            ents = gold_ents[table][ci][ri]
                            entids = {e.id for e in ents}
                            n = len(ents)
                            if all(x not in entids for x in newid[-1]) and n > 0:
                                if len(newid[-1]) < n:
                                    # not enough candidates, the gold entities replace all candidates and add new ones
                                    newid[-1] = np.empty(n, dtype=self.id.dtype)
                                    newlabel[-1] = np.empty(n, dtype=self.label.dtype)
                                    newdescription[-1] = np.empty(
                                        n, dtype=self.description.dtype
                                    )
                                    newaliases[-1] = np.empty(
                                        n, dtype=self.aliases.dtype
                                    )
                                    newpopularity[-1] = np.empty(
                                        n, dtype=self.popularity.dtype
                                    )
                                    newscore[-1] = np.empty(n, dtype=self.score.dtype)
                                    newprovenance[-1] = np.empty(
                                        n, dtype=self.provenance.dtype
                                    )
                                    sortedindex = np.empty(n, dtype=sortedindex.dtype)

                                # correct entity not found, replace the last entities with the gold entities
                                newid[-1][-n:] = [e.id for e in ents]
                                newlabel[-1][-n:] = [e.label for e in ents]
                                newdescription[-1][-n:] = [e.description for e in ents]
                                newaliases[-1][-n:] = [e.aliases for e in ents]
                                newpopularity[-1][-n:] = [e.popularity for e in ents]
                                newscore[-1][-n:] = 0.0
                                newprovenance[-1][-n:] = "oracle"
                                sortedindex[-n:] = -1
                        else:
                            erstart, erend = gold_ents.index[table][ci][ri]
                            entids = gold_ents.entity_id[erstart:erend]
                            n = len(entids)
                            if not np.any(np.isin(newid[-1], entids)) and n > 0:
                                if len(newid[-1]) < n:
                                    # not enough candidates, the gold entities replace all candidates and add new ones
                                    newid[-1] = np.empty(n, dtype=self.id.dtype)
                                    newlabel[-1] = np.empty(n, dtype=self.label.dtype)
                                    newdescription[-1] = np.empty(
                                        n, dtype=self.description.dtype
                                    )
                                    newaliases[-1] = np.empty(
                                        n, dtype=self.aliases.dtype
                                    )
                                    newpopularity[-1] = np.empty(
                                        n, dtype=self.popularity.dtype
                                    )
                                    newscore[-1] = np.empty(n, dtype=self.score.dtype)
                                    newprovenance[-1] = np.empty(
                                        n, dtype=self.provenance.dtype
                                    )
                                    sortedindex = np.empty(n, dtype=sortedindex.dtype)
                                # correct entity not found, replace the last entities with the gold entities
                                newid[-1][-n:] = entids
                                newlabel[-1][-n:] = gold_ents.entity_label[
                                    erstart:erend
                                ]
                                newdescription[-1][-n:] = gold_ents.entity_description[
                                    erstart:erend
                                ]
                                newaliases[-1][-n:] = gold_ents.entity_aliases[
                                    erstart:erend
                                ]
                                newpopularity[-1][-n:] = gold_ents.entity_popularity[
                                    erstart:erend
                                ]
                                newscore[-1][-n:] = 0.0
                                newprovenance[-1][-n:] = "oracle"
                                sortedindex[-n:] = -1

                        if n == 0 and remove_nil_entity:
                            # there is no gold entity for this cell, and NIL entity is removed
                            newid.pop()
                            newlabel.pop()
                            newdescription.pop()
                            newaliases.pop()
                            newpopularity.pop()
                            newscore.pop()
                            newprovenance.pop()
                            continue

                    if return_index_remap:
                        idx_map.append(sortedindex)
                    newcindex[ri] = (count, count + len(newid[-1]))
                    count += len(newid[-1])

                newtindex[ci] = (coloffset, count, newcindex)
                coloffset = count
            newindex[table] = (tbloffset, count, newtindex)
            tbloffset = count

        newds = DatasetCandidateEntities(
            newindex,
            np.concatenate(newid),
            np.concatenate(newlabel),
            np.concatenate(newdescription),
            np.concatenate(newaliases),
            np.concatenate(newpopularity),
            np.concatenate(newscore),
            np.concatenate(newprovenance),
        )

        if return_index_remap:
            return newds, np.concatenate(idx_map)
        return newds

    def select(self, table: Union[str, list[str]]):
        """Select candidates of a single table or multiple tables.
        If passing multiple tables, they must be consecutive in the dataset.
        """
        if isinstance(table, str):
            tables = [table]
            # could do [:2] but type checker complains
            start, end = (tmp := self.index[table])[0], tmp[1]
        else:
            tables = table
            if len(tables) == 0:
                raise ValueError("No tables passed")

            # verify that the tables are consecutive
            checker = ContiguousIndexChecker(self.index[tables[0]][0])
            for table in tables:
                # could do [:2] but type checker complains
                start, end = (tmp := self.index[table])[0], tmp[1]
                checker.next(start, end)

            start = self.index[tables[0]][0]
            end = self.index[tables[-1]][1]

        newindex = {
            table: (
                (tres := self.index[table])[0] - start,
                tres[1] - start,
                {
                    ci: (
                        cstart - start,
                        cend - start,
                        {
                            ri: (rstart - start, rend - start)
                            for ri, (rstart, rend) in cindex.items()
                        },
                    )
                    for ci, (cstart, cend, cindex) in tres[2].items()
                },
            )
            for table in tables
        }

        return DatasetCandidateEntities(
            newindex,
            self.id[start:end],
            self.label[start:end],
            self.description[start:end],
            self.aliases[start:end],
            self.popularity[start:end],
            self.score[start:end],
            self.provenance[start:end],
        )


class TableCandidateEntities(CandidateEntities[OffsetIndex[TableIndex]]):
    index: OffsetIndex[TableIndex]

    def get_column_candidates(self, col: int):
        start, end, cindex = self.index.index[col]
        start -= self.index.offset
        end -= self.index.offset
        return ColumnCandidateEntities(
            OffsetIndex(cindex, start),
            self.id[start:end],
            self.label[start:end],
            self.description[start:end],
            self.aliases[start:end],
            self.popularity[start:end],
            self.score[start:end],
            self.provenance[start:end],
        )

    def has_cell_candidates(self, row: int, col: int) -> bool:
        return col in self.index.index and row in self.index.index[col][2]

    def get_cell_candidates(self, row: int, col: int):
        start, end = self.index.index[col][2][row]
        start -= self.index.offset
        end -= self.index.offset
        return CellCandidateEntities(
            None,
            self.id[start:end],
            self.label[start:end],
            self.description[start:end],
            self.aliases[start:end],
            self.popularity[start:end],
            self.score[start:end],
            self.provenance[start:end],
        )

    @staticmethod
    def from_cell_candidates(
        cell_cans: dict[int, dict[int, CellCandidateEntities]]
    ) -> TableCandidateEntities:
        index = {}
        start = 0
        lst = []

        for ci in cell_cans:
            col_start = start
            col_index = {}

            cindex = cell_cans[ci]
            for ri in cindex:
                cans = cindex[ri]
                lst.append(cans)
                col_index[ri] = (start, start + len(cans))
                start += len(cans)
            index[ci] = (col_start, start, col_index)
        return TableCandidateEntities(
            OffsetIndex(index, 0),
            id=np.concatenate([cans.id for cans in lst]),
            label=np.concatenate([cans.label for cans in lst]),
            description=np.concatenate([cans.description for cans in lst]),
            aliases=np.concatenate([cans.aliases for cans in lst]),
            popularity=np.concatenate([cans.popularity for cans in lst]),
            score=np.concatenate([cans.score for cans in lst]),
            provenance=np.concatenate([cans.provenance for cans in lst]),
        )


class ColumnCandidateEntities(CandidateEntities[OffsetIndex[ColumnIndex]]):
    index: OffsetIndex[ColumnIndex]

    def get_cell_candidates(self, row: int):
        start, end = self.index.index[row]
        start -= self.index.offset
        end -= self.index.offset
        return CellCandidateEntities(
            None,
            self.id[start:end],
            self.label[start:end],
            self.description[start:end],
            self.aliases[start:end],
            self.popularity[start:end],
            self.score[start:end],
            self.provenance[start:end],
        )


class CellCandidateEntities(CandidateEntities[None]):
    index: None

    @staticmethod
    def empty():
        return CellCandidateEntities(
            None,
            np.empty(0, dtype=np.object_),
            np.empty(0, dtype=np.object_),
            np.empty(0, dtype=np.object_),
            np.empty(0, dtype=np.object_),
            np.empty(0, dtype=np.float64),
            np.empty(0, dtype=np.float64),
            np.empty(0, dtype=np.object_),
        )

    def select(self, items: Sequence[int]) -> CellCandidateEntities:
        return CellCandidateEntities(
            None,
            self.id[items],
            self.label[items],
            self.description[items],
            self.aliases[items],
            self.popularity[items],
            self.score[items],
            self.provenance[items],
        )


DatasetCandidateEntities.init()
TableCandidateEntities._metadata = deepcopy(DatasetCandidateEntities._metadata)
ColumnCandidateEntities._metadata = deepcopy(DatasetCandidateEntities._metadata)
CellCandidateEntities.init()
