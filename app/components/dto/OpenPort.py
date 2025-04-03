from typing import Optional

from pydantic import BaseModel


class OpenPort(BaseModel):
    port: str
    protocol: str
    service: Optional[str]

    def __eq__(self, other):
        return self.port == other.port

    def __hash__(self):
        return hash(self.port)
