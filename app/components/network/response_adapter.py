from aiohttp import ClientResponse


async def async_json_adapter(response: ClientResponse):
    return await response.json()
