from __future__ import annotations
import enum
from operator import itemgetter
import re, pickle

from typing import Union
import numpy as np
import orjson
import ray
from nptyping import Float64, NDArray, Shape, Object
from ream.data_model_helper import NumpyDataModel
from tqdm import tqdm
from ned.data_models.pymodels import Entity
from sm.misc.funcs import batch, filter_duplication
from sm.misc.ray_helper import ray_map
import rltk.similarity as sim
from scipy.optimize import linear_sum_assignment


class CRDatasetFeatures(NumpyDataModel):
    __slots__ = ["features"]
    # if this hold candidate features (from DatasetCandidateEntities), then the order of this object and candidates are the same
    # if this hold entity features (CRDatasetEnt), then the order of this object and entities are the same
    features: NDArray[Shape["*,*"], Float64]

    @staticmethod
    def create(
        cell: NDArray[Shape["*"], Object],
        entity_label: NDArray[Shape["*"], Object],
        entity_aliases: NDArray[Shape["*"], Object],
        entity_popularity: NDArray[Shape["*"], Float64],
    ):
        features = ray_map(
            extract_features,
            batch(512, cell, entity_label, entity_aliases, entity_popularity),
            verbose=True,
            desc="extract features",
            is_func_remote=False,
        )
        features = np.concatenate(features, axis=0)
        return CRDatasetFeatures(features)


CRDatasetFeatures.init()


def extract_features(
    cells: np.ndarray,
    labels: np.ndarray,
    aliases: np.ndarray,
    popularities: np.ndarray,
):
    feats = []

    for i in range(len(labels)):
        cell = cells[i]

        feat = np.zeros((N_PAIRWISE_FEATURES + N_EXTRA_FEATURES,), dtype=np.float64)
        label_feat = extract_pairwise_features_v1(cell, labels[i])
        for alias in orjson.loads(aliases[i]):
            label_feat = np.maximum(
                label_feat, extract_pairwise_features_v1(cell, alias)
            )

        feat[:N_PAIRWISE_FEATURES] = label_feat
        feat[N_PAIRWISE_FEATURES] = popularities[i]
        feats.append(feat)

    return np.array(feats, dtype=np.float64)


# number of extracted pairwise features
# for setting default gold_features for NIL entity
# one extra feature is added from pagerank
class PairwiseFeatures(enum.Enum):
    levenshtein_sim = 0
    jaro_winkler_sim = 1
    monge_elkan_sim = 2
    sym_monge_elkan_sim = 3
    hybrid_jaccard_sim = 4
    numeric_sym_monge_elkan_sim = 5
    numeric_hybrid_jaccard_sim = 6


N_PAIRWISE_FEATURES = len(list(PairwiseFeatures))
N_EXTRA_FEATURES = 1


def extract_pairwise_features_v1(text: str, entity_label: str):
    """Extract feature from mention and entity.

    When this function is changed, the version number should be updated in this function and all step functions
    """
    text_tokens = text.split(" ")
    entity_label_tokens = entity_label.split(" ")

    unique_text_tokens = filter_duplication(text_tokens)
    unique_entity_label_tokens = filter_duplication(entity_label_tokens)

    monge_elkan_score = sim.monge_elkan_similarity(text_tokens, entity_label_tokens)
    sym_monge_elkan_score = sim.symmetric_monge_elkan_similarity(
        text_tokens, entity_label_tokens
    )
    hybrid_jaccard_score = hybrid_jaccard_similarity(
        unique_text_tokens, unique_entity_label_tokens
    )

    return [
        sim.levenshtein_similarity(text, entity_label),
        sim.jaro_winkler_similarity(
            text, entity_label, threshold=0.7, scaling_factor=0.1, prefix_len=4
        ),
        monge_elkan_score,
        sym_monge_elkan_score,
        hybrid_jaccard_score,
        does_ordinal_match(text, entity_label, sym_monge_elkan_score, 0.7),
        does_ordinal_match(text, entity_label, hybrid_jaccard_score, 0.7),
    ]


def does_ordinal_match(s1: str, s2: str, sim: float, threshold: float) -> float:
    """Test for strings containing ordinal categorical values such as Su-30 vs Su-25, 29th Awards vs 30th Awards.

    Args:
        s1: Cell Label
        s2: Entity Label
    """
    if sim < threshold:
        return 0.4
    digit_tokens_1 = re.findall(r"\d+", s1)
    if len(digit_tokens_1) == 0:
        return 0.4

    digit_tokens_2 = re.findall(r"\d+", s2)
    if digit_tokens_1 == digit_tokens_2:
        return 1.0
    return 0.0


# copy from rltk.hybrid module to fix unnecessary type check
# so that set1 and set2 can be a sequence. since using slightly changing order of tokens can
# change the similarity score. Is it a bug?
def hybrid_jaccard_similarity(
    set1,
    set2,
    threshold=0.5,
    function=sim.jaro_winkler_similarity,
    parameters=None,
    lower_bound=None,
):
    """
    Generalized Jaccard Measure.

    Args:
        set1 (set): Set 1.
        set2 (set): Set 2.
        threshold (float, optional): The threshold to keep the score of similarity function. \
            Defaults to 0.5.
        function (function, optional): The reference of a similarity measure function. \
            It should return the value in range [0,1]. If it is set to None, \
            `jaro_winlker_similarity` will be used.
        parameters (dict, optional): Other parameters of function. Defaults to None.
        lower_bound (float): This is for early exit. If the similarity is not possible to satisfy this value, \
            the function returns immediately with the return value 0.0. Defaults to None.

    Returns:
        float: Hybrid Jaccard similarity.

    Examples:
        >>> def hybrid_test_similarity(m ,n):
        ...     ...
        >>> rltk.hybrid_jaccard_similarity(set(['a','b','c']), set(['p', 'q']), function=hybrid_test_similarity)
        0.533333333333
    """

    parameters = parameters if isinstance(parameters, dict) else {}

    if len(set1) > len(set2):
        set1, set2 = set2, set1
    total_num_matches = len(set1)

    matching_score = [[1.0] * len(set2) for _ in range(len(set1))]
    row_max = [0.0] * len(set1)
    for i, s1 in enumerate(set1):
        for j, s2 in enumerate(set2):
            score = function(s1, s2, **parameters)
            if score < threshold:
                score = 0.0
            row_max[i] = max(row_max[i], score)
            matching_score[i][j] = 1.0 - score  # munkres finds out the smallest element

        if lower_bound:
            max_possible_score_sum = sum(
                row_max[: i + 1] + [1] * (total_num_matches - i - 1)
            )
            max_possible = (
                1.0
                * max_possible_score_sum
                / float(len(set1) + len(set2) - total_num_matches)
            )
            if max_possible < lower_bound:
                return 0.0

    # run munkres, finds the min score (max similarity) for each row
    row_idx, col_idx = linear_sum_assignment(matching_score)

    # recover scores
    score_sum = 0.0
    for r, c in zip(row_idx, col_idx):
        score_sum += 1.0 - matching_score[r][c]

    if len(set1) + len(set2) - total_num_matches == 0:
        return 1.0
    sim = float(score_sum) / float(len(set1) + len(set2) - total_num_matches)
    if lower_bound and sim < lower_bound:
        return 0.0
    return sim
