from __future__ import annotations
import enum
from collections.abc import Mapping, Sequence
from grams.algorithm.literal_matchers.text_parser import TextParser
import numpy as np
from nptyping import Float64, NDArray, Shape, Int32
from ream.data_model_helper import NumpyDataModel
from ned.data_models.pymodels import NEDExample


class ERFeature(str, enum.Enum):
    cardinality = "cardinality"
    percent_num = "percent_num"
    text_length = "text_length"


class FeatureVector:
    def __init__(self, features: list[enum.Enum]):
        self.features = features
        self.feat2index = {feat: i for i, feat in enumerate(features)}
        self.base_vec = np.ones((len(features),), dtype=np.float64) * -1

    def sequence2vec(self, feat_values: Sequence[tuple[enum.Enum, float]]):
        vec = self.base_vec.copy()
        for feat, value in feat_values:
            vec[self.feat2index[feat]] = value
        return vec

    def mapping2vec(self, feat_values: Mapping[enum.Enum, float]):
        vec = self.base_vec.copy()
        for feat, value in feat_values.items():
            vec[self.feat2index[feat]] = value
        return vec


class ERFeatureStore(NumpyDataModel):
    __slots__ = ["id", "features", "label"]
    id: NDArray[Shape["*"], Int32]
    features: NDArray[Shape["*,*"], Float64]
    label: NDArray[Shape["*"], Int32]

    feature_vector = FeatureVector(
        [
            ERFeature.cardinality,
            ERFeature.percent_num,
            ERFeature.text_length,
        ]
    )

    @staticmethod
    def create(examples: list[NEDExample]):
        text_parser = TextParser.default()

        ids = []
        X = []
        y = []

        # the order of id is very important for later process to put the results back
        count = 0
        for example in examples:
            id = example.table.table_id
            entity_columns = set(example.entity_columns)

            for ci, col in enumerate(example.table.columns):
                label = ci in entity_columns
                values = [text_parser.parse(value) for value in col.values]
                unique_values = {value.normed_string for value in values}
                n_num = sum(1 for value in values if value.number is not None)

                feat = ERFeatureStore.feature_vector.sequence2vec(
                    [
                        (ERFeature.cardinality, len(unique_values) / len(values)),
                        (ERFeature.percent_num, n_num / len(values)),
                        (
                            ERFeature.text_length,
                            sum([len(x) for x in unique_values]) / len(unique_values),
                        ),
                    ]
                )

                ids.append(count)
                X.append(feat)
                y.append(label)
                count += 1

        return ERFeatureStore(
            np.asarray(ids, dtype=np.int32),
            np.stack(X, axis=0),
            np.asarray(y, dtype=np.int32),
        )


ERFeatureStore.init()
