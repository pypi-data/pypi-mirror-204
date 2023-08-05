from dataclasses import dataclass, field
from typing import Literal, Optional
from grams.algorithm.literal_matchers.text_parser import TextParser
from ned.actors.dataset.utils import (
    has_non_unique_mention,
    normalize_table,
    NEDDatasetDict,
    get_cell_links,
)
from ned.actors.db import DBActor
from ned.autodata.erv1 import EntityRecognitionV1, EntityRecognitionV1Args
from ned.data_models.pymodels import NEDExample

from ream.actors.base import BaseActor
from pathlib import Path
from ream.dataset_helper import DatasetQuery
from ream.cache_helper import Cache
from ned.autodata.prelude import (
    FilterRegex,
    FilterRegexArgs,
    FilterV1Args,
    FilterV1,
    TransformV1,
    TransformV1Args,
    LabelV1Args,
    LabelV1,
    CombinedFilter,
    CombinedFilterArgs,
    FilterByEntType,
    FilterByEntTypeArgs,
    FilterByHeaderColType,
    FilterByHeaderColTypeArgs,
)
from ream.params_helper import EnumParams
from sm.dataset import Dataset, Example, FullTable
from sm.namespaces.wikidata import WikidataNamespace


@dataclass
class NEDAutoDatasetParams(EnumParams):
    dataset_dir: Path
    skip_non_unique_mention: bool = False
    skip_column_with_no_type: bool = field(
        default=False,
        metadata={
            "help": "Column that auto-labeler cannot find any entity type will be skipped"
        },
    )
    recog_method: Literal["recog_v1"] = field(
        default="recog_v1",
        metadata={
            "help": "Entity recognition method to use",
            "variants": {"recog_v1": EntityRecognitionV1},
        },
    )
    recog_v1: EntityRecognitionV1Args = field(
        default_factory=EntityRecognitionV1Args,
        metadata={"help": "Entity recognition v1 arguments"},
    )
    filter_method: Literal[
        "filter_regex",
        "filter_v1",
        "filter_ent_type",
        "filter_header_col_type",
        "filter_combined",
    ] = field(
        default="filter_regex",
        metadata={
            "help": "Filter method to use",
            "variants": {
                "filter_regex": FilterRegex,
                "filter_v1": FilterV1,
                "filter_ent_type": FilterByEntType,
                "filter_header_col_type": FilterByHeaderColType,
                "filter_combined": CombinedFilter,
            },
        },
    )
    filter_regex: FilterRegexArgs = field(
        default_factory=FilterRegexArgs,
        metadata={"help": "Filter regex arguments"},
    )
    filter_ent_type: FilterByEntTypeArgs = field(
        default_factory=FilterByEntTypeArgs,
        metadata={"help": "Filter by entity type arguments"},
    )
    filter_header_col_type: Optional[FilterByHeaderColTypeArgs] = field(
        default=None,
        metadata={"help": "Filter by header col type arguments"},
    )
    filter_combined: CombinedFilterArgs = field(
        default_factory=CombinedFilterArgs,
        metadata={"help": "Combined filter arguments"},
    )
    filter_v1: FilterV1Args = field(
        default_factory=FilterV1Args,
        metadata={"help": "Filter v1 arguments"},
    )
    transform_method: Literal["transform_v1"] = field(
        default="transform_v1",
        metadata={
            "help": "Transformation method to use",
            "variants": {"transform_v1": TransformV1},
        },
    )
    transform_v1: TransformV1Args = field(
        default_factory=TransformV1Args,
        metadata={"help": "Transformation v1 arguments"},
    )
    label_method: Literal["label_v1"] = field(
        default="label_v1",
        metadata={
            "help": "Label method to use",
            "variants": {"label_v1": LabelV1},
        },
    )
    label_v1: LabelV1Args = field(default_factory=LabelV1Args)


class NEDAutoDatasetActor(BaseActor[str, NEDAutoDatasetParams]):
    VERSION = 105

    def __init__(self, params: NEDAutoDatasetParams, db_actor: DBActor):
        super().__init__(params, [db_actor])
        self.db_actor = db_actor

    @Cache.mem()
    def run_dataset(self, query: str) -> NEDDatasetDict:
        dsquery = DatasetQuery.from_string(query)
        dsdict = NEDDatasetDict(dsquery.dataset, {})
        for subset, sub_dsquery in dsquery.iter_subset():
            dsdict[subset] = self._run_dataset(sub_dsquery.strip().get_query())[""]
        return dsdict

    @Cache.cls.dir(
        cls=NEDDatasetDict,
        mem_persist=True,
        dirname=lambda self, query: DatasetQuery.from_string(query).dataset,
        log_serde_time=True,
        compression="lz4",
    )
    def _run_dataset(self, query: str) -> NEDDatasetDict:
        dsquery = DatasetQuery.from_string(query)
        examples = self.autolabel_dataset(dsquery.dataset)
        return NEDDatasetDict.molt(dsquery.select(examples))

    @Cache.mem()
    def autolabel_dataset(self, dataset: str) -> list[NEDExample]:
        examples = Dataset(self.params.dataset_dir / dataset).load()
        er = self.get_er()
        fil = self.get_filter()
        map = self.get_transformation()
        labeler = self.get_label()

        text_parser = TextParser.default()
        new_examples = []

        for ex in examples:
            table = ex.table
            entity_columns = er.recognize(table)
            entity_columns = fil.filter(table, entity_columns)
            table = map.transform(table, entity_columns)
            entity_column_types = labeler.label(table, entity_columns)

            if self.params.skip_column_with_no_type:
                valid_cols = [
                    i
                    for i in range(len(entity_columns))
                    if len(entity_column_types[i]) > 0
                ]
                entity_columns = [entity_columns[i] for i in valid_cols]
                entity_column_types = [entity_column_types[i] for i in valid_cols]

            if len(entity_columns) == 0:
                continue

            # convert full table to ned table
            ned_ex = NEDExample(
                table=normalize_table(ex.table.table, text_parser),
                entity_columns=entity_columns,
                entity_column_types=entity_column_types,
                cell_links=get_cell_links(
                    Example(sms=ex.sms, table=table),
                    is_column_entity=lambda tbl, ci: ci in entity_columns,
                ),
                should_be_entity_columns=[],
            )

            if self.params.skip_non_unique_mention and has_non_unique_mention(ned_ex):
                continue

            new_examples.append(ned_ex)
        return new_examples

    @Cache.mem()
    def get_er(self):
        if self.params.recog_method == "recog_v1":
            return EntityRecognitionV1(self.params.recog_v1)
        raise NotImplementedError()

    @Cache.mem()
    def get_filter(self):
        logfile = self.get_working_fs().root / "logs/filter.log"
        if self.params.filter_method == "filter_regex":
            return FilterRegex(self.params.filter_regex, logfile)
        if self.params.filter_method == "filter_v1":
            return FilterV1(
                self.params.filter_v1,
                self.db_actor.entities,
                logfile,
            )
        if self.params.filter_method == "filter_combined":
            filters = [
                FilterRegex(self.params.filter_combined.regex, logfile),
                FilterByEntType(
                    self.params.filter_combined.ignore_types,
                    self.db_actor.entities,
                    self.db_actor.classes,
                    logfile,
                ),
            ]
            if self.params.filter_combined.header_col_type is not None:
                filters.append(
                    FilterByHeaderColType(
                        self.params.filter_combined.header_col_type,
                        self.get_label(),
                        logfile,
                    )
                )
            return CombinedFilter(
                filters,
                logfile,
            )
        raise NotImplementedError()

    @Cache.mem()
    def get_transformation(self):
        logfile = self.get_working_fs().root / "logs/transform.log"
        if self.params.transform_method == "transform_v1":
            return TransformV1(
                self.params.transform_v1,
                self.db_actor.entities,
                self.db_actor.classes,
                logfile,
            )
        raise NotImplementedError()

    @Cache.mem()
    def get_label(self):
        if self.params.label_method == "label_v1":
            return LabelV1(
                self.params.label_v1,
                self.db_actor.entities,
                self.db_actor.pagerank,
                self.db_actor.classes,
            )
        raise NotImplementedError()
