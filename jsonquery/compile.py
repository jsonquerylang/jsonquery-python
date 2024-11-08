from jsonquery.types import JsonQueryType, JsonType, JsonQueryOptions
from typing import Callable
from jsonquery.functions import get_functions


def compile(
    query: JsonQueryType, options: JsonQueryOptions | None = None
) -> Callable[[JsonType], JsonType]:
    """
    Compile a JSON Query

    :param query: A JSON Query
    :param options: Can an object with custom functions
    :return: Returns a function which can execute the query
    """

    fn_name, *args = query

    functions = (
        {**built_in_functions, **options["functions"]}
        if (options is not None) and ("functions" in options)
        else built_in_functions
    )

    if fn_name not in functions:
        raise SyntaxError(f'Unknown function "{fn_name}"')

    fn = functions[fn_name]

    return fn(*args)


built_in_functions = get_functions(compile)
