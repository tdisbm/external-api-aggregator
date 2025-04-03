from app.worker.transformer.normalizer.CrowdstrikeHostNormalizer import CrowdstrikeHostNormalizer
from app.worker.transformer.normalizer.QualysHostNormalizer import QualysHostNormalizer

_NORMALIZER_QUALIFIER_MAP = {
    CrowdstrikeHostNormalizer.SOURCE_QUALIFIER: CrowdstrikeHostNormalizer,
    QualysHostNormalizer.SOURCE_QUALIFIER: QualysHostNormalizer,
}


def normalize_by_qualifier(data: list, qualifier: str):
    normalizer_type = _NORMALIZER_QUALIFIER_MAP.get(qualifier, None)
    if not normalizer_type:
        raise ValueError(f'Unknown normalizer type {qualifier}')
    return normalizer_type().normalize_many(data=data)