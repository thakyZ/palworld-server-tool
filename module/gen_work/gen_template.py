#!/usr/bin/env python3

"""Generate Information Template."""

import json
from typing import Literal, Any
from requests import HTTPError, request
from requests.models import Response

TemplateType = dict[Literal["head", "body", "tail"], str]


class InformationBase:
    """Template for information base."""

    def __init__(self, code_name: str, name: str) -> None:
        self.code_name: str = code_name
        self.name: str = name


class GenTemplate:
    """Template for Information Generator"""

    _site: str = ""
    _repo_user: str = ""
    _repo_name: str = ""
    _branch: str = ""
    _path_to_file: str = ""

    _template: TemplateType

    # pylint: disable-next=W0246
    def __init__(self) -> None:
        super().__init__()

    def __gen_url__(self, path: str, raw: bool = False) -> str:
        blob: str = "blob" if raw is False else "raw"
        return (
            f"https://{self._site}/{self._repo_user}/{self._repo_name}/{blob}/{self._branch}/{path}"
        )

    def generate(self) -> list[InformationBase] | None:
        """Generates information into a new file."""
        response: Response = request(
            method="get", url=self.__gen_url__(self._path_to_file, True), timeout=10
        )
        if response.status_code != 200:
            raise HTTPError(
                f"Failed to fetch json with status code: {response.status_code}"
            )
        json_data: dict[str, Any] = json.loads(
            response.content.decode(
                encoding=(
                    response.encoding if response.encoding is not None else "utf-8"
                )
            )
        )
        output: list[InformationBase] = []
        for key, value in json_data.items():
            if key == "values":
                for _, item in enumerate(value):
                    output.append(InformationBase(item["CodeName"], item["Name"]))
        return output
