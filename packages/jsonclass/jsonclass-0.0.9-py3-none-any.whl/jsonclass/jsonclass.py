from typing import Dict, Type, Any

_json_classes: Dict[str, Type['JSONClass']] = {}


class JSONClass:
    _data: Dict[str, Any]

    def __init_subclass__(cls):
        object.__init_subclass__()
        _json_classes[cls.__qualname__] = cls

    @staticmethod
    def deserializable(data: Dict[str, Any]):
        return "__json_class__" in data

    @staticmethod
    def load(data: Dict[str, Any]):
        cls = _json_classes[data["__json_class__"]]
        del data["__json_class__"]
        return cls(data)

    def __init__(self, data: Dict[str, Any] = None, /, **kwargs):
        object.__setattr__(
            self,
            "_data",
            dict(data or {}, **kwargs)
        )

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

    def to_dict(self):
        return dict(self._data, __json_class__=self.__class__.__qualname__)
