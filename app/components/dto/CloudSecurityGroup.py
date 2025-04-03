from typing import Optional

from pydantic import BaseModel


class CloudSecurityGroup(BaseModel):
    id: Optional[str]
    name: Optional[str]

    def __hash__(self):
        return hash(self.id)
