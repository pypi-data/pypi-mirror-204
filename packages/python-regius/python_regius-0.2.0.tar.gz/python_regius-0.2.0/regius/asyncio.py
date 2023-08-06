def __getattr__(name: str):
    if name.startswith("_"):
        raise AttributeError(f"module {__name__} has no attribute {name}")

    from .module import RegiusAsyncModule

    return RegiusAsyncModule(name)
