from typing import List

from .base import Prompter, build_prompt_template

__all__ = ["ClassificationPrompter", "SentimentAnalysisPrompter"]


class ClassificationPrompter(Prompter):
    task = "classification"

    template = build_prompt_template(
        intro=(
            "Classify the input text into one of the following {num_categories} categories: [{categories}]. "
            "Respond with the answer only, without punctuation."
        ),
        close="Input: {input_text}\nCategory:",
    )

    def __init__(
        self,
        categories: List[str],
    ):
        self.categories = categories
        self._examples: List[str] = []

    def add_example(self, input_text: str, category: str):
        if category not in self.categories:
            raise ValueError(f"Category {category} is not in the list of categories.")
        self._examples.append(f"Input: {input_text}\nCategory: {category}\n\n")

    def create_prompt(self, input_text: str) -> str:
        return self.template.format(
            num_categories=len(self.categories),
            categories=", ".join(self.categories),
            input_text=input_text,
            examples="".join(self._examples) if self._examples else "",
        )


class SentimentAnalysisPrompter(ClassificationPrompter):
    task = "sentiment_analysis"

    template = build_prompt_template(
        intro=(
            "Classify the sentiment of the input text into one of the following "
            "{num_categories} categories: [{categories}]. Respond with the answer only, without punctuation."
        ),
        close="Input: {input_text}\nSentiment:",
    )

    def __init__(
        self,
        include_neutral: bool = True,
    ):
        super().__init__(categories=["positive", "negative"] + (["neutral"] if include_neutral else []))
        self.include_neutral = include_neutral
