import re
from typing import List, Optional

from pydantic import Extra, Field, validator

from .base import API_DEFAULTS, BaseSchema

__all__ = ["AnthropicCompleteSchema", "anthropic_model_regex"]


anthropic_model_regex = dict(complete=re.compile(r"claude-(?:instant-)?v\d(?:\.\d)?"))


class AnthropicCompleteSchema(BaseSchema):
    """API Reference: https://console.anthropic.com/docs/api/reference"""

    class Config:
        extra = Extra.forbid

    prompt: str = Field(default="Human: Hello, Friend\n\nAssistant:", description="The prompt to complete.")
    model: str = Field(default="claude-v1.3", description="Must be of the form `claude-[model_version]`.")
    max_tokens_to_sample: int = API_DEFAULTS.complete_max_tokens
    stop_sequences: Optional[List[str]] = None
    stream: bool = False
    temperature: float = Field(default=1, ge=0.0, le=1.0)
    top_k: int = -1
    top_p: float = -1

    @validator("model", pre=True, always=True)
    def validate_model(cls, v):
        if not anthropic_model_regex["complete"].search(v):
            raise ValueError(f"{v} is an invalid model format.")
        return v
