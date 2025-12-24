
import importlib
from types import ModuleType
from typing import Any

_backend: ModuleType | None = None
_backend_name: str | None = None

def _load_backend() -> ModuleType:
    global _backend, _backend_name
    if _backend is not None:
        return _backend
    try:
        _backend = importlib.import_module("google.genai")
        _backend_name = "google.genai"
    except Exception:
        _backend = importlib.import_module("google.generativeai")
        _backend_name = "google.generativeai"
    return _backend

def __getattr__(name: str) -> Any:
    mod = _load_backend()
    return getattr(mod, name)

def __dir__() -> list[str]:
    mod = _load_backend()
    public = [n for n in dir(mod) if not n.startswith("_")]
    return sorted(list(globals().keys()) + public)

def _which_backend() -> str | None:
    return _backend_name
