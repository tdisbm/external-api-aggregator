from typing import List

from pydantic import BaseModel

from app.components.dto.network.APIConfig import APIConfig


class PollingConfig(BaseModel):
    poll_interval_s: int
    api_config: List[APIConfig]
