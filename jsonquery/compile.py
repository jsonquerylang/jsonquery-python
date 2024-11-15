from typing import Callable, Optional, Final

from jsonquery.functions import get_functions
from jsonquery.types import JsonQueryType, JsonType, JsonQueryOptions


def compile(
    query: JsonQueryType, options: Optional[JsonQueryOptions] = None
) -> Callable[[JsonType], JsonType]:
    """
    Compile a JSON Query

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
