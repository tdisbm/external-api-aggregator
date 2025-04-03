from pydantic import BaseModel

from app.components.transformer.ModelAggregator import ModelAggregator
from app.components.dto.NetworkInterface import NetworkInterface


class NetworkInterfaceAggregator(ModelAggregator):
    def merge(self, model1: BaseModel, model2: BaseModel):
        return NetworkInterface(
            name=model1.name or model2.name,
            ips=list(set(model1.ips + model2.ips)),
            mac=model1.mac or model2.mac,
            gateway=model1.gateway or model2.gateway,
        )
