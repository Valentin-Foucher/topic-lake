import copy
import importlib
from typing import Any, Type
from uuid import uuid4

from frozendict import frozendict


def wrap(obj: Any) -> list[Any]:
    return obj if isinstance(obj, list) else [obj]


def get_nested_element(o: dict[str, Any] | list[Any], path: str) -> Any:
    """
    Recursive function allowing to find nested values inside a complex structure.
    Returned value is a copy of the actual value, thus it cannot update the value from the originated dict or list

    eg: o: [
        {
            "a": [
                "b",
                {
                    "c": "d"
                }
            ],
            "e": "f"
        }
    ]
    >>> get_nested_element(o, '0.a.1.c')
    "d"
    >>> get_nested_element(o, '0.e')
    "f"
    >>> get_nested_element(o, '0.a')
    ("b", {"c": "d"})

    :param o: a dict or a list
    :param path: the path towards the value
    :return: the desired value or None if it does not exist
    """
    v = copy.deepcopy(o)
    for p in path.split('.'):
        if isinstance(v, dict) and p not in v:
            return None
        elif isinstance(v, list):
            try:
                if int(p) > len(v) - 1:
                    raise ValueError
                p = int(p)
            except ValueError:
                return None

        v = v[p]

    if isinstance(v, dict):
        v = frozendict(v)
    elif isinstance(v, list):
        v = tuple(v)

    return v


def get_object_by_name(name: str) -> Type:
    module_name, object_name = name.rsplit('.', 1)
    module = importlib.import_module(module_name)
    return getattr(module, object_name)
