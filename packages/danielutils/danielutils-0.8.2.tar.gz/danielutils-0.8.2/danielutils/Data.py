import json
from .Decorators import validate


@validate
def dict_to_json(d: dict) -> str:
    return json.dumps(d, indent=4)


@validate
def json_to_dict(j: str) -> dict:
    return json.loads(j)


__all__ = [
    "dict_to_json",
    "json_to_dict"
]
