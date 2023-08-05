from __future__ import annotations
import os

import pickle
from dataclasses import dataclass, field, fields
from functools import partial
from typing import Literal, Optional

from hugedict.prelude import HugeMutableMapping, RocksDBDict, RocksDBOptions
from kgdata.wikidata.db import WikidataDB
from ned.actors.dataset.prelude import NEDDatasetActor
from ned.actors.entity_recognition import EntityRecognitionActor
from ned.actors.evaluate_helper import EvalArgs, evaluate
from ned.candidate_generation.mtab_wrapper import MTabWrapper, MTabArgs
from ned.candidate_generation.oracle_semtyper import OracleSemTyper, OracleSemTyperArgs
from ned.candidate_generation.pyserini_wrapper import PyseriniArgs, PyseriniWrapper
from ned.data_models.prelude import (
    DatasetCandidateEntities,
    CandidateEntity,
    NEDExample,
)
from ream.actor_version import ActorVersion
from ream.cache_helper import CacheArgsHelper
from ream.dataset_helper import DatasetDict
from ream.prelude import FS, ActorState, DatasetQuery, EnumParams, Cache, ReamWorkspace
from sm.misc.ray_helper import get_instance
from timer import Timer
from sm.misc.funcs import assert_not_null
from osin.integrations.ream import OsinActor
from ned.candidate_generation.localsearch import LocalSearchArgs, LocalSearch


@dataclass
class CGParams(EnumParams):
    method: Literal["pyserini", "oracle_semtyper", "mtab"] = field(
        metadata={
            "help": "Candidate generation method",
            "variants": {
                "pyserini": PyseriniWrapper,
                "oracle_semtyper": OracleSemTyper,
                "mtab": MTabWrapper,
            },
        }
    )
    pyserini: Optional[PyseriniArgs] = None
    oracle_semtyper: Optional[OracleSemTyperArgs] = None
    mtab: Optional[MTabArgs] = None
    localsearch: Optional[LocalSearchArgs] = field(
        default=None,
        metadata={
            "help": "Search for more candidates by matching the entity's properties with the table's cells"
        },
    )
    cache: bool = field(
        default=True,
        metadata={"help": "Whether to cache candidate generation results. "},
    )


class CGDatasetDict(DatasetDict[DatasetCandidateEntities]):
    serde = (DatasetCandidateEntities.save, DatasetCandidateEntities.load, None)


class CanGenActor(
    OsinActor[
        NEDExample,
        CGParams,
    ]
):
    """
    Evaluating different methods in generating candidate entities for Record Linkage problem

    Each example is the whole table because a method may want to use other information such
    as headers or the surrounding context of the cell to generate candidates.
    """

    """CHANGELOG:
    - 200: new ream
    - 21x: same dataset shares the same cache dir for key-value store only.
    """
    VERSION = ActorVersion.create(220, [LocalSearch])
    EXP_NAME = "Candidate Generation"
    EXP_VERSION = 3

    def __init__(
        self,
        params: CGParams,
        dataset_actor: NEDDatasetActor,
        entity_recognition_actor: EntityRecognitionActor,
    ):
        super().__init__(params, dep_actors=[dataset_actor, entity_recognition_actor])
        self.db_actor = dataset_actor.auto_dataset_actor.db_actor
        self.dataset_actor = dataset_actor
        self.entity_recognition_actor = entity_recognition_actor
        self.dataset_name = ""

    def run(self, example: NEDExample) -> DatasetCandidateEntities:
        return self.batch_run([example])

    def batch_run(self, examples: list[NEDExample]) -> DatasetCandidateEntities:
        entity_columns = self.entity_recognition_actor.batch_run(examples)
        return self.get_method(self.dataset_name).get_candidates(
            examples, entity_columns
        )

    def get_provenance(self):
        return self.entity_recognition_actor.get_provenance()

    @Cache.mem(cache_self_args=CacheArgsHelper.gen_cache_self_args(get_provenance))
    def run_dataset(self, query: str):
        dsquery = DatasetQuery.from_string(query)
        dsdict = CGDatasetDict(dsquery.dataset, {}, provenance=self.get_provenance())
        for subset, sub_dsquery in dsquery.iter_subset():
            tmp_dsdict = self._run_dataset(sub_dsquery.strip().get_query())
            assert tmp_dsdict.provenance == dsdict.provenance
            dsdict[subset] = tmp_dsdict[""]
        return dsdict

    @Cache.cls.dir(
        cls=CGDatasetDict,
        cache_self_args=CacheArgsHelper.gen_cache_self_args(get_provenance),
        mem_persist=True,
        dirname=lambda self, query: DatasetQuery.from_string(query).dataset,
        compression="lz4",
        log_serde_time=True,
    )
    def _run_dataset(self, query: str):
        dsdict = self.dataset_actor.run_dataset(query)
        er_dsdict = self.entity_recognition_actor.run_dataset(query)

        localsearch = (
            None
            if self.params.localsearch is None
            else LocalSearch(self.params.localsearch, self.db_actor.db)
        )

        out = CGDatasetDict(dsdict.name, {}, er_dsdict.provenance)
        method = self.get_method(dsdict.name)
        timer = Timer()
        for name, ds in dsdict.items():
            with timer.watch("run candidate generation"):
                cans = method.get_candidates(ds, er_dsdict[name])
                if localsearch is not None:
                    cans = localsearch.augment_candidates(ds, cans)
                out[name] = cans
        timer.report(self.logger.debug)
        return out

    def evaluate(self, eval_args: EvalArgs):
        for dsquery_s in eval_args.dsqueries:
            dsquery = DatasetQuery.from_string(dsquery_s)
            dsdict = self.dataset_actor.run_dataset(dsquery_s)
            er_dsdict = self.entity_recognition_actor.run_dataset(dsquery_s)
            cangen_dsdict = self.run_dataset(dsquery_s)

            for name, examples in dsdict.items():
                candidates = cangen_dsdict[name]
                entity_columns = er_dsdict[name]
                self.logger.debug("Running evaluation on dataset {}", dsquery_s)
                dsname = dsquery.get_query(name)
                with self.new_exp_run(
                    dataset=dsname, exprun_type=eval_args.exprun_type
                ) as exprun:
                    evaluate(
                        self.db_actor.entities,
                        examples,
                        entity_columns,
                        candidates,
                        eval_ignore_nil=eval_args.eval_ignore_nil,
                        eval_ignore_non_entity_cell=eval_args.eval_ignore_non_entity_cell,
                        dsname=dsname,
                        logger=self.logger,
                        exprun=exprun,
                        report_unique=True,
                        exprun_type=eval_args.exprun_type,
                    )
                    if exprun is not None:
                        exprun.update_output(
                            primitive={"workdir": str(self.get_working_fs().root)}
                        )

    @Cache.mem()
    def _get_kv_cache(
        self, dataset_name: str
    ) -> HugeMutableMapping[str, list[tuple[str, float]]]:
        dbname = dataset_name + "_cache_db"
        if self.params.method == "pyserini":
            state = ActorState.create(
                PyseriniWrapper, self.params.pyserini, dependencies=[]
            )
        elif self.params.method == "oracle_semtyper":
            # leverage the fact that oracle_semtyper is just a wrapper of pyserini
            # so the cache is the same
            args = PyseriniArgs(
                **{
                    field.name: getattr(self.params.oracle_semtyper, field.name)
                    for field in fields(PyseriniArgs)
                }
            )
            state = ActorState.create(PyseriniWrapper, args, dependencies=[])
        elif self.params.method == "mtab":
            state = ActorState.create(MTabWrapper, self.params.mtab, dependencies=[])
            dbname = dataset_name[:2] + "_cache_db"
        else:
            raise NotImplementedError()

        cache_dir = ReamWorkspace.get_instance().reserve_working_dir(state)
        self.logger.debug(
            "Using directory: {} for key-value store caching",
            cache_dir,
        )
        wfs = FS(cache_dir)

        dsdir = wfs.get(dbname, {}, save_key=True)
        if not dsdir.exists():
            with wfs.acquire_write_lock(), dsdir.reserve_and_track() as realdir:
                dbpath = str(realdir)
        else:
            dbpath = str(dsdir.get())

        return get_instance(
            lambda: RocksDBDict(
                path=dbpath,
                options=RocksDBOptions(create_if_missing=True),
                deser_key=partial(str, encoding="utf-8"),
                deser_value=pickle.loads,
                ser_value=pickle.dumps,
                # allow to control if the cache should be opened in read-only mode
                # to run multiple experiments in parallel
                readonly=os.environ.get("CANGEN_ROCKSDB_READONLY", "0") == "1",
            ),
            f"rockdb[{dbpath}]",
        )

    @Cache.mem()
    def get_method(self, dataset_name: str):
        kvstore = self._get_kv_cache(dataset_name) if self.params.cache else None

        if self.params.method == "pyserini":
            return PyseriniWrapper(
                assert_not_null(self.params.pyserini), self.db_actor.db, kvstore
            )
        elif self.params.method == "oracle_semtyper":
            args = assert_not_null(self.params.oracle_semtyper)
            return OracleSemTyper(
                PyseriniWrapper(args, self.db_actor.db, kvstore),
                self.db_actor.db,
                args,
            )
        elif self.params.method == "mtab":
            return MTabWrapper(
                assert_not_null(self.params.mtab),
                self.db_actor.db,
                kvstore,
            )
        else:
            raise NotImplementedError(self.params.method)
