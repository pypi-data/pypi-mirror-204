from __future__ import annotations

import random
from dataclasses import dataclass
from pathlib import Path
from typing import Callable, Mapping, Optional, Union
from ned.data_models.pymodels import EntityWithScore

import numpy as np
import serde.jl
import serde.json
import serde.textline
from osin.integrations.ream import OsinActor
from rdflib.namespace import RDFS
from ream.prelude import Cache, DatasetQuery
from slugify import slugify
from sm.inputs.link import WIKIDATA, EntityId
from sm_datasets import Datasets

from grams.algorithm.literal_matchers.text_parser import TextParser
from kgdata.wikidata.db import WikidataDB
from kgdata.wikidata.models import WDEntity
from ned.actors.db import to_wikidata_db
from ned.actors.evaluate_helper import AuxComplexTableObject, EvalArgs
from ned.data_models.prelude import NEDExample
from sm.dataset import Example, FullTable
from sm.misc.ray_helper import ray_map, ray_put
from sm.namespaces.namespace import KnowledgeGraphNamespace
from sm.namespaces.wikidata import WikidataNamespace
from sm.prelude import M

from ned.actors.dataset.auto_dataset import NEDAutoDatasetActor
from ned.actors.dataset.utils import (
    NEDDatasetDict,
    has_non_unique_mention,
    normalize_table,
    is_column_entity,
    get_cell_links,
    should_be_column_entity,
)


@dataclass
class NEDDatasetParams:
    skip_non_unique_mention: bool = False


class NEDDatasetActor(OsinActor[str, NEDDatasetParams]):
    """An actor that will output the dataset for entity linking."""

    """CHANGELOG:
    - 401: add option to skip tables that the same mention at different cells are linked to different entities
    - 41x: add entity column types to the example, ignore tables with empty entity columns, 
    """

    EXP_NAME = "Dataset"
    VERSION = 505
    EXP_VERSION = 2

    kgns = WikidataNamespace.create()

    def __init__(
        self, params: NEDDatasetParams, auto_dataset_actor: NEDAutoDatasetActor
    ):
        super().__init__(params, [auto_dataset_actor])
        self.auto_dataset_actor = auto_dataset_actor
        self.text_parser = TextParser.default()

    @Cache.mem()
    def run_dataset(self, query: str) -> NEDDatasetDict:
        dsquery = DatasetQuery.from_string(query)
        if dsquery.dataset.startswith("wtauto"):
            assert (
                self.auto_dataset_actor.params.skip_non_unique_mention
                == self.params.skip_non_unique_mention
            )
            return self.auto_dataset_actor.run_dataset(query)

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
    def _run_dataset(
        self,
        query: str,
    ) -> NEDDatasetDict:
        dsquery = DatasetQuery.from_string(query)
        ned_examples = self.ned_examples(dsquery.dataset)

        infodir = self.get_working_fs().root / (f"info_" + slugify(dsquery.dataset))
        infodir.mkdir(exist_ok=True)

        if self.params.skip_non_unique_mention:
            non_unique_table_ids = [
                e.table.table_id for e in ned_examples if has_non_unique_mention(e)
            ]
            serde.textline.ser(
                non_unique_table_ids,
                infodir / f"non_unique_tables.txt",
            )
            non_unique_table_ids = set(non_unique_table_ids)
            ned_examples = [
                e for e in ned_examples if e.table.table_id not in non_unique_table_ids
            ]
            self.logger.info(
                "Skip {} tables with non-unique mentions",
                len(non_unique_table_ids),
            )

        if dsquery.shuffle:
            shuffle_file = infodir / f"shuffle_{dsquery.seed or 'none'}.json"
            if not shuffle_file.exists():
                index = list(range(len(ned_examples)))
                random.Random(dsquery.seed).shuffle(index)
                shuffle_index = [ned_examples[i].table.table_id for i in index]
                serde.json.ser(
                    shuffle_index,
                    shuffle_file,
                )

        return NEDDatasetDict.molt(dsquery.select(ned_examples))

    def evaluate(self, eval_args: EvalArgs):
        for query in eval_args.dsqueries:
            dsquery = DatasetQuery.from_string(query)
            dsdict = self.run_dataset(query)
            for name, examples in dsdict.items():
                n_cells = [np.prod(e.table.shape()) for e in examples]
                n_rows = [e.table.shape()[0] for e in examples]

                metrics = {
                    "# examples": len(examples),
                    "average # cells": float(np.mean(n_cells)),
                    "max # cells": float(np.max(n_cells)),
                    "min # cells": float(np.min(n_cells)),
                }
                for pth in [25, 50, 75, 90, 95, 99]:
                    metrics[f"{pth} percentile # cells"] = float(
                        np.percentile(n_cells, pth)
                    )

                metrics.update(
                    {
                        "average # rows": float(np.mean(n_rows)),
                        "max # rows": float(np.max(n_rows)),
                        "min # rows": float(np.min(n_rows)),
                    }
                )
                for pth in [25, 50, 75, 90, 95, 99]:
                    metrics[f"{pth} percentile # rows"] = float(
                        np.percentile(n_rows, pth)
                    )

                self.logger.info(
                    "Dataset {} - split {}:",
                    dsdict.name,
                    name,
                )
                for k, v in metrics.items():
                    self.logger.info("\t - {}: {}", k, v)

                with self.new_exp_run(dataset=dsquery.get_query(name)) as exprun:
                    if exprun is not None:
                        for ei, example in enumerate(examples):
                            exprun.update_example_output(
                                example_id=str(ei),
                                example_name=example.table.table_id,
                                complex={
                                    "table": AuxComplexTableObject(
                                        self.auto_dataset_actor.db_actor.entities
                                    ).get_table(example, None)
                                },
                            )

                        exprun.update_output(primitive=metrics)

    @Cache.jl.file(mem_persist=True, compression="lz4", cls=NEDExample)
    def ned_examples(self, dataset: str) -> list[NEDExample]:
        dbdir_ref = ray_put(WikidataDB.get_instance().database_dir)
        list_exs = ray_map(
            sm2ned_example,
            [(dbdir_ref, item) for item in M.batch(48, self.sm_examples(dataset))],
            verbose=True,
            desc="generate ned examples",
            using_ray=True,
            is_func_remote=False,
        )
        return [e for lst in list_exs for e in lst]

    @Cache.pickle.file(mem_persist=True, compression="lz4")
    def sm_examples(self, dataset: str) -> list[Example[FullTable]]:
        ds = Datasets()
        db = WikidataDB.get_instance()
        examples = getattr(ds, dataset)()
        examples = ds.fix_redirection(
            examples, db.wdentities, db.wdredirections, self.kgns
        )
        return examples


def sm2ned_example(
    db: Union[WikidataDB, Path], sm_examples: list[Example[FullTable]]
) -> list[NEDExample]:
    db = to_wikidata_db(db)

    text_parser = TextParser.default()
    kgns = WikidataNamespace.create()

    wdents = db.wdentities.cache()
    wdprops = db.wdprops.cache()
    wdpopularity = db.wdpagerank
    new_examples = []

    for example in sm_examples:
        new_examples.append(
            to_ned_example(
                example,
                text_parser,
                kgns,
                wdents,
                wdpopularity,
                is_column_entity=is_column_entity,
                should_be_column_entity=lambda tbl, ci: should_be_column_entity(
                    tbl, ci, wdprops, kgns
                ),
            )
        )
    return new_examples


def to_ned_example(
    example: Example[FullTable],
    text_parser: TextParser,
    kgns: KnowledgeGraphNamespace,
    entities: Mapping[str, WDEntity],
    pagerank: Mapping[str, float],
    is_column_entity: Callable[[Example[FullTable], int], bool],
    should_be_column_entity: Callable[[Example[FullTable], int], bool],
) -> Optional[NEDExample]:
    table = normalize_table(example.table.table, text_parser)

    should_be_entity_columns = []
    entity_columns = []
    entity_column_types: list[list[EntityWithScore]] = []

    for ci in range(example.table.table.shape()[1]):
        if is_column_entity(example, ci):
            entity_columns.append(ci)
            ctypes = []
            for sm in example.sms:
                for stype in sm.get_semantic_types_of_column(ci):
                    if stype.predicate_abs_uri == str(RDFS.label):
                        ctypes.append(kgns.get_entity_id(stype.class_abs_uri))
            entity_column_types.append(
                [
                    EntityWithScore(
                        EntityId(entid, WIKIDATA),
                        1.0,
                    )
                    for entid in M.filter_duplication(ctypes)
                ]
            )
        elif should_be_column_entity(example, ci):
            should_be_entity_columns.append(ci)

    if len(entity_columns) + len(should_be_entity_columns) == 0:
        # there is no entity column in this table
        return None

    return NEDExample(
        table=table,
        entity_columns=entity_columns,
        entity_column_types=entity_column_types,
        cell_links=get_cell_links(example, is_column_entity),
        should_be_entity_columns=should_be_entity_columns,
    )
