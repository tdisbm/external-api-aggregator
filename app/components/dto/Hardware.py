from typing import Optional, Dict, List

from pydantic import BaseModel, Field

from app.components.dto.CPU import CPU
from app.components.dto.Volume import Volume


class Hardware(BaseModel):
    manufacturer: Optional[str]
    model: Optional[str]
    bios: Optional[Dict] = Field(default_factory=dict)
    cpu: CPU = Field(default_factory=CPU)
    memory_mb: Optional[int] = Field(default_factory=int)
    volumes: List[Volume] = Field(default_factory=list)

    def __hash__(self):
        return hash((self.manufacturer, self.model))