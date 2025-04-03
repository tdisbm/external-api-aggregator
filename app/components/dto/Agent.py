from datetime import datetime
from typing import Optional, Dict, Any

from pydantic import BaseModel, Field


class Agent(BaseModel):
    name: str
    external_id: Optional[str] = Field(default_factory=str)
    version: str = Field(default_factory=str)
    status: Optional[str] = Field(default_factory=str)
    remote_address: Optional[str] = Field(default_factory=str)
    location: Optional[Dict[str, Any]] = Field(default_factory=dict)
    last_seen: Optional[datetime or None] = Field(default_factory=lambda: None)
    local_time: Optional[datetime or None] = Field(default_factory=lambda: None)
    extra: Optional[Dict[str, Any]] = Field(default_factory=dict)

    def __eq__(self, other):
        return self.external_id == other.external_id

    def __hash__(self) -> int:
        return hash(self.external_id)
