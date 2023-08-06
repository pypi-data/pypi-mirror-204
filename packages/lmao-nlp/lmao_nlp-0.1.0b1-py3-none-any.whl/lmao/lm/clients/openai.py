from typing import Dict, List, NamedTuple, Optional

from lmao.lm.clients import SUCCESS_STATUS_CODE, BaseClient, ChatHistory, ClientResponse
from lmao.lm.schemas import OpenAIChatSchema, OpenAICompleteSchema

__all__ = ["OpenAIClient", "OpenAIChatHistory"]


DEFAULT_SYSTEM_MESSAGE = "You are a helpful assistant."


class Schema(NamedTuple):
    complete: dict
    chat: dict


class OpenAIChatHistory(ChatHistory):
    human_role: str = "user"
    assistant_role: str = "assistant"

    @staticmethod
    def check_message_format(message):
        if not isinstance(message, dict):
            raise ValueError(f"Message must be a dict, not {type(message)}.")
        if "role" not in message:
            raise ValueError("Message must have a 'role' key.")
        if "content" not in message:
            raise ValueError("Message must have a 'content' key.")
        if message["role"].lower() not in ["user", "assistant"]:
            raise ValueError("Message role must be 'user' or 'assistant'.")
        return message

    def to_request_format(self):
        return {"messages": self.messages}


class OpenAIClient(BaseClient):
    base_url = "https://api.openai.com/v1"
    api_env_name = "OPENAI_API_KEY"
    api_header_format = "bearer authentication"

    schema = Schema(complete=OpenAICompleteSchema.schema()["properties"], chat=OpenAIChatSchema.schema()["properties"])

    def __init__(self, api_key: Optional[str] = None, **kwargs):
        super().__init__(api_key, **kwargs)

    def chat(
        self,
        messages: List[Dict[str, str]],
        system_message: str = DEFAULT_SYSTEM_MESSAGE,
        **kwargs,
    ) -> ClientResponse:
        messages = [{"role": "system", "content": system_message}] + [
            OpenAIChatHistory.check_message_format(m) for m in messages
        ]
        status_code, response = self._post_request(
            "chat/completions", OpenAIChatSchema(messages=messages, **kwargs).to_request_dict()
        )
        return ClientResponse(
            text=response["choices"][0]["message"]["content"] if status_code == SUCCESS_STATUS_CODE else None,
            raw_response=response,
            status_code=status_code,
        )

    def complete(self, prompt: str, **kwargs) -> ClientResponse:
        status_code, response = self._post_request(
            "completions", OpenAICompleteSchema(prompt=prompt, **kwargs).to_request_dict()
        )
        return ClientResponse(
            text=response["choices"][0]["text"] if status_code == SUCCESS_STATUS_CODE else None,
            raw_response=response,
            status_code=status_code,
        )

    def create_chat_history(self, max_length: int = 10) -> OpenAIChatHistory:
        return OpenAIChatHistory(max_length=max_length)
