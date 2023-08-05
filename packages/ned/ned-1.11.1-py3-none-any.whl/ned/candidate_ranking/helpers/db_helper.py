from __future__ import annotations
from pathlib import Path

from typing import Iterable, Literal, overload
from kgdata.wikidata.db import WikidataDB
from kgdata.wikidata.extra_ent_db import get_multilingual_key

from sm.misc.ray_helper import get_instance


@overload
def _gather_entities_attr(
    database_dir: Path, ent_ids: Iterable[str], attr: Literal["instanceof"]
) -> dict[str, list[str]]:
    ...


@overload
def _gather_entities_attr(
    database_dir: Path, ent_ids: Iterable[str], attr: Literal["label"]
) -> dict[str, str]:
    ...


def _gather_entities_attr(
    database_dir: Path, ent_ids: Iterable[str], attr: Literal["label", "instanceof"]
) -> dict[str, str] | dict[str, list[str]]:
    if attr == "label":
        db = get_instance(
            lambda: WikidataDB(database_dir).wdattr(attr),
            f"ned.candidate_ranking.dataset.gather_entities.{attr}",
        ).cache()
        return {eid: db[get_multilingual_key(eid, "en")] for eid in ent_ids}

    db = get_instance(
        lambda: WikidataDB(database_dir).wdattr(attr),
        f"ned.candidate_ranking.dataset.gather_entities.{attr}",
    ).cache()
    return {eid: db[eid] for eid in ent_ids}
