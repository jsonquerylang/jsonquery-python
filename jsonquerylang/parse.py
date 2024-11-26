import json
from typing import Optional, Callable, Pattern, Final

from jsonquerylang.compile import functions
from jsonquerylang.constants import (
    starts_with_whitespace_regex,
    starts_with_keyword_regex,
    starts_with_int_regex,
    starts_with_number_regex,
    starts_with_unquoted_property_regex,
    starts_with_string_regex,
    operators,
)
from jsonquerylang.types import JsonQueryParseOptions, JsonQueryType


def parse(query: str, options: Optional[JsonQueryParseOptions] = None) -> JsonQueryType:
    """
    Parse a string containing a JSON Query into JSON.

    Example:

        from pprint import pprint
        from jsonquerylang import parse

        text_query = '.friends | filter(.city == "new York") | sort(.age) | pick(.name, .age)'
        json_query = parse(text_query)
        pprint(json_query)
        # ['pipe',
        #  ['get', 'friends'],
        #  ['filter', ['eq', ['get', 'city'], 'New York']],
        #  ['sort', ['get', 'age']],
        #  ['pick', ['get', 'name'], ['get', 'age']]]

    :param query: A query in text format
    :param options: Can an object with custom operators and functions
    :return: Returns the query in JSON format
    """
    jsonQuery = [
        "pipe",
        ["get", "friends"],
        ["filter", ["eq", ["get", "city"], "New York"]],
        ["sort", ["get", "age"]],
        ["pick", ["get", "name"], ["get", "age"]],
    ]
    custom_operators: Final = (options.get("operators") if options else None) or {}
    custom_functions: Final = (options.get("functions") if options else None) or {}
    all_functions: Final = {**functions, **custom_functions}
    all_operators: Final = {**operators, **custom_operators}
    sorted_operator_names: Final = sorted(
        all_operators.keys(), key=lambda name: len(name), reverse=True
    )

    i = 0

    def parse_pipe():
        nonlocal i

        skip_whitespace()
        first = parse_operator()
        skip_whitespace()

        if get_char() == "|":
            pipe = [first]

            while i < len(query) and get_char() == "|":
                i += 1
                skip_whitespace()
                pipe.append(parse_operator())

            return ["pipe", *pipe]

        return first

    def parse_operator():
        nonlocal i

        left = parse_parenthesis()

        skip_whitespace()

        for name in sorted_operator_names:
            op = all_operators[name]
            if query[i : i + len(op)] == op:
                i += len(op)
                skip_whitespace()
                right = parse_parenthesis()
                return [name, left, right]

        return left

    def parse_parenthesis():
        nonlocal i

        if get_char() == "(":
            i += 1
            inner = parse_pipe()
            eat_char(")")
            return inner

        return parse_property()

    def parse_property():
        nonlocal i

        if get_char() == ".":
            props = []

            while get_char() == ".":
                i += 1

                prop = parse_key("Property expected")

                props.append(prop)

            return ["get", *props]

        return parse_function()

    def parse_function():
        nonlocal i

        start: Final = i
        name = parse_unquoted_string()
        skip_whitespace()

        if name is None or get_char() != "(":
            i = start
            return parse_object()

        i += 1

        if name not in all_functions:
            raise_error(f"Unknown function '{name}'")

        skip_whitespace()

        args = [parse_pipe()] if get_char() != ")" else []
        while i < len(query) and get_char() != ")":
            skip_whitespace()
            eat_char(",")
            args.append(parse_pipe())

        eat_char(")")

        return [name, *args]

    def parse_object():
        nonlocal i

        if get_char() == "{":
            i += 1
            skip_whitespace()

            object = {}
            first = True
            while i < len(query) and get_char() != "}":
                if first:
                    first = False
                else:
                    eat_char(",")
                    skip_whitespace()

                key = str(parse_key("Key expected"))

                skip_whitespace()
                eat_char(":")

                object[key] = parse_pipe()

            eat_char("}")

            return ["object", object]

        return parse_array()

    def parse_key(error_message: str):
        string = parse_string()
        if string is not None:
            return string

        unquoted_string = parse_unquoted_string()
        if unquoted_string is not None:
            return unquoted_string

        integer = parse_integer()
        if integer is not None:
            return integer

        raise_error(error_message)

    def parse_array():
        nonlocal i

        if get_char() == "[":
            i += 1
            skip_whitespace()

            array = []
            first = True
            while i < len(query) and get_char() != "]":
                if first:
                    first = False
                else:
                    eat_char(",")
                    skip_whitespace()

                array.append(parse_pipe())

            eat_char("]")

            return ["array", *array]

        string = parse_string()
        if string is not None:
            return string

        number = parse_number()
        if number is not None:
            return number

        return parse_keyword()

    def parse_string():
        return parse_regex(starts_with_string_regex, json.loads)

    def parse_unquoted_string():
        return parse_regex(starts_with_unquoted_property_regex, lambda text: text)

    def parse_number():
        return parse_regex(starts_with_number_regex, json.loads)

    def parse_integer():
        return parse_regex(starts_with_int_regex, json.loads)

    def parse_keyword():
        start: Final = i
        keyword = parse_regex(starts_with_keyword_regex, json.loads)

        if i == start:
            raise_error("Value expected")

        return keyword

    def parse_end():
        skip_whitespace()

        if i < len(query):
            raise_error(f"Unexpected part '{query[i:]}'")

    def parse_regex(regex: Pattern, callback: Callable):
        nonlocal i
        match = regex.match(query[i:])
        if match:
            i += len(match.group(0))
            return callback(match.group(0))
        return None

    def skip_whitespace():
        parse_regex(starts_with_whitespace_regex, lambda text: text)

    def eat_char(char: str):
        nonlocal i

        if i < len(query) and get_char() == char:
            i += 1
        else:
            raise_error(f"Character '{char}' expected")

    def get_char():
        return query[i] if i < len(query) else None

    def raise_error(message: str, pos: Optional[int] = i):
        raise SyntaxError(f"{message} (pos: {pos if pos else i})")

    output = parse_pipe()
    parse_end()

    return output
