from jsonquerylang import jsonquery, compile, JsonQueryOptions


def about_eq(a, b):
    epsilon = 0.001
    a_compiled = compile(a, options)
    b_compiled = compile(b, options)

    return lambda data: abs(a_compiled(data) - b_compiled(data)) < epsilon


options: JsonQueryOptions = {
    "functions": {"aboutEq": about_eq},
    "operators": [{"name": "aboutEq", "op": "~=", "at": "=="}],
}

scores = [
    {"name": "Joe", "score": 2.0001, "previousScore": 1.9999},
    {"name": "Sarah", "score": 3, "previousScore": 1.5},
]
query = "filter(.score ~= .previousScore)"
unchanged_scores = jsonquery(scores, query, options)

print(unchanged_scores)
# [{'name': 'Joe', 'score': 2.0001, 'previousScore': 1.9999}]
