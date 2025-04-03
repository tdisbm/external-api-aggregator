from typing import Optional, List

from pydantic import BaseModel, Field


class NetworkInterface(BaseModel):
    name: Optional[str]
    mac: Optional[str]
    ips: List[str] = Field(default_factory=list)
    gateway: Optional[str]

    def __eq__(self, other):
        return (self.mac == other.mac and
                self.ips == other.ips and
                self.gateway == other.gateway)
