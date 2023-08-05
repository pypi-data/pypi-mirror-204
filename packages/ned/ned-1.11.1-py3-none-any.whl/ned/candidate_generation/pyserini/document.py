import copy
from typing import Any, Literal, Callable
from dataclasses import dataclass
from kgdata.wikidata.models.multilingual import MultiLingualStringList
from kgdata.wikidata.models.wdentity import WDEntity

import orjson


@dataclass
class LuceneDocument:
    """Represent a document about an entity stored in Lucene."""

    id: str
    label: str
    aliases: str
    description: str
    body: str
    popularity: float

    def pretokenize(self, analyzer: Callable[[str], str]):
        self.label = analyzer(self.label)
        self.aliases = analyzer(self.aliases)
        self.description = analyzer(self.description)
        self.body = analyzer(self.body)
        return self

    def set(
        self,
        field: Literal["id", "label", "aliases", "description", "body", "popularity"],
        value: Any,
    ):
        self.__dict__[field] = value
        return self

    def to_dict(self):
        return {
            "id": self.id,
            "contents": self.label,
            "aliases": self.aliases,
            "description": self.description,
            "popularity": self.popularity,
            "body": self.body,
        }

    def to_json(self):
        return orjson.dumps(self.to_dict())

    @staticmethod
    def from_dict(d):
        return LuceneDocument(
            d["id"],
            d["contents"],
            d["aliases"],
            d["description"],
            d["body"],
            d["popularity"],
        )

    @staticmethod
    def from_entity(entity: WDEntity, popularity: float):
        label = str(entity.label)
        aliases = MultiLingualStringList(
            copy.deepcopy(entity.aliases.lang2values), entity.aliases.lang
        )
        for lang, value in entity.label.lang2value.items():
            if lang != entity.label.lang:
                if lang not in aliases.lang2values[lang]:
                    aliases.lang2values[lang] = []
                aliases.lang2values[lang].append(value)

        return LuceneDocument(
            id=entity.id,
            label=label,
            description=str(entity.description),
            aliases=StringEncoder.encode_multilingual_string_list(aliases),
            body="",
            popularity=popularity,
        )


class StringEncoder:
    SEP_TOKEN = "\n"
    ESCAPE_SEP_TOKEN = "\\-n"

    @classmethod
    def encode_multilingual_string_list(cls, aliases: MultiLingualStringList):
        main_lang = ""
        other_langs = {}
        for lang, values in aliases.lang2values.items():
            assert all(cls.SEP_TOKEN not in v for v in values)
            newvalues = cls.SEP_TOKEN.join(
                value.replace(cls.SEP_TOKEN, cls.ESCAPE_SEP_TOKEN) for value in values
            )
            if lang == aliases.lang:
                main_lang = f"{lang}: {newvalues}"
            else:
                other_langs[lang] = f"{lang}: {newvalues}"

        out = [main_lang]
        out.extend(other_langs.values())
        return (cls.SEP_TOKEN + cls.SEP_TOKEN).join(out)

    @classmethod
    def decode_multilingual_string_list(cls, aliases: str) -> MultiLingualStringList:
        lst = aliases.split(cls.SEP_TOKEN + cls.SEP_TOKEN)
        lang2values = []
        for item in lst:
            lang, values = item.split(": ", 1)
            values = [
                v.replace(cls.ESCAPE_SEP_TOKEN, cls.SEP_TOKEN)
                for v in values.split(cls.SEP_TOKEN)
            ]
            lang2values.append((lang, values))

        if len(lang2values) == 0:
            return MultiLingualStringList({}, "en")
        return MultiLingualStringList(dict(lang2values), lang2values[0][0])
