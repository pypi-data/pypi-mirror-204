from __future__ import annotations
from ned.data_models.pymodels import NEDExample
from ned.entity_recognition.model_data.feature_store import ERFeatureStore, ERFeature

from ream.cache_helper import Cache, Cacheable, unwrap_cache_decorators


class ERModelData(Cacheable):
    """Prepare data for entity recognition models."""

    @Cache.cls.file(
        cls=ERFeatureStore,
        cache_args=[],
        mem_persist=True,
        fileext="parq",
        compression="lz4",
    )
    def feature_store(self, examples: list[NEDExample]) -> ERFeatureStore:
        return ERFeatureStore.create(examples)


class NoCacheERModelData(ERModelData):
    def __init__(self):
        pass


unwrap_cache_decorators(NoCacheERModelData)


__all__ = ["ERModelData", "NoCacheERModelData", "ERFeature"]
