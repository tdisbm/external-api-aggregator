from typing import List, Optional, Dict

from pydantic import BaseModel, Field

from app.components.dto.Account import Account
from app.components.dto.Software import Software
from app.components.dto.Cloud import Cloud
from app.components.dto.Hardware import Hardware
from app.components.dto.Identity import Identity
from app.components.dto.Metadata import Metadata
from app.components.dto.Network import Network
from app.components.dto.OS import OS
from app.components.dto.Security import Security
from app.components.dto.Timestamp import Timestamps


class Host(BaseModel):
    identity: Identity
    metadata: Metadata
    network: Network
    os: OS
    hardware: Hardware
    software: Software
    security: Security
    cloud: Cloud
    accounts: List[Account] = Field(default_factory=list)
    timestamps: Timestamps
    extras: Optional[Dict] = Field(default_factory=dict)

    def __eq__(self, other):
        return self.identity == other.identity and self.identity.hostname == other.identity.hostname

    def __hash__(self):
        return hash(self.identity)
