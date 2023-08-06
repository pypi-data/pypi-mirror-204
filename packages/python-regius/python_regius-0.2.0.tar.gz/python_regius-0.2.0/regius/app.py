from importlib.util import module_from_spec, spec_from_file_location
from inspect import iscoroutine, isfunction
from types import ModuleType

from sanic import BadRequest, NotFound, Request, Sanic, json
from sanic.log import logger

__all__ = ["RegiusApp"]


class RegiusApp(Sanic):
    _logger = logger.getChild("regius")

    def __init__(self, module: ModuleType, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.ctx._module = module

        self.add_route(self._handler, "/<name>", methods=["POST"])

    def refresh(self, *args, **kwargs):
        spec = self.ctx._module.__spec__
        assert spec is not None

        loader = spec.loader
        assert loader is not None

        loader.exec_module(self.ctx._module)

        return super().refresh(*args, **kwargs)

    @classmethod
    def from_path(cls, path: str, *args, **kwargs):
        module = _load_module(path)

        return cls(module, *args, **kwargs)

    async def _handler(self, request: Request, name: str):
        try:
            assert not name.startswith("_")
            func = getattr(self.ctx._module, name)
            assert isfunction(func)
        except (AttributeError, AssertionError):
            raise NotFound

        body = request.json

        if isinstance(body, list):
            self._logger.info("--> %s(%r)", name, body)
            result = func(*body)
        elif isinstance(body, dict):
            self._logger.info("--> %s(%r)", name, body)
            result = func(**body)
        else:
            raise BadRequest("Invalid request body, expected array or object")

        if iscoroutine(result):
            result = await result

        self._logger.info("<-- %s(%r) = %r", name, body, result)

        return json(result)


def _load_module(path: str):
    try:
        spec = spec_from_file_location("regius_module", path)
        assert spec is not None

        loader = spec.loader
        assert loader is not None

        module = module_from_spec(spec)
        loader.exec_module(module)

        return module
    except (FileNotFoundError, AssertionError) as exc:
        raise ModuleNotFoundError(f"Could not find module at {path}") from exc
