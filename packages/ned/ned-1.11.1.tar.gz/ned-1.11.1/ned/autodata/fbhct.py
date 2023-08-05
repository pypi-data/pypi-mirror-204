from typing import Optional
from ned.autodata.lv1 import LabelV1
from ned.autodata.utils import FilterMixin, StrPath
from dataclasses import dataclass
from pathlib import Path
import re

import serde.yaml
from sm.dataset import FullTable

DEFAULT_WHITELIST_FILENAME = "whitelist.yml"


@dataclass
class FilterByHeaderColTypeArgs:
    whitelist_file: Path


class FilterByHeaderColType(FilterMixin):

    VERSION = 100

    def __init__(
        self,
        args: FilterByHeaderColTypeArgs,
        labeler: LabelV1,
        log_file: Optional[StrPath] = None,
    ):
        super().__init__(log_file)
        # mapping from class id to list of allowed column names
        self.whitelist: dict[str, set[str]] = self.parse_whitelist(args.whitelist_file)
        self.whitelist_keys = set(self.whitelist.keys())
        self.labeler = labeler
        self.classes = labeler.classes

    def is_noisy(self, table: FullTable, ci: int) -> tuple[bool, str]:
        header = table.table.columns[ci].clean_multiline_name
        if header is None:
            return True, "no header"
        col_types = self.labeler.label_column(table.links[:, ci])
        for col_type in col_types:
            if col_type.entity in self.whitelist_keys:
                if header in self.whitelist[col_type.entity]:
                    return False, ""
            else:
                cls = self.classes[col_type.entity]
                common_ancestors = cls.ancestors.intersection(self.whitelist_keys)
                if any(
                    header in self.whitelist[ancestor] for ancestor in common_ancestors
                ):
                    return False, ""
        return (
            True,
            f"Column {header} with candidate types {[f'{self.classes[ctype.entity].label} ({ctype.entity})' for ctype in col_types]} not in whitelist",
        )

    def parse_whitelist(self, infile: Path):
        whitelist = {}
        label2headers = serde.yaml.deser(infile)
        label_parser = re.compile(r"[^(]+ \((Q\d+)\)")

        for label, headers in label2headers.items():
            m = label_parser.match(label)
            assert m is not None
            class_id = m.group(1)
            whitelist[class_id] = set(headers)
        return whitelist
