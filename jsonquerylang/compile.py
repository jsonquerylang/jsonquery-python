import json
from typing import Any, Callable, Mapping, Optional, Final, cast
from jsonquerylang.functions import get_functions
from jsonquerylang.types import JsonQueryType, JsonType, JsonQueryOptions


CompileFunc = Callable[..., Callable[[Any], Any]]
FunctionDict = Mapping[str, Callable[..., Any]]


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

    if options is None:
        options = {}

    compile_inner: CompileFunc = lambda query: compile(query, options)

    builtin_functions: Final[FunctionDict] = get_functions(
        compile_inner, build_function
    )

    custom_functions: Final[FunctionDict] = cast(
        FunctionDict, options.get("functions", {})
    )

    custom_function_builders: Final[list[Callable[[CompileFunc], FunctionDict]]] = (
        options.get("function_builders", [])
    )

    built_custom_function_dicts = [
        function_builder(compile_inner) for function_builder in custom_function_builders
    ]

    function_dicts: list[FunctionDict] = [
        builtin_functions,
        custom_functions,
        *built_custom_function_dicts,
    ]

    all_functions = {
        function_name: function_instance
        for function_dict in function_dicts
        for function_name, function_instance in function_dict.items()
    }

    if type(query) is list:
        # a function like ["sort", ["get", "name"], "desc"]
        fn_name, *args = query

        if fn_name not in all_functions:
            raise SyntaxError(f'Unknown function "{fn_name}"')

        fn = all_functions[fn_name]

        return fn(*args)

    if type(query) is dict:
        raise SyntaxError(
            f'Function notation ["object", {{...}}] expected but got {json.dumps(query)}'
        )

    else:
        # a static value (string, number, boolean, or null)
        return lambda _: query


def build_function(fn):
    def evaluate_fn(*args):
        compiled_args = list(map(compile, args))

        return lambda data: fn(
            *list(map(lambda compiled_arg: compiled_arg(data), compiled_args))
        )

    return evaluate_fn
