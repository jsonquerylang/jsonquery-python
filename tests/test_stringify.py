import unittest
import json
from os import path

from jsonquerylang import stringify
from jsonquerylang.types import JsonQueryStringifyOptions


class StringifyTestCase(unittest.TestCase):
    def test_suite(self):
        """Run the official stringify test-suite"""
        test_suite_file = (
            path.dirname(path.realpath(__file__)) + "/test-suite/stringify.test.json"
        )

        with open(test_suite_file, "r") as read_file:
            suite = json.load(read_file)

            for group in suite["groups"]:
                options = (
                    to_stringify_options(group["options"])
                    if "options" in group
                    else None
                )

                for test in group["tests"]:
                    message = f"[{group['category']}] {group['description']} (input: {test['input']})"
                    with self.subTest(message=message):
                        self.assertEqual(
                            stringify(test["input"], options), test["output"]
                        )

    def test_options1(self):
        """should stringify a custom operator"""
        options: JsonQueryStringifyOptions = {
            "operators": [{"name": "aboutEq", "op": "~=", "at": "=="}]
        }

        self.assertEqual(stringify(["aboutEq", 2, 3], options), "2 ~= 3")
        self.assertEqual(
            stringify(["filter", ["aboutEq", 2, 3]], options), "filter(2 ~= 3)"
        )
        self.assertEqual(
            stringify(["object", {"result": ["aboutEq", 2, 3]}], options),
            "{ result: 2 ~= 3 }",
        )

        # existing operators should still be there
        self.assertEqual(stringify(["eq", 2, 3], options), "2 == 3")

        # precedence and parenthesis
        self.assertEqual(
            stringify(["aboutEq", ["aboutEq", 2, 3], 4], options), "(2 ~= 3) ~= 4"
        )
        self.assertEqual(
            stringify(["aboutEq", 2, ["aboutEq", 3, 4]], options), "2 ~= (3 ~= 4)"
        )
        self.assertEqual(
            stringify(["aboutEq", ["and", 2, 3], 4], options), "(2 and 3) ~= 4"
        )
        self.assertEqual(
            stringify(["aboutEq", 2, ["and", 3, 4]], options), "2 ~= (3 and 4)"
        )
        self.assertEqual(
            stringify(["and", ["aboutEq", 2, 3], 4], options), "2 ~= 3 and 4"
        )
        self.assertEqual(
            stringify(["and", 2, ["aboutEq", 3, 4]], options), "2 and 3 ~= 4"
        )
        self.assertEqual(
            stringify(["aboutEq", ["add", 2, 3], 4], options), "2 + 3 ~= 4"
        )
        self.assertEqual(
            stringify(["aboutEq", 2, ["add", 3, 4]], options), "2 ~= 3 + 4"
        )
        self.assertEqual(
            stringify(["add", ["aboutEq", 2, 3], 4], options), "(2 ~= 3) + 4"
        )
        self.assertEqual(
            stringify(["add", 2, ["aboutEq", 3, 4]], options), "2 + (3 ~= 4)"
        )

    def test_options2(self):
        """should stringify left associative custom operator"""
        options: JsonQueryStringifyOptions = {
            "operators": [
                {"name": "aboutEq", "op": "~=", "at": "==", "left_associative": True}
            ]
        }

        self.assertEqual(
            stringify(["aboutEq", ["aboutEq", 2, 3], 4], options), "2 ~= 3 ~= 4"
        )
        self.assertEqual(
            stringify(["aboutEq", 2, ["aboutEq", 3, 4]], options), "2 ~= (3 ~= 4)"
        )

    # Note: we do not test the option `CustomOperator.vararg`
    # since they have no effect on stringification, only on parsing.


if __name__ == "__main__":
    unittest.main()


def to_stringify_options(javascript_options) -> JsonQueryStringifyOptions:
    return {
        "operators": javascript_options.get("operators", None),
        "max_line_length": javascript_options.get("maxLineLength", None),
        "indentation": javascript_options.get("indentation", None),
    }
