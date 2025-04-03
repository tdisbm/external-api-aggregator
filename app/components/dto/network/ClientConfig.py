from pydantic import BaseModel


class ClientConfig(BaseModel):
    retries_threshold: int
    url: str
    headers: dict