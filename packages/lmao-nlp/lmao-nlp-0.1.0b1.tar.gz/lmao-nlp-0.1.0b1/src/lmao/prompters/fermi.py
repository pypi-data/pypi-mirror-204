from .base import Prompter, build_prompt_template

__all__ = ["FermiProblemPrompter"]


class FermiProblemPrompter(Prompter):
    template = build_prompt_template(
        intro=(
            "Answer the following question, which is a Fermi problem. Think logically step by step "
            "in the spirit of Enrico Fermi."
        ),
        close="Question: {question}\nAnswer:",
    )

    def __init__(self):
        self._examples = []

    def add_example(self, question: str, answer: str):
        self._examples.append(f"Question: {question}\nAnswer:{answer}\n\n")

    def create_prompt(self, question: str) -> str:
        return self.template.format(question=question, examples="".join(self._examples) if self._examples else "")
