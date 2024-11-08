# jsonquery-python

![JSON Query Logo](https://jsonquerylang.org/frog-756900-100.png)

This is the Python implementation of **JSON Query**, a small, flexible, and expandable JSON query language.

Try it out on the online playground: <https://jsonquerylang.org>

![JSON Query Overview](https://jsonquerylang.org/jsonquery-overview.svg)

## Install

The library is not yet published and requires a manual build. 

## Use

```python
from jsonquery import jsonquery, compile
from pprint import pprint

data = [
    {"name": "Chris", "age": 23, "scores": [7.2, 5, 8.0]},
    {"name": "Joe", "age": 32, "scores": [6.1, 8.1]},
    {"name": "Emily", "age": 19},
]

pprint(jsonquery(data, ["sort", ["get", "age"], "desc"]))
# [{'age': 32, 'name': 'Joe', 'scores': [6.1, 8.1]},
#  {'age': 23, 'name': 'Chris', 'scores': [7.2, 5, 8.0]},
#  {'age': 19, 'name': 'Emily'}]

# use the function `compile` to compile once and execute repeatedly on different JSON documents
execute = compile(["sort"])
pprint(execute([32, 19, 23])) # [19, 23, 32]
pprint(execute([5, 2, 7, 4])) # [2, 4, 5, 7]
```

## License

Released under the [ISC license](LICENSE.md).
