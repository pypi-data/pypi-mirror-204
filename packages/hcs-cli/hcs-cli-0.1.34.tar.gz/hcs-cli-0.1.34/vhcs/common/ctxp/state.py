from . import jsondot
from typing import Any
import os


class state_file:
    def __init__(self, file_path: str):
        self._path = file_path
        self._cache = None

    def _data(self, reload: bool = False):
        if self._cache is None or reload:
            self._cache = jsondot.load(self._path, {})
        return self._cache

    def get(self, key: str, default: Any, reload: bool = False):
        return self._data(reload).get(key, default)

    def set(self, key: str, value: Any):
        self._data()[key] = value
        jsondot.save(self._cache, self._path)


_file: state_file = None


def _init(store_path: str, name: str):
    global _file
    _file = state_file(os.path.join(store_path, name))


def get(key: str, default: Any, reload: bool = False):
    return _file.get(key=key, default=default, reload=reload)


def set(key: str, value: Any):
    _file.set(key, value)
