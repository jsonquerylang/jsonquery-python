from functools import reduce
from math import prod
import re


def get_functions(compile):
    def build_function(fn):
        def evaluate_fn(*args):
            compiled_args = list(map(compile, args))

            return lambda data: fn(
                *list(map(lambda compiled_arg: compiled_arg(data), compiled_args))
            )

        return evaluate_fn

    def fn_get(*path: []):
        def getter(item):
            value = item

            for p in path:
                value_exists = value is not None and (
                    p < len(value) if type(value) is list else p in value
                )
                value = value[p] if value_exists else None

            return value

        return getter

    def fn_pick(*properties):
        getters = {}
        for prop in properties:
            _, *path = prop
            name = path[-1]
            getters[name] = fn_get(*path)

        def pick(object):
            out = {}
            for key, getter in getters.items():
                out[key] = getter(object)
            return out

        return lambda data: list(map(pick, data)) if type(data) is list else pick(data)

    def fn_object(query):
        getters = {}
        for key, value in query.items():
            getters[key] = compile(value)

        def evaluate_object(data):
            obj = {}
            for obj_key, getter in getters.items():
                obj[obj_key] = getter(data)

            return obj

        return evaluate_object

    def fn_array(*items):
        getters = map(compile, items)

        return lambda data: list(map(lambda getter: getter(data), getters))

    def fn_filter(predicate):
        _predicate = compile(predicate)

        return lambda data: list(filter(lambda item: truthy(_predicate(item)), data))

    def fn_map(callback):
        _callback = compile(callback)

        return lambda data: list(map(_callback, data))

    def fn_map_object(callback):
        _callback = compile(callback)

        def map_object(data):
            object = {}

            for key, value in data.items():
                res = _callback({"key": key, "value": value})
                object[res["key"]] = res["value"]

            return object

        return map_object

    def fn_map_keys(callback):
        _callback = compile(callback)

        return lambda data: {_callback(key): value for key, value in data.items()}

    def fn_map_values(callback):
        _callback = compile(callback)

        return lambda data: {key: _callback(value) for key, value in data.items()}

    def fn_pipe(*entries):
        getters = map(compile, entries)

        return lambda data: reduce(lambda value, getter: getter(value), getters, data)

    def fn_sort(path=None, direction="asc"):
        getter = compile(path) if path is not None else lambda item: item

        return lambda data: sorted(data, key=getter, reverse=direction == "desc")

    def fn_reverse():
        return lambda data: list(reversed(data))

    def fn_group_by(path):
        getter = compile(path)

        def group_by(data):
            res = {}

            for item in data:
                value = format(getter(item))
                if value in res:
                    res[value].append(item)
                else:
                    res[value] = [item]

            return res

        return group_by

    def fn_key_by(path):
        getter = compile(path)

        def key_by(data):
            res = {}

            for item in data:
                value = format(getter(item))
                if value not in res:
                    res[value] = item

            return res

        return key_by

    fn_flatten = lambda: lambda data: [x for xs in data for x in xs]
    fn_join = lambda separator="": lambda data: separator.join(data)
    fn_split = build_function(
        lambda text, separator=None: (
            text.split(separator) if separator is not "" else split_chars(text)
        )
    )
    fn_substring = build_function(
        lambda text, start, end=None: text[max(start, 0) : end]
    )
    fn_uniq = lambda: lambda data: list(dict.fromkeys(data))
    fn_uniq_by = lambda path: lambda data: list(fn_key_by(path)(data).values())
    fn_limit = lambda count: lambda data: data[0:count] if count >= 0 else []
    fn_size = lambda: lambda data: len(data)
    fn_keys = lambda: lambda data: list(data.keys())
    fn_values = lambda: lambda data: list(data.values())
    fn_prod = lambda: lambda data: prod(data)
    fn_sum = lambda: lambda data: sum(data)
    fn_average = lambda: lambda data: sum(data) / len(data)
    fn_min = lambda: lambda data: min(data)
    fn_max = lambda: lambda data: max(data)

    fn_and = build_function(lambda a, b: a and b)
    fn_or = build_function(lambda a, b: a or b)
    fn_not = build_function(lambda a: not a)

    def fn_exists(query_get):
        _, *path = query_get

        def exec_exists(data):
            value = data

            for key in path:
                if value is None or key not in value:
                    return False
                value = value[key]

            return True

        return exec_exists

    def fn_if(condition, value_if_true, value_if_false):
        _condition = compile(condition)
        _value_if_true = compile(value_if_true)
        _value_if_false = compile(value_if_false)

        return (
            lambda data: _value_if_true(data)
            if truthy(_condition(data))
            else _value_if_false(data)
        )

    def fn_in(path, in_values):
        getter = compile(path)
        _values = map(compile, in_values)

        return lambda data: getter(data) in map(lambda _value: _value(data), _values)

    def fn_not_in(path, not_in_values):
        getter = compile(path)
        _values = map(compile, not_in_values)

        return lambda data: getter(data) not in map(
            lambda _value: _value(data), _values
        )

    def fn_regex(path, expression, options=None):
        regex = (
            re.compile(expression, flags=_parse_regex_flags(options))
            if options
            else re.compile(expression)
        )
        getter = compile(path)

        return lambda value: regex.match(getter(value)) is not None

    fn_eq = build_function(lambda a, b: a == b)
    fn_gt = build_function(lambda a, b: a > b)
    fn_gte = build_function(lambda a, b: a >= b)
    fn_lt = build_function(lambda a, b: a < b)
    fn_lte = build_function(lambda a, b: a <= b)
    fn_ne = build_function(lambda a, b: a != b)

    fn_add = build_function(
        lambda a, b: to_string(a) + to_string(b)
        if type(a) is str or type(b) is str
        else a + b
    )
    fn_subtract = build_function(lambda a, b: a - b)
    fn_multiply = build_function(lambda a, b: a * b)
    fn_divide = build_function(lambda a, b: a / b)
    fn_pow = build_function(pow)
    fn_mod = build_function(lambda a, b: a % b)
    fn_abs = build_function(abs)
    fn_round = build_function(lambda value, digits=0: round(value, digits))
    fn_string = build_function(to_string)
    fn_number = build_function(to_number)

    return {
        "get": fn_get,
        "pick": fn_pick,
        "object": fn_object,
        "array": fn_array,
        "filter": fn_filter,
        "map": fn_map,
        "mapObject": fn_map_object,
        "mapKeys": fn_map_keys,
        "mapValues": fn_map_values,
        "pipe": fn_pipe,
        "sort": fn_sort,
        "reverse": fn_reverse,
        "groupBy": fn_group_by,
        "keyBy": fn_key_by,
        "flatten": fn_flatten,
        "join": fn_join,
        "split": fn_split,
        "substring": fn_substring,
        "uniq": fn_uniq,
        "uniqBy": fn_uniq_by,
        "limit": fn_limit,
        "size": fn_size,
        "keys": fn_keys,
        "values": fn_values,
        "prod": fn_prod,
        "sum": fn_sum,
        "average": fn_average,
        "min": fn_min,
        "max": fn_max,
        "and": fn_and,
        "or": fn_or,
        "not": fn_not,
        "exists": fn_exists,
        "if": fn_if,
        "in": fn_in,
        "not in": fn_not_in,
        "regex": fn_regex,
        "eq": fn_eq,
        "gt": fn_gt,
        "gte": fn_gte,
        "lt": fn_lt,
        "lte": fn_lte,
        "ne": fn_ne,
        "add": fn_add,
        "subtract": fn_subtract,
        "multiply": fn_multiply,
        "divide": fn_divide,
        "pow": fn_pow,
        "mod": fn_mod,
        "abs": fn_abs,
        "round": fn_round,
        "string": fn_string,
        "number": fn_number,
    }


def _parse_regex_flags(flags):
    if flags is None or len(flags) == 0:
        return None

    all_flags = {
        "A": re.A,
        "I": re.I,
        "M": re.M,
        "S": re.S,
        "X": re.X,
        "L": re.L,
    }

    first, *rest = flags.upper()

    return reduce(
        lambda combined, flag: combined | all_flags[flag], rest, all_flags[first]
    )


def truthy(value):
    return value not in [False, 0, None]


def to_string(value):
    return (
        "false"
        if value is False
        else "true"
        if value is True
        else "null"
        if value is None
        else format(value)
    )


def to_number(value):
    try:
        return float(value)
    except ValueError:
        return None


def split_chars(text):
    (*chars,) = text
    return chars
