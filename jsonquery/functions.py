def get_functions(compile):
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

    return {"get": get, "sort": sort}
