from __future__ import annotations
from copy import deepcopy

from dataclasses import dataclass
from typing import Any, cast
from typing_extensions import Self
from ned.candidate_generation.pyserini.document import StringEncoder

from sm.inputs.table import ColumnBasedTable
from sm.inputs.link import WIKIDATA_NIL_ENTITY, EntityId
from sm.misc.matrix import Matrix
from sm.outputs.semantic_model import SemanticModel
from kgdata.wikidata.models.multilingual import MultiLingualStringList


ALIAS_SEP_TOKEN = "\n"
ESCAPE_ALIAS_SEP_TOKEN = "\\-n"
NIL_ENTITY = str(WIKIDATA_NIL_ENTITY)  # Q0 -- NIL entity, does not exist in Wikidata
assert NIL_ENTITY == "Q0"
NO_ENTITY = "Q-1"  # no entity, used for cells that are not entities such as numbers


@dataclass
class Entity:
    id: str
    # information of the entity itself embedded so that
    # we do not need to query the entity database again
    label: str | None = None
    description: str | None = None
    aliases: str | None = None
    popularity: float | None = None

    def to_tuple(self):
        return (
            self.id,
            self.label,
            self.description,
            self.aliases,
            self.popularity,
        )

    @staticmethod
    def from_tuple(t):
        return Entity(*t)

    def to_dict(self):
        return {
            "id": self.id,
            "label": self.label,
            "description": self.description,
            "aliases": self.aliases,
            "popularity": self.popularity,
        }

    @staticmethod
    def from_dict(d):
        return Entity(**d)

    @staticmethod
    def encode_aliases(aliases: MultiLingualStringList):
        values = aliases.lang2values[aliases.lang]
        assert all(ESCAPE_ALIAS_SEP_TOKEN not in v for v in values), values
        return ALIAS_SEP_TOKEN.join(
            value.replace(ALIAS_SEP_TOKEN, ESCAPE_ALIAS_SEP_TOKEN) for value in values
        )

    @staticmethod
    def decode_aliases(aliases: str) -> list:
        return [
            v.replace(ESCAPE_ALIAS_SEP_TOKEN, ALIAS_SEP_TOKEN)
            for v in aliases.split(ALIAS_SEP_TOKEN)
        ]

    def iter_names(self):
        yield self.label
        assert self.aliases is not None
        for alias in self.decode_aliases(self.aliases):
            yield alias

    def __str__(self):
        return f"{self.label} ({self.id})"


@dataclass
class CandidateEntity:
    entity: Entity
    # score of the candidate entity
    score: float
    # method to retrieve the candidate entity
    provenance: str = ""

    def to_dict(self):
        return {
            "entity": self.entity.to_tuple(),
            "score": self.score,
            "provenance": self.provenance,
        }

    @classmethod
    def from_dict(cls, d: dict):
        d["entity"] = Entity.from_tuple(d["entity"])
        return cls(**d)


@dataclass
class CellLink:
    # if the cell is not linked any entity, self is None
    # if the cell does linked to an entity, but the list is empty, it means
    # the cell is linked to NIL.
    entities: list[EntityId]
    # mapping from entity id to the range (exclusive), a cell may appear multiple times
    mentions: dict[str, list[tuple[int, int]]]

    def to_dict(self):
        return {
            "mentions": [
                (k, v[0], v[1]) for k, vs in self.mentions.items() for v in vs
            ],
            "entities": [e.to_dict() for e in self.entities],
        }

    @classmethod
    def from_dict(cls, d):
        mentions = {}
        for k, s, e in d["mentions"]:
            if k not in mentions:
                mentions[k] = []
            mentions[k].append((s, e))
        return cls(
            [EntityId.from_dict(e) for e in d["entities"]],
            mentions,
        )


@dataclass
class EntityWithScore:
    entity: EntityId
    score: float  # a normalized score from 0 to 1

    def to_dict(self):
        return {
            "entity": self.entity.to_dict(),
            "score": self.score,
        }

    @classmethod
    def from_dict(cls, d):
        return cls(
            EntityId.from_dict(d["entity"]),
            d["score"],
        )


@dataclass
class NEDExample:
    table: ColumnBasedTable
    # list of columns that are entity columns (size != #columns)
    entity_columns: list[int]
    # list of types of entity columns, corresponding with entity_columns (size != #columns)
    # a column can have more than 1 type, and also with a score to specify the confidence or preference
    entity_column_types: list[list[EntityWithScore]]
    # (row, col) -> cell link (can have more than one entity)
    cell_links: Matrix[CellLink | None]
    # list of columns that should be entity columns but are not linked to any entities (size != #columns)
    # for example: column position is linked with an object property (played position) but the values are text not
    # links in Wikipedia. Hence, the auto-label algorithm misses this column.
    should_be_entity_columns: list[int]

    def to_dict(self):
        return {
            "table": self.table.to_dict(),
            "entity_columns": self.entity_columns,
            "entity_column_types": [
                [e.to_dict() for e in ents] for ents in self.entity_column_types
            ],
            "cell_links": [
                [l.to_dict() if l is not None else None for l in row]
                for row in self.cell_links.data
            ],
            "should_be_entity_columns": self.should_be_entity_columns,
        }

    @classmethod
    def from_dict(cls, obj: dict) -> Self:
        obj["table"] = ColumnBasedTable.from_dict(obj["table"])
        obj["entity_column_types"] = [
            [EntityWithScore.from_dict(e) for e in ents]
            for ents in obj["entity_column_types"]
        ]
        obj["cell_links"] = Matrix(
            [
                [CellLink.from_dict(l) if l is not None else None for l in row]
                for row in obj["cell_links"]
            ]
        )
        return cls(**obj)

    def keep_columns(self, columns: list[int]):
        """Keep only the entities in the given columns. This allow us to evaluate/predict a subset of the columns."""
        entity_columns = []
        entity_column_types = []

        set_columns = set(columns)
        for ec in self.entity_columns:
            if ec in set_columns:
                entity_columns.append(ec)
        entity_columns = [ec for ec in self.entity_columns if ec in set_columns]
        entity_column_types = [
            ect if ec in set_columns else []
            for ec, ect in enumerate(self.entity_column_types)
        ]

        cell_links = self.cell_links.shallow_copy()
        for row in cell_links.data:
            for ci in range(len(row)):
                if ci not in set_columns:
                    row[ci] = None

        should_be_entity_columns = [
            ec for ec in self.should_be_entity_columns if ec in set_columns
        ]

        return NEDExample(
            self.table,
            entity_columns,
            entity_column_types,
            cell_links,
            should_be_entity_columns,
        )
