import os.path
from importlib.util import module_from_spec, spec_from_file_location
from inspect import iscoroutinefunction, isfunction
from typing import Callable

from sanic import BadRequest, Request, Sanic, json
from sanic.log import logger

__all__ = ["app", "RegiusApp"]


class RegiusApp(Sanic):
    def __init__(self, path: str, *args, **kwargs):
        super().__init__(name="regius_app", *args, **kwargs)

        path = os.path.join(path, "__init__.py")
        module = _load_module(path)
        _install_handlers(self, module.__dict__)


def app(*args, **kwargs):
    import os

    return RegiusApp(path=os.getcwd(), *args, **kwargs)


def _load_module(path: str):
    try:
        spec = spec_from_file_location("regius_module", path)
        assert spec is not None, "Could not get module spec"

        loader = spec.loader
        assert loader is not None, "Could not get module loader from spec"

        module = module_from_spec(spec)
        loader.exec_module(module)

        return module
    except (FileNotFoundError, AssertionError) as exc:
        raise ModuleNotFoundError(f"Could not find module at {path}") from exc


def _install_handlers(app: Sanic, func_dict: dict[str, Callable]):
    for name, value in func_dict.items():
        if name.startswith("_"):
            continue

        if not isfunction(value):
            logger.warning("Skipping %s because it is not a function", name)
            continue

        logger.info("Registering function %s", name)
        handler = _create_handler(value)
        app.add_route(handler, f"/{name}", methods=["POST"], name=name)


def _create_handler(func: Callable):
    if iscoroutinefunction(func):
        return _handle_async(func)
    else:
        return _handle_sync(func)


def _handle_async(func: Callable):
    async def handler(request: Request):
        data = request.json

        if isinstance(data, dict):
            logger.debug("Calling %r with dict %r", func, data)

            body = await func(**data)

            logger.debug("Calling %r with list %r got %r", func, data, body)

            return json(body)
        elif isinstance(data, list):
            logger.debug("Calling %r with list %r", func, data)

            body = await func(*data)

            logger.debug("Calling %r with list %r got %r", func, data, body)

            return json(body)
        else:
            raise BadRequest("Invalid request body, expected array or object")

    return handler


def _handle_sync(func: Callable):
    async def handler(request: Request):
        data = request.json

        if isinstance(data, dict):
            logger.debug("Calling %r with dict %r", func, data)

            body = func(**data)

            logger.debug("Calling %r with list %r got %r", func, data, body)

            return json(body)
        elif isinstance(data, list):
            logger.debug("Calling %r with list %r", func, data)

            body = func(*data)

            logger.debug("Calling %r with list %r got %r", func, data, body)

            return json(body)
        else:
            raise BadRequest("Invalid request body, expected array or object")

    return handler
