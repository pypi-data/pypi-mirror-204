from abc import abstractmethod
import json
import os
from typing import IO, Any, cast

from vellum.api_resources.abstract.api_resource import APIResource


class DocumentsAPIResource(APIResource):
    @property
    @abstractmethod
    def api_path(self) -> str:
        pass

    api_base = "https://documents.vellum.ai"

    @classmethod
    def run(cls, contents: IO, **kwargs: Any) -> dict:
        result = cast(
            dict,
            cls._make_request(
                "POST",
                cast(str, cls.api_path),
                files={"contents": (contents.name, contents, "application/octet-stream")},
                data=kwargs,
            ).json(),
        )

        return result
