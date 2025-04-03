from typing import List

from pydantic import BaseModel


class ModelAggregator:
    def aggregate(self, models: List[BaseModel]):
        merged_models = list()
        for model in models:
            match_found = False
            for i, merged_model in enumerate(merged_models):
                if merged_model == model:
                    merged_models[i] = self.merge(merged_model, model)
                    match_found = True
                    break
            if not match_found:
                merged_models.append(model)
        return merged_models

    def merge(self, model1: BaseModel, model2: BaseModel):
        raise NotImplemented("Interface method")
