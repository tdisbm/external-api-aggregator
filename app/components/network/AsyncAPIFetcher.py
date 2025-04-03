import asyncio
import logging
from typing import List, Iterable, Coroutine

from app.components.dto.network.OffsetConfig import OffsetConfig
from app.components.network.AsyncAPIClient import AsyncAPIClient

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


class AsyncAPIFetcher:
    def __init__(self,
                 client: AsyncAPIClient,
                 offset: OffsetConfig,
                 max_concurrent_calls: int = 1,
                 ):
        self.client = client
        self.max_concurrent_calls = max_concurrent_calls
        self.offset = offset

    async def fetch_all(self) -> List:
        responses_all: List = []
        skip = self.offset.skip

        while True:
            responses_last = await self._fetch_next_batch(skip=skip)
            responses_all.extend(responses_last)
            skip += len(responses_last)
            if self._is_fetch_done(responses_last, responses_all):
                break

        return responses_all

    async def _fetch_next_batch(self, skip: int) -> List:
        offset_copy = self.offset.model_copy()
        offset_copy.skip = skip
        responses = await asyncio.gather(*_generate_api_calls(
            client=self.client,
            offset=offset_copy,
            max_concurrent_calls=self.max_concurrent_calls
        ))

        return _generate_response_data(responses)

    def _is_fetch_done(self, responses_last: List, responses_all: List) -> bool:
        if not responses_last:
            return True
        if len(responses_last) < self.offset.take * self.max_concurrent_calls:
            return True
        if self.offset.limit and len(responses_all) >= self.offset.limit:
            return True
        return False


def _generate_response_data(responses: Iterable) -> List:
    responses_clean = []
    for response in responses:
        if response:
            if isinstance(response, Iterable):
                responses_clean.extend(response)
            else:
                responses_clean.append(response)
    return responses_clean


def _generate_api_calls(client: AsyncAPIClient, offset: OffsetConfig, max_concurrent_calls: int) -> List[Coroutine]:
    skip = offset.skip
    take = offset.take
    return [
        client.fetch(method="POST", params={"skip": skip, "limit": take})
        for skip in range(skip, skip + (take * max_concurrent_calls), take)
    ]
