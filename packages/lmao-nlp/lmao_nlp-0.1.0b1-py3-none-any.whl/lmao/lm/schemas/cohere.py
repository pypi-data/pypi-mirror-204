from typing import List, Optional

from pydantic import Field

from lmao.lm.schemas import API_DEFAULTS, BaseSchema

__all__ = ["CohereCompleteSchema"]


class CohereCompleteSchema(BaseSchema):
    """API Reference: https://docs.cohere.ai/reference/generate"""

    prompt: str = Field(default="Human: Hello, Friend!\n\nAssistant:", description="The prompt to complete.")
    model: str = "command-xlarge-nightly"
    num_generations: int = Field(default=1, ge=1, le=5)
    max_tokens: int = API_DEFAULTS.complete_max_tokens
    preset: Optional[str] = None
    temperature: float = Field(default=0.75, ge=0.0, le=5.0)
    k: int = Field(default=0, ge=0, le=500)
    p: float = Field(default=0.75, ge=0.0, le=1.0)
    frequency_penalty: float = Field(default=0.0, ge=0.0, le=1.0)
    presence_penalty: float = Field(default=0.0, ge=0.0, le=1.0)
    end_sequences: Optional[List[str]] = None
    stop_sequences: Optional[List[str]] = None
    return_likelihoods: Optional[str] = None
    logit_bias: Optional[dict] = None
    truncate: Optional[str] = None
