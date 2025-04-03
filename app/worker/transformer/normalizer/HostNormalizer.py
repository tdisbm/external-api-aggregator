from app.components.dto.Host import Host
from app.components.transformer.ModelNormalizer import ModelNormalizer


class HostNormalizer(ModelNormalizer):
    SOURCE_QUALIFIER = 'UNKNOWN'

    def normalize(self, data: dict) -> Host:
        return Host(
            metadata=self._normalize_metadata(data=data),
            identity=self._normalize_identity(data=data),
            network=self._normalize_network(data=data),
            os=self._normalize_os(data=data),
            hardware=self._normalize_hardware(data=data),
            software=self._normalize_software(data=data),
            security=self._normalize_security(data=data),
            cloud=self._normalize_cloud(data=data),
            accounts=self._normalize_accounts(data=data),
            timestamps=self._normalize_timestamps(data=data),
            extras=self._normalize_extra(data=data),
        )

    def _normalize_metadata(self, data: dict) -> dict:
        raise NotImplementedError()

    def _normalize_identity(self, data: dict) -> dict:
        raise NotImplementedError()

    def _normalize_network(self, data: dict) -> dict:
        raise NotImplementedError()

    def _normalize_os(self, data: dict) -> dict:
        raise NotImplementedError()

    def _normalize_hardware(self, data: dict) -> dict:
        raise NotImplementedError()

    def _normalize_software(self, data: dict) -> dict:
        raise NotImplementedError()

    def _normalize_security(self, data: dict) -> dict:
        raise NotImplementedError()

    def _normalize_cloud(self, data: dict) -> dict:
        raise NotImplementedError()

    def _normalize_accounts(self, data: dict) -> dict:
        raise NotImplementedError()

    def _normalize_timestamps(self, data: dict) -> dict:
        raise NotImplementedError()

    def _normalize_extra(self, data: dict) -> dict:
        raise NotImplementedError()
