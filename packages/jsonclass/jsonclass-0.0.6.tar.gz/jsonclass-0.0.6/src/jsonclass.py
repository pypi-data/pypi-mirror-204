from functools import singledispatch
from typing import Dict, Type, Any

_json_classes: Dict[str, Type['JSONClass']] = {}


class JSONClass:
    _data: Dict[str, Any]

    def __init_subclass__(cls):
        object.__init_subclass__()
        _json_classes[cls.__qualname__] = cls

    def __new__(cls, data: Dict[str, Any] = None, /, **kwargs):
        _instance = object.__new__(cls)
        object.__setattr__(_instance, "_data", dict(data or {}, **kwargs, __json_class__=cls.__qualname__))
        return _instance

    def __getattr__(self, item):
        if item not in self._data:
            typ = self.__class__.__annotations__[item]
            if issubclass(typ, (JSONClass, list, set, dict)):
                self._data[item] = typ()
            else:
                raise AttributeError
        return self._data[item]

    def __setattr__(self, key, value):
        self._data[key] = value

    def to_json(self):
        return {
            name: value.to_json() if isinstance(value, JSONClass) else value
            for name, value in self._data.items()
        }


@singledispatch
def load(data):
    return data


@load.register
def _(data: dict):
    if "__json_class__" in data:
        class_name = data["__json_class__"]
        del data["__json_class__"]
        return _json_classes[class_name]({key: load(value) for key, value in data.items()})
    else:
        return data
