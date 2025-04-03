from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class SecurityPolicy(BaseModel):
    type: str
    id: str
    applied: bool
    applied_date: Optional[datetime]
    assigned_date: Optional[datetime]

    def __eq__(self, other):
        return self.id == other.id

    def __hash__(self):
        return hash(self.id)
