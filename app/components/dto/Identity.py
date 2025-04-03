from typing import Optional

from pydantic import BaseModel, Field


class Identity(BaseModel):
    hostname: str
    fqdn: Optional[str] = Field(default_factory=str)
    instance_id: Optional[str] = Field(default_factory=str)
    serial_number: Optional[str] = Field(default_factory=str)
    external_ids: Optional[list] = Field(default_factory=list)

    def __eq__(self, other):
        return self.hostname == other.hostname and self.instance_id == other.instance_id
