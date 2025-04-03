from pydantic import BaseModel

from app.components.dto.network.OffsetConfig import OffsetConfig


class FetcherConfig(BaseModel):
    max_concurrent_calls: int
    offset: OffsetConfig
