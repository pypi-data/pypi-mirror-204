from ..adapters.chatbot import BaseChatbotAdapter
from ..clients.base import SUCCESS_STATUS_CODE, ClientResponse

__all__ = ["Chatbot"]


class Chatbot:
    def __init__(self, adapter: BaseChatbotAdapter):
        self.adapter = adapter
        self.client = adapter.client
        self.history = adapter.chat_history

    def chat(self, message: str, **kwargs) -> ClientResponse:
        self.history.add_human_message(message)
        kwargs.update((self.history.to_request_format()))
        response = getattr(self.client, str(self.client._target_api_endpoint))(**kwargs)
        if response.status_code == SUCCESS_STATUS_CODE:
            self.history.add_assistant_message(response.text)
        return self.adapter.postprocess_response(response)
