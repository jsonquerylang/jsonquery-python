from typing import TypeAlias, List, Mapping, TypedDict, Callable, NotRequired

JsonType: TypeAlias = List["JsonValueType"] | Mapping[str, "JsonValueType"]
JsonValueType: TypeAlias = str | int | float | None | JsonType


# TODO: improve this type definition to be a list with a string followed by zero or multiple JsonType's
JsonQueryType: TypeAlias = list[str | JsonType]


class JsonQueryOptions(TypedDict):
    functions: NotRequired[Mapping[str, Callable]]
