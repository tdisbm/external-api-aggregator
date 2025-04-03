from typing import List

from pydantic import BaseModel


class ModelNormalizer:
    def normalize_many(self, data: List[dict]) -> List[BaseModel]:
        return list(self.normalize(item) for item in data)

    def normalize(self, data: dict) -> BaseModel:
        raise NotImplementedError()
