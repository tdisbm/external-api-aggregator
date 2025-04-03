import logging
from time import sleep
from typing import List, Dict, Tuple

from app.components.dto.network.APIConfig import APIConfig
from app.components.dto.network.PollingConfig import PollingConfig
from app.database.connection import Session
from app.database.repository.host_repository import find_similar_hosts, delete_hosts, update_hosts
from app.worker.transformer.aggregator.HostAggregator import HostAggregator
from app.worker.service.api_fetch_service import fetch
from app.worker.service.normalize_service import normalize_by_qualifier


logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


def run_hosts_polling(polling_config: Dict):  # May be generified, but not now
    polling_config: PollingConfig = PollingConfig(**polling_config)
    while True:  # Polling never stops
        try:
            responses = fetch(api_conf=polling_config.api_config)
            hosts = _post_fetch(responses)
            hosts_existing = find_similar_hosts(hosts=hosts)
            hosts_unique = HostAggregator().aggregate(models=hosts + hosts_existing)
            with Session() as session:
                # Delete already existing host because they are merged with latest batch fetched from API.
                # Delete operation may be excluded since we update already existing hosts, but hey, let's leave it
                # just in case
                delete_hosts(hosts=hosts_unique, session=session)
                update_hosts(hosts=hosts_unique, session=session)
            logger.info(f"[+] Polling iteration complete: Applying delay of {polling_config.poll_interval_s}s")
            sleep(polling_config.poll_interval_s)
        except Exception as e:
            logger.error(f"[-] Poll iteration failed: {str(e)}")


def _post_fetch(responses: List[Tuple[List, APIConfig]]):
    hosts_normalized_all = list()
    for response in responses:
        data = response[0]
        conf = response[1]
        hosts_normalized = normalize_by_qualifier(data=data, qualifier=conf.qualifier)
        _update_offsets(data=hosts_normalized, api_config=conf)
        hosts_normalized_all.extend(hosts_normalized)
    return hosts_normalized_all


def _update_offsets(data: List, api_config: APIConfig):
    if len(data) < api_config.fetcher.offset.take * api_config.fetcher.max_concurrent_calls:
        api_config.fetcher.offset.skip = 0
    else:
        api_config.fetcher.offset.skip += len(data)
