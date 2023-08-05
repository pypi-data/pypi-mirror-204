from __future__ import annotations
import copy

import os
from dataclasses import dataclass, field
from typing import Literal, Optional, cast
from ned.candidate_ranking.cr_searchscore import CRSearchScore
from ned.candidate_ranking.cr_string_similarity import (
    CRStringSimilarity,
    CRStringSimilarityArgs,
)
from ned.candidate_ranking.helpers.dataset import MyDatasetDict
from ned.entity_recognition.oracle_model import OracleERModelArgs
from slugify import slugify
import torch
from osin.integrations.ream import OsinActor
from ream.actors.base import BaseActor
from ream.cache_helper import Cache, CacheArgsHelper
from ream.dataset_helper import DatasetQuery
from ream.fs import ItemStatus
from ream.params_helper import NoParams
from ream.helper import orjson_dumps
from ream.prelude import (
    ActorState,
    Cache,
    DatasetDict,
    DatasetQuery,
    EnumParams,
    NoParams,
)
from timer import Timer

from ned.actors.candidate_generation import CanGenActor
from ned.actors.dataset.prelude import NEDDatasetActor
from ned.actors.entity_recognition import (
    EntityRecognitionActor,
    ERParams,
)
from ned.actors.evaluate_helper import EvalArgs, evaluate
from ned.candidate_ranking.columnwise_model import ColumnwiseModel, ColumnwiseModelArgs
from ned.candidate_ranking.contrastive_pairwise_model import (
    ContrastivePairwiseModel,
    ContrastivePairwiseModelArgs,
)
from ned.candidate_ranking.cr_method import (
    CandidateEntityScores,
    CandidateRankingMethod,
)
from ned.candidate_ranking.cr_training import cr_training
from ned.candidate_ranking.helpers.training_helper import (
    CkptHelper,
    ModifiedTrainingArguments,
)
from ned.candidate_ranking.pairwise_model import PairwiseModel, PairwiseModelArgs
from ned.data_models.prelude import DatasetCandidateEntities, NEDExample
from sm.misc.prelude import assert_not_null
import scripts.ned.candidate_ranking.notebooks.models as new_models


@dataclass
class CRParams(EnumParams):
    method: Literal[
        "pairwise",
        "crv3",
        "columnwise",
        "contrastive_pairwise",
        "searchscore",
        "strsim",
    ] = field(
        metadata={
            "variants": {
                "pairwise": PairwiseModel,
                "crv3": new_models.CRV3,
                "columnwise": ColumnwiseModel,
                "contrastive_pairwise": ContrastivePairwiseModel,
                "searchscore": CRSearchScore,
                "strsim": CRStringSimilarity,
            }
        }
    )
    training: Optional[ModifiedTrainingArguments] = None
    crv3: Optional[new_models.CRV3Args] = None
    pairwise: Optional[PairwiseModelArgs] = None
    columnwise: Optional[ColumnwiseModelArgs] = None
    contrastive_pairwise: Optional[ContrastivePairwiseModelArgs] = None
    searchscore: Optional[NoParams] = field(default_factory=NoParams)
    strsim: Optional[CRStringSimilarityArgs] = None


class CRDatasetDict(DatasetDict[CandidateEntityScores]):
    serde = (CandidateEntityScores.save, CandidateEntityScores.load, None)


class CanRankActor(OsinActor[NEDExample, CRParams]):
    """Different methods in ranking candidate entities for Record Linkage problem"""

    """CHANGELOG:
    - 10X: fixing bugs
    - 110: switching to use pyarrow
    - 111: add missing depenedency which is canrank_dataset
    - 200: new version of ream
    """
    EXP_NAME = "Candidate Ranking"
    VERSION = 204
    EXP_VERSION = 3

    def __init__(
        self,
        params: CRParams,
        dataset_actor: NEDDatasetActor,
        cangen_actor: CanGenActor,
    ):
        canrank_dataset = CRModelDataActor(
            dataset_actor,
            cangen_actor,
        )
        super().__init__(
            params,
            [
                dataset_actor,
                cangen_actor,
                canrank_dataset,
            ],
        )
        self.db_actor = dataset_actor.auto_dataset_actor.db_actor
        self.db = self.db_actor.db
        self.dataset_actor = dataset_actor
        self.cangen_actor = cangen_actor
        self.canrank_dataset = canrank_dataset
        self.model: CandidateRankingMethod | None = None
        self.is_eval: bool = False
        self.timer = Timer()

    def run(
        self, example: NEDExample, candidates: DatasetCandidateEntities
    ) -> CandidateEntityScores:
        can = self.batch_run([example], candidates)
        return can

    def batch_run(
        self,
        examples: list[NEDExample],
        candidates: DatasetCandidateEntities | None = None,
    ) -> CandidateEntityScores:
        if candidates is None:
            candidates = self.cangen_actor.batch_run(examples)

        method, provenance = self.get_trained_method()
        ds = method.generate_dataset(examples, candidates)
        return method.rank_datasets(examples, candidates, ds)

    def get_provenance(self):
        method, provenance = self.get_trained_method()
        return self._fmt_provenance(self.cangen_actor.get_provenance(), provenance)

    @Cache.cls.dir(
        cls=CRDatasetDict,
        cache_self_args=CacheArgsHelper.gen_cache_self_args(get_provenance),
        mem_persist=True,
        compression="lz4",
        log_serde_time=True,
    )
    def run_dataset(self, dataset_query: str) -> CRDatasetDict:
        # run the candidate ranking on the dataset and return the result
        # we want to cache the result here. but we almost have to rerun
        # unless we can retrieve the result from the cache.
        dsdict = self.dataset_actor.run_dataset(dataset_query)
        cg_dsdict = self.cangen_actor.run_dataset(dataset_query)

        method, provenance = self.get_trained_method()
        canrank_dsdict = self.canrank_dataset.run_dataset(
            self.get_method(),
            dataset_query,
            for_training=False,
        )

        if not method.EVAL_ON_CPU:
            method = method.to(torch.device("cpu"))

        out = CRDatasetDict(
            cg_dsdict.name,
            {},
            self._fmt_provenance(cg_dsdict.provenance, provenance),
        )
        for name, candidates in cg_dsdict.items():
            examples = dsdict[name]
            self.logger.debug(
                "Running candidate ranking on dataset {}:{}", dsdict.name, name
            )
            # uncomment for debugging purpose
            # candidates = getattr(canrank_dsdict[name], "candidates")
            out[name] = method.rank_datasets(
                examples, candidates, canrank_dsdict[name], verbose=True
            )

        return out

    def evaluate(self, eval_args: EvalArgs):
        retrain = int(os.environ.get("CR_RETRAIN", "0")) == 1
        fromstep = int(os.environ.get("CR_RETRAIN_FROMSTEP", "0"))
        fromfile = os.environ.get("CR_RETRAIN_FROMFILE", None)
        self.get_trained_method(retrain=retrain, fromstep=fromstep, fromfile=fromfile)

        for dsquery_s in eval_args.dsqueries:
            dsquery = DatasetQuery.from_string(dsquery_s)

            dsdict = self.dataset_actor.run_dataset(dsquery_s)
            er_dsdict = self.cangen_actor.entity_recognition_actor.run_dataset(
                dsquery_s
            )
            cg_dsdict = self.cangen_actor.run_dataset(dsquery_s)
            cr_dsdict = self.run_dataset(dsquery_s)

            self.logger.debug("Running evaluation on dataset {}", dsquery_s)

            for name, examples in dsdict.items():
                entity_columns = er_dsdict[name]
                can_scores = cr_dsdict[name]
                candidates = cg_dsdict[name].replace("score", can_scores.score)

                subdsquery_s = dsquery.get_query(name)
                with self.new_exp_run(
                    dataset=subdsquery_s,
                    exprun_type=eval_args.exprun_type,
                    eval_ignore_nil=eval_args.eval_ignore_nil,
                ) as exprun:
                    evaluate(
                        self.db_actor.entities,
                        examples,
                        entity_columns,
                        candidates,
                        eval_ignore_nil=eval_args.eval_ignore_nil,
                        dsname=subdsquery_s,
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
    def get_method(self) -> CandidateRankingMethod:
        if self.params.method == "pairwise":
            model = PairwiseModel.from_args(assert_not_null(self.params.pairwise))
        elif self.params.method == "columnwise":
            model = ColumnwiseModel.from_args(assert_not_null(self.params.columnwise))
        elif self.params.method == "contrastive_pairwise":
            model = ContrastivePairwiseModel.from_args(
                assert_not_null(self.params.contrastive_pairwise)
            )
        elif self.params.method == "searchscore":
            model = CRSearchScore()
        elif self.params.method == "strsim":
            model = CRStringSimilarity.from_args(assert_not_null(self.params.strsim))
        elif self.params.method == "crv3":
            model = new_models.CRV3.from_args(assert_not_null(self.params.crv3))
        else:
            raise NotImplementedError()
        return model

    @Cache.mem()
    def get_trained_method(
        self,
        retrain: bool = False,
        fromstep: int = 0,
        fromfile: Optional[str] = None,
    ) -> tuple[CandidateRankingMethod, str]:
        if self.params.method in ["searchscore", "strsim"]:
            # return no trained methods
            method = self.get_method()
            return method, f"{self.params.method}_{method.VERSION}"

        wfs = self.get_working_fs()
        model_file = wfs.get("model.pt")

        if not model_file.exists() or retrain:
            # train the model again or resume training
            with wfs.acquire_write_lock():
                ckpt = CkptHelper(self.get_working_fs().root, fromstep, fromfile)
                eval_ds_mode: str = cast(
                    Literal["train", "test"], os.environ.get("EVAL_DS_MODE", "train")
                )
                assert eval_ds_mode in ["train", "test"]
                model, trained_file = cr_training(self, ckpt, eval_ds_mode)

                if model_file.exists():
                    linked_file = model_file.get()
                else:
                    linked_file = model_file.reserve()
                    model_file.update_status(ItemStatus.Success)

                if linked_file.exists():
                    os.remove(linked_file)
                os.symlink(
                    os.path.relpath(trained_file.absolute(), linked_file.parent),
                    linked_file,
                )
        else:
            statedict = torch.load(model_file.get(), map_location=torch.device("cpu"))
            model = self.get_method()
            model.load_state_dict(statedict["model"])
            model.eval()

            if torch.cuda.is_available():
                model = model.to(torch.device("cuda"))
            if torch.backends.mps.is_available():  # type: ignore
                model = model.to(torch.device("mps"))

        provenance = os.path.realpath(model_file.get())
        provenance = os.path.relpath(provenance, wfs.root)
        return model, provenance

    def _fmt_provenance(self, cg_prov: str, cr_prov: str) -> str:
        return f"cangen:{cg_prov};canrank:{cr_prov}"


class CRModelDataActor(BaseActor[str, NoParams]):
    """CHANGELOG:
    - 200: switch to new ream version
    """

    VERSION = 219

    def __init__(
        self,
        dataset_actor: NEDDatasetActor,
        cangen_actor: CanGenActor,
    ):
        super().__init__(NoParams(), dep_actors=[dataset_actor, cangen_actor])
        self.dataset_actor = dataset_actor
        self.cangen_actor = cangen_actor

        oracle_er_params = ERParams(
            method="oracle", oracle=OracleERModelArgs(), training=None
        )
        oracle_er_actor = EntityRecognitionActor(oracle_er_params, dataset_actor)
        cangen_params = copy.copy(cangen_actor.params)
        cangen_params.localsearch = None  # always disable local search
        self.train_cangen_actor = CanGenActor(
            cangen_params, dataset_actor, oracle_er_actor
        )

    def run_dataset(
        self,
        method: CandidateRankingMethod,
        dataset_query: str,
        for_training: bool = False,
    ):
        cg_dsdict = self.cangen_actor.run_dataset(dataset_query)

        # @Cache.cls.dir(
        #     cls=MyDatasetDict,
        #     cache_key=CRModelDataActor.get_cache_key,
        #     dirname=CRModelDataActor.get_cache_dirname,
        #     compression="lz4",
        # )
        def exec(
            self,
            method: CandidateRankingMethod,
            dataset_query: str,
            for_training: bool,
            cg_provenance: str,
        ):
            return self.gen_data(method, dataset_query, for_training)

        return exec(self, method, dataset_query, for_training, cg_dsdict.provenance)

    def gen_data(
        self,
        method: CandidateRankingMethod,
        dataset_query: str,
        for_training: bool = False,
    ):
        parsed_dsquery = DatasetQuery.from_string(dataset_query)
        builddir = self.get_working_fs().get(
            "build_" + parsed_dsquery.dataset,
            {"query": dataset_query, "for_training": for_training},
            save_key=True,
        )
        if builddir.exists():
            builddir_path = builddir.get()
        else:
            with builddir.reserve_and_track() as builddir_path:
                pass
        self.logger.debug(
            "Cache common model data to a build directory: {}", builddir_path
        )

        self.logger.debug("Retrieve candidates of dataset: {}", dataset_query)
        dsdict = self.dataset_actor.run_dataset(dataset_query)

        if for_training:
            # for training, we always use an oracle entity recognition to generate the candidates
            # as the entity recognition model may not produce the correct entity columns
            cg_dsdict = self.train_cangen_actor.run_dataset(dataset_query)
        else:
            cg_dsdict = self.cangen_actor.run_dataset(dataset_query)

        # # fmt: off
        # from pathlib import Path
        # Path("/tmp/test.csv").write_text("\n".join(cangen_dsdict['train'].id))
        # # fmt: on
        self.logger.debug("Generate dataset: {}", dataset_query)
        cr_dsdict = MyDatasetDict(parsed_dsquery.dataset, {})
        for split, candidates in cg_dsdict.items():
            self.logger.debug("\tSubset: {}", split)
            examples = dsdict[split]
            myds, newcans = method.generate_dataset(
                examples,
                candidates,
                num_proc=os.cpu_count(),
                for_training=for_training,
                cache_dir=builddir_path / split,
                return_candidates=True,
            )
            # uncomment for debugging purpose
            # setattr(myds, "candidates", newcans)
            cr_dsdict[split] = myds

        return cr_dsdict

    def get_cache_key(
        self: CRModelDataActor,
        method: CandidateRankingMethod,
        dsquery: str,
        for_training: bool,
        cg_provenance: str,
    ):
        deps = [actor.get_actor_state() for actor in self.dep_actors]
        state = ActorState.create(
            method.__class__, method.get_generating_dataset_args(), dependencies=deps
        )
        return orjson_dumps(
            {
                "state": state.to_dict(),
                "dsquery": dsquery,
                "for_training": for_training,
                "cg_provenance": cg_provenance,
            }
        )

    def get_cache_dirname(
        self: CRModelDataActor,
        method: CandidateRankingMethod,
        dsquery: str,
        for_training: bool,
        cg_provenance: str,
    ):
        return slugify(
            f"{method.__class__.__name__}_{getattr(method, 'VERSION')}_{dsquery}_{for_training}"
        ).replace("-", "_")
