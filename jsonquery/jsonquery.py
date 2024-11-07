from jsonquery.compile import compile


def jsonquery(data, query):
    """
    Compile and evaluate a query

    :param data: The JSON document to be queried
    :param query: A JSON Query
    :return: Returns the result of the query applied to the data
    """

    evaluate = compile(query)

    return evaluate(data)
