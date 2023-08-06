from typing import Any


def convert_to_dict(target: Any):
    result = dict(target).copy()

    for key, value in dict(target).items():
        if isinstance(value, dict):
            remove_none_properties(value)
        elif value is None:
            result.pop(key)

    return result


def remove_none_properties(target: dict):
    result = target.copy()

    for key, value in target.items():
        if isinstance(value, dict):
            remove_none_properties(value)
        elif value is None:
            result.pop(key)

    return result
