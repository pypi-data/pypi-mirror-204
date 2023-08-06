import json
from typing import Any

from .jsonclass import JSONClass


def default(data: JSONClass):
    return data.to_dict()


def dumps(data: Any):
    return json.dumps(data, default=default)
