from abc import ABC, abstractmethod
from typing import Optional

from ..clients.base import BaseClient, ClientResponse
from ..prompters.base import Prompter

__all__ = ["BaseAdapter", "BaseTaskAdapter"]


class BaseAdapter(ABC):
    def __init__(self, api_key: Optional[str] = None, **kwargs):
        self.client = self.load_client(api_key, **kwargs)
        assert self.client._target_api_endpoint is not None, "You must set the client's target API endpoint."

    @abstractmethod
    def load_client(self, api_key: Optional[str] = None, **kwargs) -> BaseClient:
        pass

    @abstractmethod
    def prepare_input_content(self, content) -> dict:
        pass

    def postprocess_response(self, response: ClientResponse) -> ClientResponse:
        return response


class BaseTaskAdapter(BaseAdapter):
    def __init__(self, prompter: Prompter, api_key: Optional[str] = None, **kwargs):
        self.prompter = prompter
        super().__init__(api_key, **kwargs)
