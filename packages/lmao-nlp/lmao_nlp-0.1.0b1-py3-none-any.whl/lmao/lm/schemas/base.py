from typing import NamedTuple

from pydantic import BaseModel

__all__ = ["BaseSchema", "API_DEFAULTS"]


class GLOBAL_API_DEFAULTS(NamedTuple):
    complete_max_tokens: int = 512


class BaseSchema(BaseModel):
    def to_request_dict(self):
        """Return a dict of the schema with None values removed."""
        return {k: v for k, v in self.dict().items() if v is not None}


API_DEFAULTS = GLOBAL_API_DEFAULTS()
