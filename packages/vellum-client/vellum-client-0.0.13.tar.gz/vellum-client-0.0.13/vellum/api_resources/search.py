from dataclasses import asdict
from typing import Optional

from vellum.api_resources.abstract.predict_api_resource import PredictAPIResource
from vellum.api_resources.types import SearchOptions, SearchResults


class Search(PredictAPIResource):
    api_path = "v1/search"

    @classmethod
    def run(  # type: ignore
        cls,
        query: str,
        index_id: Optional[str] = None,
        index_name: Optional[str] = None,
        options: Optional[SearchOptions] = None,
    ) -> SearchResults:
        """Peform a semantic search query against a document index.

        Args:
            actuals: A list of CompletionActual objects, each containing the info needed
                to submit a single actual.
            index_id: The ID of the document index that you'd like to search across. You must provide either this
                or index_name.
            index_name: The name of the document index that you'd like to search across. You must provide either
                this or index_id.
            options: An optional SearchOptions object containing options for the search query.
        Returns:
            The result of the generation request.
        """

        if index_id is None and index_name is None:
            raise ValueError("Must provide either index_id or index_name")
        elif index_id is not None and index_name is not None:
            raise ValueError("Must provide only one of index_id or index_name")

        options = options or SearchOptions()

        raw_result = super().run(
            query=query,
            index_id=index_id,
            index_name=index_name,
            options=asdict(options),
        )

        return SearchResults.from_raw(raw_result)
