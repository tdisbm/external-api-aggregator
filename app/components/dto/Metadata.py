from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class Metadata(BaseModel):
    source: str
    collection_time: Optional[datetime]
