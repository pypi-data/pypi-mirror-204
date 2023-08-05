from __future__ import annotations
from typing import Literal, Mapping, Optional
from kgdata.wikidata.db import WikidataDB
from kgdata.wikidata.models.wdentity import WDEntity
from ned.autodata.freg import FilterRegex, FilterRegexArgs
from ned.autodata.utils import FilterMixin, StrPath
import py_stringmatching as sm
from sm.dataset import FullTable
from dataclasses import dataclass

from sm.inputs.link import Link

"""Filtering linked columns in the tables that are noisy:

* Columns that majority of the linked entities are dissimilar to the mentioned.

"""


@dataclass
class FilterV1Args:
    similarity_method: Literal["monge_elkan", "general_jaccard"] = "monge_elkan"
    dissimilarity_threshold: float = 0.2
    noisy_threshold: float = 0.5


class FilterV1(FilterMixin):
    VERSION = 100

    def __init__(
        self,
        args: FilterV1Args,
        entities: Mapping[str, WDEntity],
        log_file: Optional[StrPath] = None,
    ):
        super().__init__(log_file)
        self.entities = entities
        self.args = args
        self.strsim = StrSim(args.similarity_method)
        self.regex_filter = FilterRegex(FilterRegexArgs(args.noisy_threshold))

    def is_noisy(self, table: FullTable, ci: int) -> tuple[bool, str]:
        if (regex_filter_res := self.regex_filter.is_noisy(table, ci))[0]:
            return regex_filter_res
        values = table.table.columns[ci].values

        n_noisy_cells = 0
        for ri, cell in enumerate(values):
            if len(table.links[ri, ci]) == 0:
                continue
            if (
                self.compute_dissimilarity(cell, table.links[ri, ci])
                >= self.args.dissimilarity_threshold
            ):
                n_noisy_cells += 1

        nfreq = n_noisy_cells / len(values)
        return nfreq >= self.args.noisy_threshold, f"{nfreq:.03f} cells are noisy"

    def compute_dissimilarity(self, cell: str, links: list[Link]) -> float:
        entities = self.entities
        score = 0.0
        for link in links:
            for entity in link.entities:
                score = max(
                    score,
                    self.strsim.match(
                        cell, self.iter_entity_name(entities[str(entity)])
                    ),
                )
        return 1 - score

    def iter_entity_name(self, entity: WDEntity):
        for label in entity.label.lang2value.values():
            yield label
        for aliases in entity.aliases.lang2values.values():
            for alias in aliases:
                yield alias


class StrSim:
    def __init__(self, method: Literal["monge_elkan", "general_jaccard"]):
        if method == "monge_elkan":
            self.simfn = sm.MongeElkan()
        else:
            self.simfn = sm.GeneralizedJaccard(sim_func=sm.JaroWinkler().get_raw_score)
        self.tokenizer = sm.WhitespaceTokenizer()

    def match(self, query: str, keys) -> float:
        query_tokens = self.tokenizer.tokenize(query)
        return max(self.sim(query_tokens, self.tokenizer.tokenize(key)) for key in keys)

    def sim(self, s1, s2):
        return self.simfn.get_raw_score(s1, s2)
