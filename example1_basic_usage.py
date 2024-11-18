from pprint import pprint
from jsonquery import jsonquery

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
