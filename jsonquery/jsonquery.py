from jsonquery.types import JsonType, JsonQueryType, JsonQueryOptions
from jsonquery.compile import compile


def jsonquery(
    data: JsonType, query: JsonQueryType, options: JsonQueryOptions | None = None
) -> JsonType:
    """
    Compile and evaluate a query

    :param data: The JSON document to be queried
    :param query: A JSON Query
    :param options: Can an object with custom functions
    :return: Returns the result of the query applied to the data
    """

    evaluate = compile(query, options)

    return evaluate(data)
