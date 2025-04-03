import logging
from typing import Optional, Callable

from aiohttp import ClientSession
from aiohttp.typedefs import LooseHeaders
from tenacity import wait_exponential, stop_after_attempt, Retrying

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


class AsyncAPIClient:
    def __init__(self,
                 url: str,
                 response_adapter: Callable,
                 headers: Optional[LooseHeaders] = None,
                 retries: int = 3):
        self.url = url
        self.headers = headers
        self.retry_threshold = retries
        self.response_adapter = response_adapter

    async def fetch(self, method: str, params: dict):
        retrying = Retrying(
            stop=stop_after_attempt(self.retry_threshold),
            wait=wait_exponential(multiplier=1, min=2, max=10)
        )

        for attempt in retrying:
            with attempt:
                return await self._fetch(method, params)

    async def _fetch(self, method: str, params: dict):
        async with ClientSession() as session:
            request_executor = getattr(session, method.lower(), None)

            if not callable(request_executor):
                raise AttributeError(f"Unknown method '{method}'")

            request_kwargs = {
                'url': self.url,
                'headers': self.headers,
                'params': params
            }

            try:
                logger.info(f"[+] Request - URL: {self.url}, METHOD: {method}, PARAMS: {params}")

                async with request_executor(**request_kwargs) as response:
                    if self.response_adapter:
                        return await self.response_adapter(response)
                    return response

            except Exception as e:
                logger.error(f"[-] Request failed - Error: {e}")
                return None
