from ..adapters.fermi import FermiProblemAdapter
from ..clients.base import ClientResponse

__all__ = ["FermiProblem"]


class FermiProblem:
    def __init__(self, adapter: FermiProblemAdapter):
        self.adapter = adapter

    def ask(self, question: str, **kwargs) -> ClientResponse:
        input_text = self.adapter.prompter.create_prompt(question)
        kwargs.update(self.adapter.prepare_input_content(input_text))
        response = getattr(self.adapter.client, str(self.adapter.client._target_api_endpoint))(**kwargs)
        response = self.adapter.postprocess_response(response)
        return response
