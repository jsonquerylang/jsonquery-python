import json
from typing import List, Optional, Union, Final

from jsonquerylang.constants import operators, unquoted_property_regex
from jsonquerylang.types import (
    JsonQueryType,
    JsonQueryStringifyOptions,
    JsonQueryObjectType,
    JsonPath,
    JsonQueryFunctionType,
)

DEFAULT_MAX_LINE_LENGTH = 40
DEFAULT_INDENTATION = "  "


def stringify(
    query: JsonQueryType, options: Optional[JsonQueryStringifyOptions] = None
) -> str:
    """
    Stringify a JSON Query into a readable, human friendly text syntax.

    Example:

        from jsonquerylang import stringify

        jsonQuery = [
            "pipe",
            ["get", "friends"],
            ["filter", ["eq", ["get", "city"], "New York"]],
            ["sort", ["get", "age"]],
            ["pick", ["get", "name"], ["get", "age"]],
        ]
        textQuery = stringify(jsonQuery)
        print(textQuery)
        # '.friends | filter(.city == "new York") | sort(.age) | pick(.name, .age)'

    :param query: A JSON Query
    :param options: A dict with custom operators, max_line_length, and indentation
    :return: Returns a human friendly string representation of the query
    """

    space: Final = (
        options.get("indentation") if options else None
    ) or DEFAULT_INDENTATION
    max_line_length: Final = (
        options.get("max_line_length") if options else None
    ) or DEFAULT_MAX_LINE_LENGTH
    custom_operators: Final = (options.get("operators") if options else None) or {}
    all_operators: Final = {**operators, **custom_operators}

    def _stringify(_query: JsonQueryType, indent: str) -> str:
        if isinstance(_query, list):
            return stringify_function(_query, indent)
        else:
            return json.dumps(_query)  # value (string, number, boolean, null)

    def stringify_function(query_fn: JsonQueryFunctionType, indent: str) -> str:
        name, *args = query_fn

        if name == "get" and len(args) > 0:
            return stringify_path(args)

        if name == "pipe":
            args_str = stringify_args(args, indent + space)
            return join(args_str, ["", " | ", ""], ["", f"\n{indent + space}| ", ""])

        if name == "object":
            return stringify_object(args[0], indent)

        if name == "array":
            args_str = stringify_args(args, indent + space)
            return join(
                args_str,
                ["[", ", ", "]"],
                [f"[\n{indent + space}", f",\n{indent + space}", f"\n{indent}]"],
            )

        op = all_operators.get(name)
        if op is not None and len(args) == 2:
            left, right = args
            left_str = _stringify(left, indent)
            right_str = _stringify(right, indent)
            return f"({left_str} {op} {right_str})"

        child_indent = indent if len(args) == 1 else indent + space
        args_str = stringify_args(args, child_indent)
        return (
            f"{name}{args_str[0]}"
            if len(args) == 1 and args_str[0][0] == "("
            else join(
                args_str,
                [f"{name}(", ", ", ")"],
                (
                    [f"{name}(", f",\n{indent}", ")"]
                    if len(args) == 1
                    else [
                        f"{name}(\n{child_indent}",
                        f",\n{child_indent}",
                        f"\n{indent})",
                    ]
                ),
            )
        )

    def stringify_object(query_obj: JsonQueryObjectType, indent: str) -> str:
        child_indent = indent + space
        entries = [
            f"{stringify_property(key)}: {_stringify(value, child_indent)}"
            for key, value in query_obj.items()
        ]
        return join(
            entries,
            ["{ ", ", ", " }"],
            [f"{{\n{child_indent}", f",\n{child_indent}", f"\n{indent}}}"],
        )

    def stringify_args(args: List, indent: str) -> List[str]:
        return list(map(lambda arg: _stringify(arg, indent), args))

    def stringify_path(path: JsonPath) -> str:
        return "".join([f".{stringify_property(prop)}" for prop in path])

    def stringify_property(prop: Union[str, int]) -> str:
        prop_str = str(prop)
        return prop_str if unquoted_property_regex.match(prop_str) else json.dumps(prop)

    def join(items: List[str], compact: List[str], formatted: List[str]) -> str:
        compact_start, compact_separator, compact_end = compact
        format_start, format_separator, format_end = formatted

        compact_length = (
            len(compact_start)
            + sum(len(item) + len(compact_separator) for item in items)
            - len(compact_separator)
            + len(compact_end)
        )
        if compact_length <= max_line_length:
            return compact_start + compact_separator.join(items) + compact_end
        else:
            return format_start + format_separator.join(items) + format_end

    return _stringify(query, "")
