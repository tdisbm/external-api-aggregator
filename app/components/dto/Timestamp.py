from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class Timestamps(BaseModel):
    created: Optional[datetime]
    modified: Optional[datetime]
    first_seen: Optional[datetime]
    last_seen: Optional[datetime]
