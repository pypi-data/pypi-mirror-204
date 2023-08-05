from __future__ import annotations

import os
import pickle
from dataclasses import dataclass, field
from functools import partial
from typing import Literal, Optional

from loguru import logger
from osin.integrations.ream import OsinActor
from ream.actors.base import BaseActor
from ream.cache_helper import CacheArgsHelper
from ream.fs import ItemStatus
from ream.helper import orjson_dumps
from ream.prelude import (
    ActorState,
    Cache,
    DatasetDict,
    DatasetQuery,
    EnumParams,
    NoParams,
)
from slugify import slugify

from ned.actors.dataset.prelude import NEDDatasetActor, NEDDatasetDict
from ned.actors.evaluate_helper import EvalArgs
from ned.candidate_ranking.helpers.dataset import MyDatasetDict
from ned.candidate_ranking.helpers.training_helper import ModifiedTrainingArguments
from ned.data_models.prelude import NEDExample
from ned.entity_recognition.ensemble_model import EnsembleModel, EnsembleModelArgs
from ned.entity_recognition.er_model_interface import ERModelInterface
from ned.entity_recognition.oracle_model import OracleERModel, OracleERModelArgs
from ned.entity_recognition.training import sklearn_train
from sm.misc.funcs import assert_not_null, get_incremental_path


@dataclass
class ERParams(EnumParams):
    method: Literal["ensemble", "oracle"] = field(
        metadata={
            "help": "Candidate generation method",
            "variants": {
                "ensemble": EnsembleModel,
                "oracle": OracleERModel,
            },
        }
    )
    ensemble: Optional[EnsembleModelArgs] = field(default_factory=EnsembleModelArgs)
    oracle: Optional[OracleERModelArgs] = field(default_factory=OracleERModelArgs)
    training: Optional[ModifiedTrainingArguments] = field(
        default_factory=ModifiedTrainingArguments
    )


class EntityRecognitionActor(OsinActor[NEDExample, ERParams]):
    EXP_NAME = "Entity Column Recognition"
    VERSION = 110
    EXP_VERSION = 1

    def __init__(self, params: ERParams, dataset_actor: NEDDatasetActor):
        model_data_actor = ERModelDataActor(dataset_actor)
        super().__init__(params, [dataset_actor, model_data_actor])
        self.dataset_actor = dataset_actor
        self.model_data_actor = model_data_actor

    def run(self, example: NEDExample) -> list[int]:
        return self.batch_run([example])[0]

    def batch_run(self, examples: list[NEDExample]):
        method, provenance = self.get_trained_method()
        return method.predict_data(examples, method.gen_data(examples))

    def get_provenance(self):
        method, provenance = self.get_trained_method()
        return provenance

    @Cache.mem(cache_self_args=CacheArgsHelper.gen_cache_self_args(get_provenance))
    def run_dataset(self, query: str):
        dsquery = DatasetQuery.from_string(query)
        dsdict: DatasetDict[list[list[int]]] = DatasetDict(
            dsquery.dataset, {}, provenance=self.get_provenance()
        )
        for subset, sub_dsquery in dsquery.iter_subset():
            tmp_dsdict = self._run_dataset(sub_dsquery.strip().get_query())
            dsdict[subset] = tmp_dsdict[""]
            assert tmp_dsdict.provenance == dsdict.provenance
        return dsdict

    @Cache.cls.dir(
        cls=DatasetDict,
        cache_self_args=CacheArgsHelper.gen_cache_self_args(get_provenance),
        mem_persist=True,
        dirname=lambda self, query: DatasetQuery.from_string(query).dataset,
        compression="lz4",
        log_serde_time=True,
    )
    def _run_dataset(self, query: str):
        method, provenance = self.get_trained_method()
        dsdict = self.dataset_actor.run_dataset(query)
        method_dsdict = self.model_data_actor.run_dataset(
            method, query, for_training=False
        )
        out: DatasetDict[list[list[int]]] = DatasetDict(
            dsdict.name, {}, provenance=provenance
        )
        for name, ds in method_dsdict.items():
            examples = dsdict[name]
            out[name] = method.predict_data(examples, method_dsdict[name])

        return out

    def evaluate(self, evalargs: EvalArgs):
        retrain = int(os.environ.get("ER_RETRAIN", "0")) == 1
        method, provenance = self.get_trained_method(retrain)

        for dsquery in evalargs.dsqueries:
            self.logger.debug("Running evaluation on dataset {}", dsquery)
            self.run_dataset(dsquery)

    @Cache.mem()
    def get_trained_method(self, retrain: bool = False) -> tuple[ERModelInterface, str]:
        method = self.get_method()
        if isinstance(method, OracleERModel):
            return method, "oracle"

        wfs = self.get_working_fs()
        model_file = wfs.get("model.pkl")

        if not model_file.exists() or retrain:
            # train the model again or resume training
            method = sklearn_train(
                method,
                self.model_data_actor.run_dataset,
                assert_not_null(self.params.training),
                ["precision", "recall", "f1"],
            )

            dir = get_incremental_path(wfs.root / "training_v")
            trained_file = dir / "model.pkl"
            with open(trained_file, "wb") as f:
                pickle.dump(method.state_dict(), f)

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
            with open(model_file.get(), "rb") as f:
                method.load_state_dict(pickle.load(f))

        provenance = os.path.realpath(model_file.get())
        provenance = os.path.relpath(provenance, wfs.root)
        return method, provenance

    def get_method(self):
        if self.params.method == "ensemble":
            return EnsembleModel(assert_not_null(self.params.ensemble))
        if self.params.method == "oracle":
            return OracleERModel(assert_not_null(self.params.oracle))
        raise NotImplementedError()


class ERModelDataActor(BaseActor[str, NoParams]):
    VERSION = 100

    def __init__(self, dataset_actor: NEDDatasetActor):
        super().__init__(NoParams(), [dataset_actor])
        self.dataset_actor = dataset_actor

    def run_dataset(
        self, method: ERModelInterface, dataset_query: str, for_training: bool
    ):
        return self.gen_data(method, dataset_query, for_training)

    def gen_data(
        self, method: ERModelInterface, dataset_query: str, for_training: bool
    ):
        parsed_dsquery = DatasetQuery.from_string(dataset_query)

        # a build directory that is unique to the dataset query and can be shared across methods
        builddir = self.get_working_fs().get(
            "build_" + parsed_dsquery.dataset, {"query": dataset_query}, save_key=True
        )
        if builddir.exists():
            builddir_path = builddir.get()
        else:
            with builddir.reserve_and_track() as builddir_path:
                pass

        self.logger.debug(
            "Cache common model data to a build directory: {}", builddir_path
        )
        dsdict = self.dataset_actor.run_dataset(dataset_query)
        out = MyDatasetDict(parsed_dsquery.dataset, {})
        for split, ds in dsdict.items():
            out[split] = method.gen_data(ds, for_training=for_training)

        return out

    def get_cache_key(
        self,
        method: ERModelInterface,
        dataset_query: str,
        for_training: bool,
    ):
        deps = [actor.get_actor_state() for actor in self.dep_actors]
        state = ActorState.create(
            method.__class__, method.get_gen_data_args(), dependencies=deps
        )
        return orjson_dumps(
            {
                "state": state.to_dict(),
                "dsquery": dataset_query,
                "for_training": for_training,
            }
        )

    def get_cache_dirname(
        self,
        method: ERModelInterface,
        dataset_query: str,
        for_training: bool,
    ):
        return slugify(
            f"{method.__class__.__name__}_{getattr(method, 'VERSION')}_{DatasetQuery.from_string(dataset_query).dataset}_{for_training}"
        ).replace("-", "_")


ERModelDataActor.run_dataset = Cache.cls.dir(
    cls=MyDatasetDict,
    cache_key=ERModelDataActor.get_cache_key,
    dirname=ERModelDataActor.get_cache_dirname,
    compression="lz4",
)(ERModelDataActor.run_dataset)
