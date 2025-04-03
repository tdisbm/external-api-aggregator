from typing import Optional, List

from pydantic import BaseModel, Field

from app.components.dto.CloudSecurityGroup import CloudSecurityGroup
from app.components.dto.Tag import Tag


class Cloud(BaseModel):
    provider: Optional[str or None]
    account_id: Optional[str or None]
    region: Optional[str or None]
    zone: Optional[str or None]
    vpc_id: Optional[str or None]
    subnet_id: Optional[str or None]
    security_groups: List[CloudSecurityGroup] = Field(default_factory=list)
    tags: List[Tag] = Field(default_factory=list)

    def __hash__(self):
        return hash(self.account_id)
