#!/usr/bin/env python3

"""Generates PalType from JSON file."""

import os
from pathlib import Path
from .gen_template import GenTemplate, InformationBase


class GenPalType(GenTemplate):
    """Generates PalType from JSON file."""
    def __init__(self) -> None:
        self._site: str = "github.com"
        self._repo_user: str = "EternalWraith"
        self._repo_name: str = "PalEdit"
        self._branch: str = "main"
        self._path_to_file: str = "palworld_pal_edit/resources/data/pals.json"
        self._path_to_python_file: str = "PalInfo.py"

        self._template = dict({
            "head": f"""# pylint: disable=C0114,C0103
from enum import Enum
from .logger import log


# {self.__gen_url__(self._path_to_python_file)}
class PalType(Enum):
    \"\"\"PalType

    See:
        {self.__gen_url__(self._path_to_python_file)}
        {self.__gen_url__(self._path_to_file)}

    Args:
        Enum (str): Name of pal per internal ID.
    \"\"\"

""",
            "body": "    {} = \"{}\"",
            "tail": """


    @classmethod
    def get(cls, value: str, origin_value: str) -> str:
        for i in PalType:
            if i.name.upper() == value:
                return i.value
        log(f"PalType {origin_value} need to be translated", "WARN")
        return origin_value
""",
        })
        super().__init__()

    def generate(self) -> None:
        data: list[InformationBase] | None = super().generate()
        if data is None:
            raise TypeError("Type from parent generate function returned typeof None.")
        current_dir: Path = Path(os.path.dirname(os.path.realpath(__file__)))
        with current_dir.joinpath("..", "pal_skills.py").open(mode="w", encoding="utf8") as f:
            f.write(self._template["head"])
            for item in data:
                f.write(self._template["body"].format(item.code_name, item.name))
            f.write(self._template["tail"])
            f.close()
