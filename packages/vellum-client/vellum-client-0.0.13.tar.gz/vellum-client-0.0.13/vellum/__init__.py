import os

from vellum.api_resources import Generate
from vellum.api_resources.completion_actuals import SubmitCompletionActuals
from vellum.api_resources.search import Search
from vellum.api_resources.types import (
    CompletionActual,
    DocumentUploadResult,
    GenerateRequest,
    ResultMerging,
    SearchFilters,
    SearchOptions,
    SearchWeights,
)
from vellum.api_resources.upload_document import UploadDocument

api_key = os.environ.get("VELLUM_API_KEY")

__all__ = [
    "CompletionActual",
    "Generate",
    "GenerateRequest",
    "ResultMerging",
    "Search",
    "SearchFilters",
    "SearchOptions",
    "SearchWeights",
    "SubmitCompletionActuals",
    "UploadDocument",
    "DocumentUploadResult",
    "api_key",
]
