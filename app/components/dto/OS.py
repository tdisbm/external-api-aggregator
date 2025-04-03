from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class OS(BaseModel):
    name: str
    version: Optional[str] = Field(default_factory=str)
    kernel: Optional[str] = Field(default_factory=str)
    boot_time: Optional[datetime or None] = Field(default_factory=lambda: None)
