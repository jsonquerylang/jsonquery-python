from functools import reduce
from typing import Mapping
from jsonquerylang.types import OperatorGroup, CustomOperator
from jsonquerylang.utils import find_index

operators: list[OperatorGroup] = [
    {"pow": "^"},
    {"multiply": "*", "divide": "/", "mod": "%"},
    {"add": "+", "subtract": "-"},
    {"gt": ">", "gte": ">=", "lt": "<", "lte": "<=", "in": "in", "not in": "not in"},
    {"eq": "==", "ne": "!="},
    {"and": "and"},
    {"or": "or"},
]


def extend_operators(
    all_operators: list[OperatorGroup], new_operators: list[CustomOperator]
) -> list[OperatorGroup]:
    return reduce(extend_operator, new_operators, all_operators)


def extend_operator(
    all_operators: list[OperatorGroup], custom_operator: CustomOperator
) -> list[OperatorGroup]:
    name = custom_operator["name"]
    op = custom_operator["op"]
    at = custom_operator["at"] if "at" in custom_operator else None
    after = custom_operator["after"] if "after" in custom_operator else None
    before = custom_operator["before"] if "before" in custom_operator else None

    if at:
        callback = lambda group: {**group, name: op} if at in group.values() else group

        return list(map(callback, all_operators))

    search_op = after or before
    index = find_index(lambda group: search_op in group.values(), all_operators)
    if index != -1:
        updated_operators = all_operators.copy()
        new_group: Mapping[str, str] = {name: op}
        updated_operators.insert(index + (1 if after else 0), new_group)

        return updated_operators

    raise RuntimeError("Invalid custom operator")
