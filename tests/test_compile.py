import unittest
import json
import re
from os import path
from jsonquerylang import compile
from jsonquerylang.compile import build_function

friends = [
    {"name": "Chris", "age": 23, "scores": [7.2, 5, 8.0]},
    {"name": "Joe", "age": 32, "scores": [6.1, 8.1]},
    {"name": "Emily", "age": 19},
]


class CompileTestCase(unittest.TestCase):
    def test_unknown_function(self):
        """Raise an exception in case of an unknown function"""
        self.assertRaisesRegex(
            SyntaxError, 'Unknown function "foo"', lambda: go([], ["foo"])
        )

    def test_pass_empty_options(self):
        """Test define empty options object"""

        query = ["get", "name"]
        evaluate = compile(query, {})

        self.assertEqual(evaluate({"name": "Joe"}), "Joe")

    def test_options1(self):
        """should define a custom function"""
        options = {
            "functions": {
                "times": lambda value: lambda data: [item * value for item in data]
            }
        }

        self.assertEqual(go([1, 2, 3], ["times", 2], options), [2, 4, 6])
        with self.assertRaises(Exception) as context:
            go([1, 2, 3], ["times", 2])
        self.assertIn('Unknown function "times"', str(context.exception))

    def test_options2(self):
        """should extend with a custom function with more than 2 arguments"""

        def one_of(value, a, b, c):
            return value == a or value == b or value == c

        options = {"functions": {"oneOf": build_function(one_of)}}

        self.assertTrue(go("C", ["oneOf", ["get"], "A", "B", "C"], options))
        self.assertFalse(go("D", ["oneOf", ["get"], "A", "B", "C"], options))

    def test_options3(self):
        """should override an existing function"""
        options = {"functions": {"sort": lambda: lambda _data: "custom sort"}}

        self.assertEqual(go([2, 3, 1], ["sort"], options), "custom sort")

    def test_options4(self):
        """should be able to insert a function in a nested compile"""

        def times(value):
            _options = {"functions": {"foo": lambda: lambda _data: 42}}
            _value = compile(value, _options)
            return lambda data: [item * _value(data) for item in data]

        options = {"functions": {"times": times}}

        self.assertEqual(go([1, 2, 3], ["times", 2], options), [2, 4, 6])
        self.assertEqual(go([1, 2, 3], ["times", ["foo"]], options), [42, 84, 126])

        with self.assertRaises(Exception) as context:
            go([1, 2, 3], ["foo"], options)
        self.assertIn('Unknown function "foo"', str(context.exception))

    def test_options6(self):
        """should clean up the custom function stack when creating a query throws an error"""
        options = {
            "functions": {
                "sort": lambda: (_ for _ in ()).throw(Exception("Test Error"))
            }
        }

        with self.assertRaises(Exception) as context:
            go({}, ["sort"], options)
        self.assertEqual(str(context.exception), "Test Error")

        # Should fall back to default behavior
        self.assertEqual(go([2, 3, 1], ["sort"]), [1, 2, 3])

    def test_options7(self):
        """should extend with a custom function aboutEq"""

        def about_eq(a, b):
            epsilon = 0.001
            return abs(a - b) < epsilon

        options = {"functions": {"aboutEq": build_function(about_eq)}}

        self.assertTrue(go({"a": 2}, ["aboutEq", ["get", "a"], 2], options))
        self.assertTrue(go({"a": 1.999}, ["aboutEq", ["get", "a"], 2], options))

    def test_error_handling1(self):
        """should throw a helpful error when a pipe contains a compile time error"""

        query = ["foo", 42]

        self.assertRaisesRegex(
            SyntaxError,
            'Unknown function "foo"',
            lambda: compile(query),
        )

    def test_error_handling2(self):
        """should throw a helpful error when passing an object {...} instead of function ["object", {...}]"""

        user = {"name": "Joe"}
        query = {"name": ["get", "name"]}

        self.assertRaisesRegex(
            SyntaxError,
            re.escape(
                'Function notation ["object", {...}] expected but got {"name": ["get", "name"]}'
            ),
            lambda: go(user, query),
        )

    def test_error_handling3(self):
        """should throw a helpful error when a pipe contains a runtime error"""

        score_data = {
            "participants": [
                {"name": "Chris", "age": 23, "scores": [7.2, 5, 8.0]},
                {"name": "Emily", "age": 19},
                {"name": "Joe", "age": 32, "scores": [6.1, 8.1]},
            ]
        }
        query = [
            "pipe",
            ["get", "participants"],
            ["map", ["pipe", ["get", "scores"], ["sum"]]],
        ]

        self.assertRaisesRegex(
            RuntimeError,
            re.escape("Array expected"),
            lambda: print(go(score_data, query)),
        )

    def test_suite(self):
        """Run the official compile test-suite"""
        test_suite_file = (
            path.dirname(path.realpath(__file__)) + "/test-suite/compile.test.json"
        )

        with open(test_suite_file, "r") as read_file:
            suite = json.load(read_file)

            for group in suite["groups"]:
                for test in group["tests"]:
                    message = f"[{group['category']}] {group['description']} (input: {test['input']})"

                    evaluate = compile(test["query"])

                    if "output" in test:
                        with self.subTest(message=message):
                            self.assertEqual(evaluate(test["input"]), test["output"])
                    else:
                        with self.subTest(message=message):
                            self.assertRaisesRegex(
                                RuntimeError,
                                re.escape(test["throws"]),
                                lambda: print(evaluate(test["input"])),
                            )


def go(data, query, options=None):
    evaluate = compile(query, options)

    return evaluate(data)


if __name__ == "__main__":
    unittest.main()
