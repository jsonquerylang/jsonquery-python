from jsonquerylang import jsonquery, JsonQueryOptions


def times(value):
    return lambda array: list(map(lambda item: item * value, array))


data = [2, 3, 8]
query = ["times", 2]
options: JsonQueryOptions = {"functions": {"times": times}}

print(jsonquery(data, query, options))
# [4, 6, 16]
