from typing import Optional

from pydantic import BaseModel, Field


class OffsetConfig(BaseModel):
    limit: Optional[int] = Field(default_factory=lambda: -1)
    skip: Optional[int] = Field(default_factory=lambda: 0)
    take: int
