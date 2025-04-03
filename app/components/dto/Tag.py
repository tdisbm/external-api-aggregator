from typing import Optional

from pydantic import BaseModel


class Tag(BaseModel):
    id: Optional[str]
    name: Optional[str]

    def __eq__(self, other):
        return self.name == other.name

    def __hash__(self):
        return hash(self.name)
