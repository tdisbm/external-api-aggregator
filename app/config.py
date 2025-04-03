import os

from app.worker.transformer.normalizer.CrowdstrikeHostNormalizer import CrowdstrikeHostNormalizer
from app.worker.transformer.normalizer.QualysHostNormalizer import QualysHostNormalizer

MONGO_DB_NAME = os.getenv("MONGO_DB_NAME", "armis")
MONGO_DB_URI = os.getenv("MONGO_DB_URI", "mongodb://localhost:27017")

HOSTS_POLLING_CONFIG = {
    "poll_interval_s": 2,
    "api_config": [{
        "name": "crowdstrike hosts api",
        "qualifier": CrowdstrikeHostNormalizer.SOURCE_QUALIFIER,
        "client": {
            "retries_threshold": 10,
            "url": "https://api.recruiting.app.silk.security/api/crowdstrike/hosts/get",
            "headers": {
                "token": "shared-zevetone@armis.com_357c050d-e4da-432a-a2e5-f61516928717",
                "accept": "application/json"
            }
        },
        "fetcher": {
            "max_concurrent_calls": 4,  # How many concurrent clients are executed in one iteration
            "offset": {
                "limit": 4,  # max results that fetcher might return as sum of all the requests data
                "take": 1  # one record per request to avoid api errors
            },
        }
    }, {
        "name": "qualys hosts api",
        "qualifier": QualysHostNormalizer.SOURCE_QUALIFIER,
        "client": {
            "retries_threshold": 10,
            "url": "https://api.recruiting.app.silk.security/api/qualys/hosts/get",
            "headers": {
                "token": "shared-zevetone@armis.com_357c050d-e4da-432a-a2e5-f61516928717",
                "accept": "application/json"
            },
        },
        "fetcher": {
            "max_concurrent_calls": 4,
            "offset": {
                "limit": 1,
                "take": 1
            },
        }
    }]
}
