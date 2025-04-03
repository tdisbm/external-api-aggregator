from typing import List

from pydantic import BaseModel, Field

from app.components.dto.NetworkInterface import NetworkInterface
from app.components.dto.OpenPort import OpenPort


class Network(BaseModel):
    interfaces: List[NetworkInterface] = Field(default_factory=list)
    public_ips: List[str] = Field(default_factory=list)
    dns_names: List[str] = Field(default_factory=list)
    open_ports: List[OpenPort] = Field(default_factory=list)
