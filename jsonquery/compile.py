def compile(query):
    """
    Compile a JSON Query

    :param query: A JSON Query
    :return: Returns a function which can execute the query
    """

    fn_name, *args = query

    if fn_name not in functions:
        raise SyntaxError(f'Unknown function "{fn_name}"')

    fn = functions[fn_name]

    return fn(*args)


def get(*path: []):
    def getter(item):
        value = item

        for p in path:
            value = value[p] if (value is not None) else None

        return value

    return getter


def sort(path=None, direction="asc"):
    if path is None:
        path = ["get"]

    getter = compile(path)

    return lambda data: sorted(
        data,
        key=getter,
        reverse=direction == "desc",
    )


# TODO: implement all functions
functions = {"get": get, "sort": sort}
