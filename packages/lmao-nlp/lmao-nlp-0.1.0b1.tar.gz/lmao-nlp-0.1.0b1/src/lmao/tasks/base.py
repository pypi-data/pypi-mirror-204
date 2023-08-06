from dataclasses import dataclass
from typing import NamedTuple, Protocol, runtime_checkable

from ..adapters.base import BaseAdapter
from ..clients.base import ClientResponse

__all__ = ["task_errors", "ModelTaskProtocol", "QATaskProtocol", "TaskResponse"]


class TaskErrors(NamedTuple):
    CLIENT_ERROR: str
    PREDICTION_ERROR: str


task_errors = TaskErrors(CLIENT_ERROR="CLIENT ERROR", PREDICTION_ERROR="PREDICTION ERROR")


@dataclass
class TaskResponse:
    prediction: str
    client_response: ClientResponse
    success: bool


@runtime_checkable
class ModelTaskProtocol(Protocol):
    adapter: BaseAdapter

    def predict(self, text: str, **kwargs) -> TaskResponse:
        ...


@runtime_checkable
class QATaskProtocol(Protocol):
    adapter: BaseAdapter

    def ask(self, question: str, **kwargs) -> TaskResponse:
        ...
