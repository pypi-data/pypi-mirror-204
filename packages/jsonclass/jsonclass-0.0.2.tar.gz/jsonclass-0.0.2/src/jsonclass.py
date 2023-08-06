from typing import Dict, Type, Any

_json_classes: Dict[str, Type['JSONClass']] = {}


class JSONClass:
    __json_data: Dict

    def __init_subclass__(cls):
        object.__init_subclass__()
        _json_classes[cls.__qualname__] = cls

    def __new__(cls, data: Dict[str, Any] = None):
        __data = data or {}
        __data["__json_class__"] = cls.__qualname__
        __instance = object.__new__(_json_classes[__data["__json_class__"]])
        object.__setattr__(__instance, "__json_data", __data)
        return __instance

    def __getattr__(self, item):
        return object.__getattribute__(self, "__json_data")[item]

    def __setattr__(self, key, value):
        object.__getattribute__(self, "__json_data")[key] = value

    def to_json(self):
        return object.__getattribute__(self, "__json_data")
