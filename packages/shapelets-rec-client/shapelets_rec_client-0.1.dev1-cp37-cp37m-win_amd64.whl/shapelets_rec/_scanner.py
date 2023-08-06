
from typing import Any, Union, List
from .services import FieldScan, ValueHolder, IntValueHolder, FloatValueHolder, BoolValueHolder, StringValueHolder, ListValueHolder

from uuid import uuid4


def _validate_pointer(pointer: str) -> str:
    if pointer is None:
        raise ValueError("Pointer is none")
    if not isinstance(pointer, str):
        raise ValueError("Pointers should be strings")
    p = pointer.strip()
    if len(p) == 0:
        raise ValueError(f"Pointer is an empty string")
    if not p.startswith('/'):
        raise ValueError(f"Pointer {p} should start with '/'")
    if '*' in p:
        raise ValueError(f"Pointer {p} should not be a wildcard expression")
    return p


def wrap_value(value: Union[str, float, int, bool]) -> ValueHolder:
    if isinstance(value, str):
        return StringValueHolder(value=value)
    elif isinstance(value, int):
        return IntValueHolder(value=value)
    elif isinstance(value, float):
        return FloatValueHolder(value=value)
    elif isinstance(value, bool):
        return BoolValueHolder(value=value)
    elif isinstance(value, List):
        return ListValueHolder(value=[wrap_value(x) for x in value])
    raise ValueError(f"{value} should be of type int, float, str or bool")


def eq(pointer: str, value: Union[List[Any], str, float, int, bool]) -> FieldScan:
    return FieldScan(id=uuid4(), projection=_validate_pointer(pointer), operation='eq', value=wrap_value(value))


def neq(pointer: str, value: Union[str, float, int, bool]) -> FieldScan:
    return FieldScan(id=uuid4(), projection=_validate_pointer(pointer), operation='neq', value=wrap_value(value))


def lt(pointer: str, value: Union[str, float, int, bool]) -> FieldScan:
    return FieldScan(id=uuid4(), projection=_validate_pointer(pointer), operation='lt', value=wrap_value(value))


def gt(pointer: str, value: Union[str, float, int, bool]) -> FieldScan:
    return FieldScan(id=uuid4(), projection=_validate_pointer(pointer), operation='gte', value=wrap_value(value))


def lte(pointer: str, value: Union[str, float, int, bool]) -> FieldScan:
    return FieldScan(id=uuid4(), projection=_validate_pointer(pointer), operation='gte', value=wrap_value(value))


def gte(pointer: str, value: Union[str, float, int, bool]) -> FieldScan:
    return FieldScan(id=uuid4(), projection=_validate_pointer(pointer), operation='gte', value=wrap_value(value))


# in is a reserved word. 'il' stands for 'in list'
def il(pointer: str, value: Union[str, float, int, bool]) -> FieldScan:
    return FieldScan(id=uuid4(), projection=_validate_pointer(pointer), operation='il', value=wrap_value(value))


def ni(pointer: str, value: Union[str, float, int, bool]) -> FieldScan:
    return FieldScan(id=uuid4(), projection=_validate_pointer(pointer), operation='ni', value=wrap_value(value))