from dataclasses import dataclass
from functools import partial
import os, yada
from sm.misc.funcs import assert_not_null
from kgdata.dataset import Dataset
from kgdata.wikidata.datasets.properties import properties
from kgdata.wikidata.models.multilingual import (
    MultiLingualString,
)
import orjson
from kgdata.wikidata.models.wdvalue import WDValue
from kgdata.wikidata.models.wdentity import WDEntity
from kgdata.wikidata.datasets.entities import entities
from pathlib import Path
from typing import Iterable, Literal, Optional, TypeVar, Union, cast
from kgdata.spark import (
    EmptyBroadcast,
    does_result_dir_exist,
    get_spark_context,
    left_outer_join_repartition,
)
from kgdata.wikidata.config import WDDataDirCfg
from kgdata.wikidata.datasets.entity_metadata import entity_metadata
from kgdata.wikidata.datasets.entity_pagerank import entity_pagerank
from ned.candidate_generation.pyserini.configuration import IndexSettings
from ned.candidate_generation.pyserini.document import LuceneDocument, StringEncoder
from pyspark import RDD
from ned.data_models.pymodels import Entity
from jnius import autoclass
import serde.json


V = TypeVar("V")


@dataclass
class BuildIndexArgs:
    dataset: Literal[
        "wikidata.entity", "wikidata.entity.extended_v0", "wikidata.entity.extended_v1"
    ]
    data_dir: Path
    index_dir: Path
    settings: IndexSettings
    n_files: int = 256
    optimize: bool = False
    shuffle: bool = True

    def get_dataset(self) -> RDD[LuceneDocument]:
        if self.dataset == "wikidata.entity":
            return self.get_wikidata_entity_dataset()
        if self.dataset == "wikidata.entity.extended_v0":
            return self.get_wikidata_entity_extended_dataset_v0()
        if self.dataset == "wikidata.entity.extended_v1":
            return self.get_wikidata_entity_extended_dataset_v1()
        raise NotImplementedError(self.dataset)

    def get_wikidata_entity_dataset(self, lang: str = "en"):
        WDDataDirCfg.init(os.environ["WD_DIR"])

        return (
            entity_metadata(lang=lang)
            .get_rdd()
            .map(
                lambda r: LuceneDocument(
                    id=r.id,
                    label=str(r.label),
                    description=str(r.description),
                    aliases=Entity.encode_aliases(r.aliases),
                    body="",
                    popularity=1,
                )
            )
            .map(lambda x: (x.id, x))
            .leftOuterJoin(entity_pagerank(lang=lang).get_rdd())
            .map(lambda x: x[1][0].set("popularity", x[1][1] or 0.0))
            .filter(lambda doc: doc.label.strip() != "")
        )

    def get_wikidata_entity_extended_dataset_v0(
        self, lang: str = "en"
    ) -> RDD[LuceneDocument]:
        """Build a full wikidata index that:

        - all properties' values are concatenated to store in the body field
        - the original aliases and labels in different languages (except for label in the default language) are merged and stored in the aliases field
        """
        WDDataDirCfg.init(os.environ["WD_DIR"])

        def entity_to_partial_doc(entity: WDEntity) -> dict:
            label = str(entity.label)
            aliases = entity.aliases
            for lang, value in entity.label.lang2value.items():
                if lang != entity.label.lang:
                    if lang not in aliases.lang2values:
                        aliases.lang2values[lang] = []
                    aliases.lang2values[lang].append(value)
            return {
                "id": entity.id,
                "contents": label,
                "aliases": StringEncoder.encode_multilingual_string_list(aliases),
                "description": str(entity.description),
            }

        def set_prop(obj: dict, name: str, value: Union[str, float]) -> dict:
            obj[name] = value
            return obj

        ent_popularity = entity_pagerank(lang=lang).get_rdd()
        ent_body = self.get_wikidata_entity_body(lang).get_rdd()

        return (
            entities(lang)
            .get_rdd()
            .map(entity_to_partial_doc)
            .map(lambda x: (x["id"], x))
            .leftOuterJoin(ent_popularity)
            .map(
                lambda x: (
                    x[0],
                    set_prop(
                        x[1][0], "popularity", x[1][1] if x[1][1] is not None else 0.0
                    ),
                )
            )
            .leftOuterJoin(ent_body)
            .map(lambda x: (x[0], set_prop(x[1][0], "body", assert_not_null(x[1][1]))))
            .map(lambda x: LuceneDocument.from_dict(x[1]))
        )

    def get_wikidata_entity_extended_dataset_v1(
        self, lang: str = "en"
    ) -> RDD[LuceneDocument]:
        """Build a full wikidata index that:

        - all properties' values are concatenated to store in the body field
        - the original aliases and labels in different languages (except for label in the default language) are merged and stored in the aliases field
        """
        WDDataDirCfg.init(os.environ["WD_DIR"])

        def entity_to_partial_doc(entity: WDEntity) -> dict:
            label = str(entity.label)

            # to fix issue of duplicating aliases
            aliases = set(entity.label.lang2value.values())
            for lang, values in entity.aliases.lang2values.items():
                aliases.update(values)

            # extra aliases from properties such as country codes
            extra_aliases = ["P984", "P3441"]
            for pid in extra_aliases:
                if pid in entity.props:
                    for stmt in entity.props[pid]:
                        if WDValue.is_string(stmt.value):
                            aliases.add(stmt.value.value)

            if label in aliases:
                aliases.remove(label)

            return {
                "id": entity.id,
                "contents": label,
                "aliases": " | ".join(sorted(aliases)),
                "description": str(entity.description),
            }

        def set_prop(obj: dict, name: str, value: Union[str, float]) -> dict:
            obj[name] = value
            return obj

        ent_popularity = entity_pagerank(lang=lang).get_rdd()
        ent_body = self.get_wikidata_entity_body(lang).get_rdd()

        return (
            entities(lang)
            .get_rdd()
            .filter(lambda x: "Q13442814" not in x.instance_of())
            .map(entity_to_partial_doc)
            .map(lambda x: (x["id"], x))
            .leftOuterJoin(ent_popularity)
            .map(
                lambda x: (
                    x[0],
                    set_prop(
                        x[1][0], "popularity", x[1][1] if x[1][1] is not None else 0.0
                    ),
                )
            )
            .leftOuterJoin(ent_body)
            .map(lambda x: (x[0], set_prop(x[1][0], "body", assert_not_null(x[1][1]))))
            .map(lambda x: LuceneDocument.from_dict(x[1]))
        )

    def get_wikidata_entity_body(self, lang: str = "en") -> Dataset[tuple[str, str]]:
        step1_dir = self.data_dir.parent / "resolved_entity_labels"
        step2_dir = self.data_dir.parent / "entity_body"

        def get_outgoing_entity(entity: WDEntity) -> list[tuple[str, str]]:
            internal_ids = set()
            for pid, stmts in entity.props.items():
                for stmt in stmts:
                    if WDValue.is_entity_id(stmt.value):
                        internal_ids.add(stmt.value.as_entity_id())
                    for qid, qvals in stmt.qualifiers.items():
                        for qval in qvals:
                            if WDValue.is_entity_id(qval):
                                internal_ids.add(qval.as_entity_id())

            return [(id, entity.id) for id in internal_ids]

        def swap_direction(
            args: tuple[str, tuple[Iterable[str], Optional[MultiLingualString]]]
        ) -> list[tuple[str, tuple[str, MultiLingualString]]]:
            id, (incoming_entities, label) = args
            if label is None:
                raise Exception(
                    f"{id} does not exist but is referenced by {list(incoming_entities)[:10]}."
                )
            return [(entid, (id, label)) for entid in incoming_entities]

        if not does_result_dir_exist(step2_dir):
            bc_props = get_spark_context().broadcast(
                dict(
                    properties(lang)
                    .get_rdd()
                    .map(lambda x: (x.id, str(x.label)))
                    .collect()
                )
            )
        else:
            bc_props = EmptyBroadcast(cast(dict[str, str], {}))

        def wdvalue_to_str(value: WDValue, id2label: dict[str, str]) -> str:
            if WDValue.is_entity_id(value):
                return id2label[value.as_entity_id()]
            elif WDValue.is_quantity(value):
                return value.value["amount"] + " " + value.value["unit"]
            elif WDValue.is_string(value):
                return value.value
            elif WDValue.is_mono_lingual_text(value):
                return value.value["text"]
            elif WDValue.is_time(value):
                return value.value["time"]
            return ""

        def build_entity_body(
            args: tuple[str, tuple[WDEntity, Optional[list[tuple[str, str]]]]]
        ) -> tuple[str, str]:
            id, (entity, outgoing_labels) = args
            if outgoing_labels is None:
                id2label = {}
            else:
                id2label = dict(outgoing_labels)

            output = []
            for pid, stmts in entity.props.items():
                stmt_output = []
                for stmt in stmts:
                    stmt_value = wdvalue_to_str(stmt.value, id2label)
                    if stmt_value == "":
                        continue

                    if len(stmt.qualifiers) > 0:
                        qual_output = []
                        for qid, qvals in stmt.qualifiers.items():
                            qserval = ", ".join(
                                [
                                    s
                                    for qval in qvals
                                    if (s := wdvalue_to_str(qval, id2label)) != ""
                                ]
                            )
                            if qserval != "":
                                qual_output.append(bc_props.value[qid] + ": " + qserval)

                        if len(qual_output) > 0:
                            qual_value = ", ".join(qual_output)
                            stmt_value = f"{stmt_value} ({qual_value})"
                    stmt_output.append(stmt_value)
                if len(stmt_output) > 0:
                    output.append(bc_props.value[pid] + ": ")
                    output.append(", ".join(stmt_output))
                    output.append("\n")
            return id, "".join(output)

        ent_rdd = entities(lang).get_rdd()

        if not does_result_dir_exist(step1_dir):
            (
                left_outer_join_repartition(
                    ent_rdd.flatMap(get_outgoing_entity),
                    entity_metadata(lang).get_rdd().map(lambda x: (x.id, x.label)),
                )
                .flatMap(swap_direction)
                .groupByKey()
                .map(lambda x: (x[0], list(x[1])))
                .map(orjson.dumps)
                .saveAsTextFile(
                    str(step1_dir),
                    compressionCodecClass="org.apache.hadoop.io.compress.GzipCodec",
                )
            )

        if not does_result_dir_exist(step2_dir):
            (
                ent_rdd.map(lambda x: (x.id, x))
                .leftOuterJoin(
                    get_spark_context().textFile(str(step1_dir)).map(orjson.loads)
                )
                .map(build_entity_body)
                .map(orjson.dumps)
                .saveAsTextFile(
                    str(step2_dir),
                    compressionCodecClass="org.apache.hadoop.io.compress.GzipCodec",
                )
            )

        return Dataset(str(step2_dir / "*.gz"), deserialize=orjson.loads)


def build_sparse_index(
    dataset_name: str,
    dataset: RDD[LuceneDocument],
    data_dir: Union[str, Path],
    index_dir: Union[str, Path],
    settings: IndexSettings,
    n_files: int,
    optimize: bool,
    shuffle: bool,
):
    """Build a pyserini index from the given dataset.

    Args:
        dataset_name: name of the dataset
        dataset: The dataset to build the index from.
        data_dir: The directory to store the serialized docs.
        index_dir: The directory to store the index.
        settings: The settings to use for the index.
        n_files: The number of files to store the docs (to avoid huge number of files).
        optimize: Whether to optimize the index.
    """
    data_dir = Path(data_dir)
    index_dir = Path(index_dir)

    if not does_result_dir_exist(data_dir):
        if settings.analyzer.need_pretokenize():
            dataset = dataset.map(
                partial(LuceneDocument.pretokenize, analyzer=settings.get_analyzer())
            )

        rdd = dataset.map(LuceneDocument.to_json)
        if n_files > 0:
            rdd = rdd.coalesce(n_files, shuffle=shuffle)
        rdd.saveAsTextFile(str(data_dir))

        for file in Path(data_dir).iterdir():
            if file.name.startswith("part-"):
                file.rename(file.parent / f"{file.stem}.jsonl")

        serde.json.ser(settings.to_dict(), data_dir / "_SUCCESS", indent=2)
        serde.json.ser(
            dict(
                data_dir=str(data_dir),
                index_dir=str(index_dir),
                dataset=dataset_name,
                settings=settings.to_dict(),
            ),
            data_dir / "_METADATA",
            indent=2,
        )
    else:
        assert (
            IndexSettings.from_dict(serde.json.deser(data_dir / "_SUCCESS")) == settings
        )

    if not does_result_dir_exist(index_dir):
        index_dir.mkdir(parents=True, exist_ok=True)
        extra_args = []
        if settings.analyzer.need_pretokenize():
            extra_args.append(f"-pretokenized")

        if optimize:
            extra_args.append("-optimize")

        JIndexCollection = autoclass("io.anserini.index.IndexCollection")
        JIndexCollection.main(
            [
                "-collection",
                "JsonCollection",
                "-input",
                str(data_dir),
                "-index",
                str(index_dir),
                "-generator",
                "EnhancedLuceneDocumentGenerator",
                "-storePositions",
                "-storeDocvectors",
                "-storeRaw",
                "-threads",
                str(os.cpu_count()),
                "-memorybuffer",
                "8192",
                "-fields",
                "aliases description body",
                "-floatFields",
                "popularity",
                "-featureFields",
                "popularity",
            ]
            + extra_args
        )
        (index_dir / "_SUCCESS").touch()
        serde.json.ser(settings.to_dict(), index_dir / "_SUCCESS", indent=2)
    else:
        assert (
            IndexSettings.from_dict(serde.json.deser(index_dir / "_SUCCESS"))
            == settings
        )


if __name__ == "__main__":
    args = yada.Parser1(BuildIndexArgs).parse_args()

    build_sparse_index(
        dataset_name=args.dataset,
        dataset=args.get_dataset(),
        data_dir=args.data_dir,
        index_dir=args.index_dir,
        settings=args.settings,
        n_files=args.n_files,
        optimize=args.optimize,
        shuffle=args.shuffle,
    )
