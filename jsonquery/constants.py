import re

built_in_operators = {
    "and": "and",
    "or": "or",
    "eq": "==",
    "gt": ">",
    "gte": ">=",
    "lt": "<",
    "lte": "<=",
    "ne": "!=",
    "add": "+",
    "subtract": "-",
    "multiply": "*",
    "divide": "/",
    "pow": "^",
    "mod": "%",
    "in": "in",
    "not in": "not in",
}

unquoted_property_regex = re.compile(r"^[a-zA-Z_$][a-zA-Z\d_$]*$")
starts_with_unquoted_property_regex = re.compile(r"^[a-zA-Z_$][a-zA-Z\d_$]*")
starts_with_string_regex = re.compile(
    r'^"(?:[^"\\]|\\.)*"'
)  # https://stackoverflow.com/a/249937/1262753
starts_with_number_regex = re.compile(
    r"^-?(?:0|[1-9]\d*)(?:\.\d+)?(?:[eE][+-]?\d+)?"
)  # https://stackoverflow.com/a/13340826/1262753
starts_with_int_regex = re.compile(r"^(0|[1-9][0-9]*)")
starts_with_keyword_regex = re.compile(r"^(true|false|null)")
starts_with_whitespace_regex = re.compile(r"^[ \n\t\r]+")
