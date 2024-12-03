import unittest
import json
import re
from os import path
from jsonquerylang import compile

friends = [
    {"name": "Chris", "age": 23, "scores": [7.2, 5, 8.0]},
    {"name": "Joe", "age": 32, "scores": [6.1, 8.1]},
    {"name": "Emily", "age": 19},
]


class CompileTestCase(unittest.TestCase):
    def test_compile(self):
        """Raise an exception in case of an unknown function"""
        self.assertRaisesRegex(
            SyntaxError, 'Unknown function "foo"', lambda: go([], ["foo"])
        )

    def test_options1(self):
        """Test defining a custom function"""

        def times(value):
            return lambda data: list(map(lambda item: item * value, data))

        query = ["times", 2]

        evaluate = compile(query, {"functions": {"times": times}})

        self.assertEqual(evaluate([2, 3, 4]), [4, 6, 8])
        self.assertEqual(evaluate([-4, 5]), [-8, 10])

    def test_options2(self):
        """Test define options but no custom function"""

        query = ["get", "name"]
        evaluate = compile(query, {})

        self.assertEqual(evaluate({"name": "Joe"}), "Joe")

    def test_options3(self):
        """Test defining a custom function that uses compile"""

        def by_times(data_path, value):
            getter = compile(data_path)

            return lambda data: list(map(lambda item: getter(item) * value, data))

        query = ["by_times", ["get", "score"], 2]
        evaluate = compile(query, {"functions": {"by_times": by_times}})

        self.assertEqual(
            evaluate(
                [
                    {"score": 2},
                    {"score": 4},
                ]
            ),
            [4, 8],
        )

    def test_error_handling1(self):
        """Should throw a helpful error when a pipe contains a compile time error"""

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
            ["filter", ["gte", ["get", "age"], 65]],
            ["map", ["get", "age"]],
            ["average"],
        ]

        self.assertRaisesRegex(
            RuntimeError,
            re.escape("Cannot calculate the average of an empty list"),
            lambda: go(score_data, query),
        )

    def test_error_handling4(self):
        """should throw an error when calculating the sum of an empty array"""

        self.assertRaisesRegex(
            RuntimeError,
            re.escape("Cannot calculate the sum of an empty list"),
            lambda: go([], ["sum"]),
        )

    def test_error_handling5(self):
        """should throw an error when calculating the prod of an empty array"""

        self.assertRaisesRegex(
            RuntimeError,
            re.escape("Cannot calculate the prod of an empty list"),
            lambda: go([], ["prod"]),
        )

    def test_error_handling6(self):
        """should throw an error when calculating the average of an empty array"""

        self.assertRaisesRegex(
            RuntimeError,
            re.escape("Cannot calculate the average of an empty list"),
            lambda: go([], ["average"]),
        )

    def test_suite(self):
        """Run the official compile test-suite"""
        test_suite_file = (
            path.dirname(path.realpath(__file__)) + "/test-suite/compile.test.json"
        )

        with open(test_suite_file, "r") as read_file:
            suite = json.load(read_file)

            for test in suite["tests"]:
                message = f"[{test["category"]}] {test["description"]}"
                with self.subTest(message=message):
                    evaluate = compile(test["query"])
                    self.assertEqual(evaluate(test["input"]), test["output"])


def go(data, query):
    evaluate = compile(query)

    return evaluate(data)


if __name__ == "__main__":
    unittest.main()
