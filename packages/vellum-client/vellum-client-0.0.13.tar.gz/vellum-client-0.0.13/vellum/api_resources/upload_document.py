from typing import IO, List, Optional

from vellum.api_resources.abstract.documents_api_resource import DocumentsAPIResource
from vellum.api_resources.types import DocumentUploadResult


class UploadDocument(DocumentsAPIResource):
    api_path = "v1/upload-document"

    @classmethod
    def run(  # type: ignore
        cls,
        contents: IO,
        label: str,
        add_to_index_names: Optional[List[str]] = None,
        external_id: Optional[str] = None,
        keywords: Optional[List[str]] = None,
    ) -> DocumentUploadResult:
        """Upload a document to later search across it.

        Args:
            contents: The contents of the file that you'd like to upload
            label: A human-friendly name for the document, typically the file name.
            add_to_index_names: The names of document indexes that you'd like this document to be added to.
            external_id: Optionally include a unique ID from your system to this document later.
                Useful if you want to perform updates later.
            keywords: Optionally include keywords to associate with the document that can be used in hybrid search.
        Returns:
            The result of the document upload request.
        """

        raw_result = super().run(
            contents=contents,
            label=label,
            add_to_index_names=add_to_index_names,
            external_id=external_id,
            keywords=keywords,
        )

        return DocumentUploadResult.from_raw(raw_result)
