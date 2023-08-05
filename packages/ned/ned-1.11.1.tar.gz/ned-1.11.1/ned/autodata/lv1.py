"""Generate label data from the table.
"""


from dataclasses import dataclass
from operator import itemgetter
from typing import Mapping

from kgdata.wikidata.models.wdclass import WDClass
from kgdata.wikidata.models.wdentity import WDEntity
from ned.data_models.prelude import EntityWithScore
from sm.dataset import FullTable
from sm.inputs.link import WIKIDATA, EntityId, Link


@dataclass
class LabelV1Args:
    topk: int = 1
    threshold: float = 0.7
    include_similar_score: bool = False


class LabelV1:
    VERSION = 101

    def __init__(
        self,
        args: LabelV1Args,
        entities: Mapping[str, WDEntity],
        pagerank: Mapping[str, float],
        classes: Mapping[str, WDClass],
    ):
        self.args = args
        self.entities = entities
        self.pagerank = pagerank
        self.classes = classes

    def label(
        self, table: FullTable, columns: list[int]
    ) -> list[list[EntityWithScore]]:
        return [self.label_column(table.links[:, ci]) for ci in columns]

    def label_column(self, links: list[list[Link]]) -> list[EntityWithScore]:
        type2freq = get_type_freq(links, self.entities, self.classes)
        output = []
        for c, freq in sorted(type2freq.items(), key=itemgetter(1), reverse=True):
            if freq < self.args.threshold:
                break

            if len(output) >= self.args.topk and (
                not self.args.include_similar_score
                or (self.args.include_similar_score and output[-1].score != freq)
            ):
                break

            output.append(
                EntityWithScore(
                    EntityId(c, WIKIDATA),
                    freq,
                )
            )
        return output


def get_type_freq(
    links: list[list[Link]],
    entities: Mapping[str, WDEntity],
    classes: Mapping[str, WDClass],
) -> dict[str, float]:
    """Calculating frequency of types in a column.
    Borrow from grams.algorithms.inferences_v2.features.node_feature.
    Difficult to reuse as it requires data graph/candidate graph.
    """
    n_linked_rows = 0
    type2freq = {}

    for ri in range(len(links)):
        found_classes = set()
        entity_ids = [e for link in links[ri] for e in link.entities]
        for entity_id in entity_ids:
            ent = entities[str(entity_id)]
            for ent_type in ent.instance_of():
                if ent_type not in classes:
                    # sometimes people just tag things incorrectly, e.g.,
                    # Q395 is not instanceof Q41511 (Q41511 is not a class)
                    continue
                found_classes.add(ent_type)

        for c in found_classes:
            if c not in type2freq:
                type2freq[c] = 0
            type2freq[c] += 1

        if len(entity_ids) > 0:
            n_linked_rows += 1

    return {c: freq / n_linked_rows for c, freq in type2freq.items()}


def filter_rows_miss_type(
    table: FullTable, ci: int, types: set[str], entities: Mapping[str, WDEntity]
) -> list[int]:
    nrows = len(table.table.columns[ci].values)
    links = table.links

    miss_type_rows = []

    for ri in range(nrows):
        entity_ids = (e for link in links[ri, ci] for e in link.entities)
        if all(
            ent_type not in types
            for entity_id in entity_ids
            for ent_type in entities[str(entity_id)].instance_of()
        ):
            miss_type_rows.append(ri)

    return miss_type_rows
