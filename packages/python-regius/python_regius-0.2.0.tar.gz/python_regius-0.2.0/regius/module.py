from logging import getLogger
from os import environ

from httpx import AsyncClient, Client

__all__ = ["RegiusModule", "RegiusAsyncModule"]

_endpoint_override: dict[str, str] = {}
_endpoint_template = "http://{name}"

getLogger("httpx").setLevel("INFO")

try:
    from dotenv import dotenv_values

    dotenv = dotenv_values(".env")
    env = environ.copy()
    env.update(**dotenv)
except ImportError:
    env = environ

if "REGIUS_ENDPOINT_TEMPLATE" in env:
    _endpoint_template = env["REGIUS_ENDPOINT_TEMPLATE"]


class RegiusModule(object):
    def __init__(self, name: str):
        if name in _endpoint_override:
            endpoint = _endpoint_override[name]
        else:
            endpoint = _endpoint_template.format(name=name)

        self._client = Client(base_url=endpoint)

    def __getattr__(self, name: str):
        def regius_method(*args, **kwargs):
            if args and kwargs:
                raise ValueError("Cannot specify both args and kwargs")

            response = self._client.post(name, json=kwargs or args)
            response.raise_for_status()
            return response.json()

        regius_method.__name__ = name

        return regius_method


class RegiusAsyncModule(object):
    def __init__(self, name: str):
        if name in _endpoint_override:
            endpoint = _endpoint_override[name]
        else:
            endpoint = _endpoint_template.format(name=name)

        self._client = AsyncClient(base_url=endpoint)

    def __getattr__(self, name: str):
        async def regius_method(*args, **kwargs):
            if args and kwargs:
                raise ValueError("Cannot specify both args and kwargs")

            response = await self._client.post(name, json=kwargs or args)
            response.raise_for_status()
            return response.json()

        regius_method.__name__ = name

        return regius_method
