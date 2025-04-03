from typing import Optional

from pydantic import BaseModel, Field


class CPU(BaseModel):
    model: Optional[str or None] = Field(default_factory=lambda: None)
    speed_mhz: Optional[int or None] = Field(default_factory=lambda: None)
    signature: Optional[str] = Field(default_factory=str)

    def __hash__(self):
        return hash(self.signature)
