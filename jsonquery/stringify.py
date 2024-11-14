import json
import re
from typing import List, Optional, Union

from jsonquery.functions import get_functions
from jsonquery.types import (
    JsonQueryType,
    JsonQueryStringifyOptions,
    JsonQueryObjectType,
    JsonPath,
    JsonQueryFunctionType,
)

DEFAULT_MAX_LINE_LENGTH = 40
DEFAULT_INDENTATION = "  "

unquoted_property_regex = re.compile(r"^[a-zA-Z_$][a-zA-Z0-9_$]*$")

built_in_operators = {
    "and": "and",
    "or": "or",
    "eq": "==",
    "gt": ">",
    "gte": ">=",
    "lt": "<",
    "lte": "<=",
    "ne": "!=",
    "add": "+",
    "subtract": "-",
    "multiply": "*",
    "divide": "/",
    "pow": "^",
    "mod": "%",
    "in": "in",
    "not in": "not in",
}

functions = get_functions(compile)


def stringify(
    query: JsonQueryType, options: Optional[JsonQueryStringifyOptions] = None
) -> str:
    space = (options.get("indentation") if options else None) or DEFAULT_INDENTATION
    max_line_length = (
        options.get("max_line_length") if options else None
    ) or DEFAULT_MAX_LINE_LENGTH
    operators = options.get("operators", built_in_operators) if options else None

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

        op = (operators.get(name) if operators else None) or built_in_operators.get(
            name
        )
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
