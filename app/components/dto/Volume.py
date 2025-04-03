from pydantic import BaseModel


class Volume(BaseModel):
    name: str
    size_bytes: int
    free_bytes: int

    def __eq__(self, other):
        return self.name == other.name

    def __hash__(self):
        return hash(self.name)
