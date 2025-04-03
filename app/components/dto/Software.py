from typing import List

from pydantic import BaseModel, Field

from app.components.dto.Agent import Agent
from app.components.dto.SoftwarePackage import SoftwarePackage


class Software(BaseModel):
    packages: List[SoftwarePackage] = Field(default_factory=list)
    agents: List[Agent] = Field(default_factory=list)
