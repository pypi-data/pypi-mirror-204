import logging

from regius.module import RegiusModule

logging.basicConfig(level=logging.INFO)


def __getattr__(name: str) -> RegiusModule:
    if name.startswith("_"):
        raise AttributeError(f"module {__name__} has no attribute {name}")

    if name == "app":
        from os import getcwd
        from os.path import basename, join

        from .app import RegiusApp

        cwd = getcwd()
        name = basename(cwd)
        return RegiusApp.from_path(join(cwd, "__init__.py"), name=name)  # type: ignore

    from .module import RegiusModule

    return RegiusModule(name)


del RegiusModule
del logging
