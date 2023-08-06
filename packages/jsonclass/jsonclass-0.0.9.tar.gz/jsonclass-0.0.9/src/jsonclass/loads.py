import json
from typing import Dict, Any

from .jsonclass import JSONClass


def object_hook(data: Dict[str, Any]):
    if JSONClass.deserializable(data):
        return JSONClass.load(data)
    else:
        return data


def loads(data: str):
    return json.loads(data, object_hook=object_hook)
