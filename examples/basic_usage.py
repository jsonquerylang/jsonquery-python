from pprint import pprint
from jsonquery import jsonquery, compile

data = [
    {"name": "Chris", "age": 23, "scores": [7.2, 5, 8.0]},
    {"name": "Joe", "age": 32, "scores": [6.1, 8.1]},
    {"name": "Emily", "age": 19},
]

# use the text format
pprint(jsonquery(data, 'sort(.age, "desc")'))
# [{'age': 32, 'name': 'Joe', 'scores': [6.1, 8.1]},
#  {'age': 23, 'name': 'Chris', 'scores': [7.2, 5, 8.0]},
#  {'age': 19, 'name': 'Emily'}]

# use the JSON format
pprint(jsonquery(data, ["sort", ["get", "age"], "desc"]))
# [{'age': 32, 'name': 'Joe', 'scores': [6.1, 8.1]},
#  {'age': 23, 'name': 'Chris', 'scores': [7.2, 5, 8.0]},
#  {'age': 19, 'name': 'Emily'}]

# use the function `compile` to compile once and execute repeatedly
execute = compile(["sort"])
pprint(execute([32, 19, 23]))  # [19, 23, 32]
pprint(execute([5, 2, 7, 4]))  # [2, 4, 5, 7]
