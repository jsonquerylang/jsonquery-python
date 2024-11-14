from typing import TypeAlias, List, Mapping, TypedDict, Callable, NotRequired

JsonType: TypeAlias = List["JsonValueType"] | Mapping[str, "JsonValueType"]
JsonValueType: TypeAlias = str | int | float | None | JsonType

JsonPath = List[str | int]

# TODO: improve this type definition to be a list with a string followed by zero or multiple JsonType's
JsonQueryType: TypeAlias = list[str | JsonType] | JsonType
JsonQueryFunctionType: TypeAlias = list[str | JsonType]
JsonQueryObjectType: TypeAlias = Mapping[str, JsonQueryType]


class JsonQueryOptions(TypedDict):
    functions: NotRequired[Mapping[str, Callable]]


class JsonQueryStringifyOptions(TypedDict):
    operators: NotRequired[Mapping[str, str]]
    max_line_length: NotRequired[int]
    indentation: NotRequired[str]
