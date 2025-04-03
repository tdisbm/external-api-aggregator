import asyncio
import logging
from typing import List, Dict, Any, Tuple

from app.components.dto.network.APIConfig import APIConfig
from app.components.dto.network.ClientConfig import ClientConfig
from app.components.network.AsyncAPIClient import AsyncAPIClient
from app.components.network.AsyncAPIFetcher import AsyncAPIFetcher
from app.components.network.response_adapter import async_json_adapter

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


def fetch(api_conf: List[APIConfig]) -> List[Tuple[List, APIConfig]]:
    return asyncio.run(async_fetch(api_conf=api_conf))


async def async_fetch(api_conf: List[APIConfig]) -> List[Tuple[List, APIConfig]]:
    fetch_tasks = list()
    for api_conf_ in api_conf:
        logger.info(f"[+] Polling - {api_conf_.name}")
        fetch_tasks.append(_async_fetch_wrapper(api_conf=api_conf_))
    return list(response for response in await asyncio.gather(*fetch_tasks))


async def _async_fetch_wrapper(api_conf: APIConfig) -> Tuple[List, APIConfig]:
    client_config: ClientConfig = api_conf.client
    client = AsyncAPIClient(
        url=client_config.url,
        headers=client_config.headers,
        retries=client_config.retries_threshold,
        response_adapter=async_json_adapter,
    )
    fetcher_config = api_conf.fetcher
    fetcher = AsyncAPIFetcher(
        client=client,
        offset=fetcher_config.offset,
        max_concurrent_calls=fetcher_config.max_concurrent_calls,
    )
    response = await fetcher.fetch_all()
    return response, api_conf
