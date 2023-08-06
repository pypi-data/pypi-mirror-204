from typing import NamedTuple, Optional

from ..clients.base import SUCCESS_STATUS_CODE, BaseClient, ClientResponse
from ..clients.schemas import CohereCompleteSchema

__all__ = ["CohereClient"]


class Schema(NamedTuple):
    complete: dict


class CohereClient(BaseClient):
    base_url = "https://api.cohere.ai"
    api_env_name = "COHERE_API_KEY"
    api_header_format = "bearer authentication"

    schema = Schema(complete=CohereCompleteSchema.schema()["properties"])

    def __init__(self, api_key: Optional[str] = None, api_version: str = "2022-12-06", **kwargs):
        super().__init__(api_key, **kwargs)
        self._api_version = api_version

    def complete(self, prompt: str, **kwargs) -> ClientResponse:
        status_code, response = self._post_request(
            "generate",
            CohereCompleteSchema(prompt=prompt, **kwargs).to_request_dict(),
            extra_headers={"Cohere-Version": self._api_version},
        )
        return ClientResponse(
            text=response["generations"][0]["text"] if status_code == SUCCESS_STATUS_CODE else None,
            raw_response=response,
            status_code=status_code,
        )
