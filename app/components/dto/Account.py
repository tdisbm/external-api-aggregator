from pydantic import BaseModel


class Account(BaseModel):
    username: str

    def __eq__(self, other):
        return self.username == other.username

    def __hash__(self):
        return hash(self.username)
