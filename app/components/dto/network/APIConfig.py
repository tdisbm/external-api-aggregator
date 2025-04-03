from pydantic import BaseModel

from app.components.dto.network.ClientConfig import ClientConfig
from app.components.dto.network.FetcherConfig import FetcherConfig


class APIConfig(BaseModel):
    name: str
    qualifier: str
    client: ClientConfig
    fetcher: FetcherConfig
