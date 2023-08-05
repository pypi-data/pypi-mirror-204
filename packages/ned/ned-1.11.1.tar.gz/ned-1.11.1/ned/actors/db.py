from dataclasses import dataclass
from pathlib import Path
from typing import Union
from kgdata.wikidata.db import WikidataDB
from functools import cached_property

from ream.actors.base import BaseActor
from sm.misc.ray_helper import get_instance


@dataclass
class DBActorParams:
    data_dir: Path


class DBActor(BaseActor[str, DBActorParams]):
    VERSION = 100

    def __init__(self, params: DBActorParams):
        super().__init__(params)
        self.db = WikidataDB(params.data_dir)

    @cached_property
    def entities(self):
        return self.db.wdentities.cache()

    @cached_property
    def pagerank(self):
        return self.db.wdpagerank.cache()

    @cached_property
    def props(self):
        return self.db.wdprops.cache()

    @cached_property
    def classes(self):
        return self.db.wdclasses.cache()


def to_wikidata_db(db: Union[WikidataDB, Path]):
    if isinstance(db, Path):
        datadir = db
        db = get_instance(
            lambda: WikidataDB(datadir),
            f"WikidataDB[{datadir}]",
        )
    return db
