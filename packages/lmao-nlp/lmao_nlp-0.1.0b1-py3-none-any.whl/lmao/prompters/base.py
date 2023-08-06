from abc import ABC, abstractmethod

__all__ = ["build_prompt_template", "Prompter"]


def build_prompt_template(intro: str, close: str, sep: str = "\n\n", include_examples: bool = True) -> str:
    base_template = "{intro}{sep}{{examples}}{close}" if include_examples else "{intro}{sep}{close}"
    return base_template.format(intro=intro, sep=sep, close=close)


class Prompter(ABC):
    task: str = "none"

    @abstractmethod
    def create_prompt(self, input_text: str) -> str:
        pass
