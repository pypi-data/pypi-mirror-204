from os import environ

from httpx import AsyncClient

__all__ = ["import_module", "RegiusModule"]


class RegiusModule(object):
    _endpoint_override: dict[str, str] = {}
    _endpoint_template = environ.get("REGIUS_ENDPOINT_TEMPLATE", "http://{name}")

    def __init__(self, name: str):
        endpoint = self._endpoint_override.get(name)
        if endpoint is None:
            endpoint = self._endpoint_template.format(name=name)

        self._client = AsyncClient(base_url=endpoint)

    def __getattr__(self, name: str):
        return _create_rpc(self._client, name)


def import_module(name: str):
    return RegiusModule(name)


def _create_rpc(client: AsyncClient, name: str):
    async def rpc(*args, **kwargs):
        if args and kwargs:
            raise ValueError("Cannot specify both args and kwargs")

        response = await client.post(name, json=kwargs or args)
        response.raise_for_status()
        return response.json()

    rpc.__name__ = name

    return rpc
