from pydantic import BaseModel, Field


class SoftwarePackage(BaseModel):
    name: str
    version: str = Field(default_factory=str)

    def __eq__(self, other):
        return self.name == other.name

    def __hash__(self):
        return hash(self.name)
