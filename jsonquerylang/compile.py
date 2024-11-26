from typing import Callable, Optional, Final

from jsonquerylang.functions import get_functions
from jsonquerylang.types import JsonQueryType, JsonType, JsonQueryOptions


def compile(
    query: JsonQueryType, options: Optional[JsonQueryOptions] = None
) -> Callable[[JsonType], JsonType]:
    """
    Compile a JSON Query.

    Example:

        from pprint import pprint
        from jsonquerylang import compile

        input = [
            {"name": "Chris", "age": 23, "scores": [7.2, 5, 8.0]},
            {"name": "Joe", "age": 32, "scores": [6.1, 8.1]},
            {"name": "Emily", "age": 19},
        ]
        query = ["sort", ["get", "age"], "desc"]
        queryMe = compile(query)
        output = queryMe(input)
        pprint(output)
        # [{'age': 32, 'name': 'Joe', 'scores': [6.1, 8.1]},
        #  {'age': 23, 'name': 'Chris', 'scores': [7.2, 5, 8.0]},
        #  {'age': 19, 'name': 'Emily'}]

    :param query: A JSON Query
    :param options: Can an object with custom functions
    :return: Returns a function which can execute the query
    """

    custom_functions: Final = (options.get("functions") if options else None) or {}
    all_functions: Final = {**functions, **custom_functions}

    if isinstance(query, list):
        # a function like ["sort", ["get", "name"], "desc"]
        fn_name, *args = query

        if fn_name not in all_functions:
            raise SyntaxError(f'Unknown function "{fn_name}"')

        fn = all_functions[fn_name]

        return fn(*args)

    else:
        # a static value (string, number, boolean, or null)
        return lambda _: query


functions = get_functions(compile)