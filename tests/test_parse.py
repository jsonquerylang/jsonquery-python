import unittest
import json
import re
from os import path

from jsonquerylang import parse, JsonQueryParseOptions


class ParseTestCase(unittest.TestCase):
    def test_suite(self):
        """Run the official parse test-suite"""
        test_suite_file = (
            path.dirname(path.realpath(__file__)) + "/test-suite/parse.test.json"
        )

        with open(test_suite_file, "r") as read_file:
            suite = json.load(read_file)

            for group in suite["groups"]:
                for test in group["tests"]:
                    message = f"[{group['category']}] {group['description']} (input: {test['input']})"

                    if "output" in test:
                        with self.subTest(message=message):
                            self.assertEqual(parse(test["input"]), test["output"])
                    else:
                        with self.subTest(message=message):
                            self.assertRaisesRegex(
                                SyntaxError,
                                re.escape(test["throws"]),
                                lambda: parse(test["input"]),
                            )

    def test_options1(self):
        """should parse a custom function"""

        options: JsonQueryParseOptions = {"functions": {"customFn": lambda: lambda: 42}}

        self.assertEqual(
            parse('customFn(.age, "desc")', options),
            ["customFn", ["get", "age"], "desc"],
        )

        # built-in functions should still be available
        self.assertEqual(parse("add(2, 3)", options), ["add", 2, 3])

    def test_options2(self):
        """should parse a custom operator without vararg"""

        options: JsonQueryParseOptions = {
            "operators": [{"name": "aboutEq", "op": "~=", "at": "=="}]
        }

        self.assertEqual(
            parse(".score ~= 8", options), ["aboutEq", ["get", "score"], 8]
        )

        # built-in operators should still be available
        self.assertEqual(parse(".score == 8", options), ["eq", ["get", "score"], 8])

        self.assertRaisesRegex(
            SyntaxError,
            re.escape("Unexpected part '~= 4'"),
            lambda: parse("2 ~= 3 ~= 4", options),
        )

    def test_options3(self):
        """should parse a custom operator with vararg without left_associative"""

        options: JsonQueryParseOptions = {
            "operators": [{"name": "aboutEq", "op": "~=", "at": "==", "vararg": True}]
        }

        self.assertEqual(parse("2 and 3 and 4", options), ["and", 2, 3, 4])
        self.assertEqual(parse("2 ~= 3", options), ["aboutEq", 2, 3])
        self.assertEqual(parse("2 ~= 3 and 4", options), ["and", ["aboutEq", 2, 3], 4])
        self.assertEqual(parse("2 and 3 ~= 4", options), ["and", 2, ["aboutEq", 3, 4]])
        self.assertEqual(parse("2 == 3 ~= 4", options), ["aboutEq", ["eq", 2, 3], 4])
        self.assertEqual(parse("2 ~= 3 == 4", options), ["eq", ["aboutEq", 2, 3], 4])
        self.assertRaisesRegex(
            SyntaxError,
            re.escape("Unexpected part '~= 4'"),
            lambda: parse("2 ~= 3 ~= 4", options),
        )
        self.assertRaisesRegex(
            SyntaxError,
            re.escape("Unexpected part '== 4'"),
            lambda: parse("2 == 3 == 4", options),
        )

    def test_options4(self):
        """should parse a custom operator with vararg without left_associative"""

        options: JsonQueryParseOptions = {
            "operators": [
                {
                    "name": "aboutEq",
                    "op": "~=",
                    "at": "==",
                    "vararg": True,
                    "left_associative": True,
                }
            ]
        }

        self.assertEqual(parse("2 and 3 and 4", options), ["and", 2, 3, 4])
        self.assertEqual(parse("2 ~= 3", options), ["aboutEq", 2, 3])
        self.assertEqual(parse("2 ~= 3 ~= 4", options), ["aboutEq", 2, 3, 4])
        self.assertRaisesRegex(
            SyntaxError,
            re.escape("Unexpected part '== 4'"),
            lambda: parse("2 == 3 == 4", options),
        )

    def test_options5(self):
        """should throw an error in case of an invalid custom operator"""

        options: JsonQueryParseOptions = {"operators": [dict()]}

        self.assertRaisesRegex(
            RuntimeError,
            re.escape("Invalid custom operator"),
            lambda: parse(".score > 8", options),
        )

    def test_options6(self):
        """should throw an error in case of an invalid custom operator (2)"""

        options: JsonQueryParseOptions = {"operators": dict()}

        self.assertRaisesRegex(
            RuntimeError,
            re.escape("Invalid custom operators"),
            lambda: parse(".score > 8", options),
        )


if __name__ == "__main__":
    unittest.main()
