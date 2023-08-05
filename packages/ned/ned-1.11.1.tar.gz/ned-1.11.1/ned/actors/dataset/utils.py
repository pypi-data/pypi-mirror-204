from __future__ import annotations

from collections import defaultdict
from copy import deepcopy
from functools import partial
from typing import Callable, Mapping, Optional, cast

import serde.jl
import serde.json
import serde.textline
from rdflib.namespace import RDFS
from ream.prelude import DatasetDict
from sm.inputs.link import WIKIDATA, EntityId

from grams.algorithm.literal_matchers.text_parser import TextParser
from kgdata.wikidata.models.wdproperty import WDProperty
from ned.data_models.prelude import CellLink, NEDExample
from sm.dataset import Example, FullTable
from sm.inputs.table import ColumnBasedTable
from sm.namespaces.namespace import KnowledgeGraphNamespace, OutOfNamespace
from sm.prelude import M


class NEDDatasetDict(DatasetDict[list[NEDExample]]):
    serde = (serde.jl.ser, partial(serde.jl.deser, cls=NEDExample), "jl")


def normalize_table(tbl: ColumnBasedTable, text_parser: TextParser) -> ColumnBasedTable:
    table = deepcopy(tbl)
    for col in table.columns:
        assert col.name is not None
        col.name = text_parser._norm_string(col.name)

    # normalize cells
    for ci, col in enumerate(table.columns):
        for ri, cell in enumerate(col.values):
            if isinstance(cell, str):
                col.values[ri] = text_parser._norm_string(cell)
    return table


def get_cell_links(
    example: Example[FullTable],
    is_column_entity: Callable[[Example[FullTable], int], bool],
) -> M.Matrix[CellLink | None]:
    """Converts links in a table to cell links. Links in the table allow same entity to be appeared in multiple mentioned in a cell
    while cell links do not allow that. For that reason,

    """
    cell_links = M.Matrix.default(
        example.table.table.shape(), cast(Optional[CellLink], None)
    )

    for ci, col in enumerate(example.table.table.columns):
        if not is_column_entity(example, ci):
            continue
        for ri in range(len(col.values)):
            links = [
                link for link in example.table.links[ri, ci] if len(link.entities) > 0
            ]
            if len(links) == 0:
                continue

            mentions = {}
            ents = []
            for link in links:
                for entid in link.entities:
                    if entid in mentions:
                        mentions[entid].append((link.start, link.end))
                        continue
                    ents.append(EntityId(entid, WIKIDATA))
                    mentions[entid] = [(link.start, link.end)]

            cell_links[ri, ci] = CellLink(
                entities=ents,
                mentions=mentions,
            )
    return cell_links


def is_column_entity(example: Example[FullTable], ci: int):
    for sm in example.sms:
        stypes = sm.get_semantic_types_of_column(ci)
        if any(stype.predicate_abs_uri == str(RDFS.label) for stype in stypes):
            return True
    return False


def should_be_column_entity(
    example: Example[FullTable],
    ci: int,
    wdprops: Mapping[str, WDProperty],
    kgns: KnowledgeGraphNamespace,
):
    for sm in example.sms:
        dnode = sm.get_data_node(ci)
        for inedge in sm.in_edges(dnode.id):
            try:
                propid = kgns.get_prop_id(inedge.abs_uri)
            except OutOfNamespace:
                continue
            if propid in wdprops and wdprops[propid].is_object_property():
                return True
    return False


def has_non_unique_mention(example: NEDExample) -> bool:
    """Check if the example table has the same mention at different cells linked to different entities"""
    col2mention = defaultdict(lambda: defaultdict(set))

    for ri, ci, link in example.cell_links.enumerate_flat_iter():
        if link is None:
            continue

        text = example.table[ri, ci]
        assert isinstance(text, str), text

        for entid, ranges in link.mentions.items():
            for start, end in ranges:
                mention = text[start:end]
                col2mention[ci][mention].add(entid)
                if len(col2mention[ci][mention]) > 1:
                    return True

    return False
