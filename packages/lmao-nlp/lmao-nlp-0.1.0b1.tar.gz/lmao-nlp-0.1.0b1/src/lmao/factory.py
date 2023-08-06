from typing import NamedTuple, Tuple, Union

from . import adapters, clients, tasks

__all__ = ["create_chatbot", "create_client", "create_task"]


class ObjectMapping(NamedTuple):
    name_to_client: dict = {
        "anthropic": clients.AnthropicClient,
        "cohere": clients.CohereClient,
        "openai": clients.OpenAIClient,
    }
    name_to_history: dict = {"anthropic": clients.AnthropicChatHistory, "openai": clients.OpenAIChatHistory}
    name_to_task: dict = {
        "sentiment_analysis": tasks.TextClassification,
        "text_classification": tasks.TextClassification,
        "fermi_problem": tasks.FermiProblem,
        "chatbot": tasks.Chatbot,
    }
    task_to_adapter: dict = {
        "chatbot": {
            "anthropic": adapters.AnthropicChatbotAdapter,
            "openai": adapters.OpenAIChatbotAdapter,
        },
        "sentiment_analysis": {
            "anthropic": adapters.AnthropicSentimentAnalysisAdapter,
            "cohere": adapters.CohereSentimentAnalysisAdapter,
            "openai": adapters.OpenAISentimentAnalysisAdapter,
        },
        "text_classification": {
            "anthropic": adapters.AnthropicTextClassificationAdapter,
            "cohere": adapters.CohereTextClassificationAdapter,
            "openai": adapters.OpenAITextClassificationAdapter,
        },
        "fermi_problem": {
            "anthropic": adapters.AnthropicFermiProblemAdapter,
            "cohere": adapters.CohereFermiProblemAdapter,
            "openai": adapters.OpenAIFermiProblemAdapter,
        },
    }


_m = ObjectMapping()


def _validate_task_input(task: str, client_name: str):
    client_name = client_name.lower()
    task = task.lower().replace(" ", "_")
    if client_name not in _m.name_to_client:
        raise ValueError(f"LM client {client_name} not supported")
    if task not in _m.name_to_task:
        raise ValueError(f"Task {task} not supported")
    return task, client_name


def create_chatbot(client_name: str, **kwargs) -> tasks.Chatbot:
    return tasks.Chatbot(_m.task_to_adapter["chatbot"][client_name](**kwargs))


def create_client(
    client_name: str, chat_history: bool = False, **kwargs
) -> Union[clients.BaseClient, Tuple[clients.BaseClient, clients.ChatHistory]]:
    max_length = kwargs.pop("max_length", 5)
    Client, History = _m.name_to_client[client_name], _m.name_to_history[client_name]
    return (Client(**kwargs), History(max_length=max_length)) if chat_history else Client(**kwargs)


def create_task(
    task: str, client_name: str, **kwargs
) -> Union[tasks.ModelTaskProtocol, tasks.QATaskProtocol, tasks.Chatbot]:
    task, client_name = _validate_task_input(task, client_name)
    Task = _m.name_to_task[task]
    client_adapter = _m.task_to_adapter[task][client_name](**kwargs)
    return Task(client_adapter) if task != "chatbot" else create_chatbot(client_name, **kwargs)
