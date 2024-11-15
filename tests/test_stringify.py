import unittest
import json
from os import path

from jsonquery import stringify
from jsonquery.types import JsonQueryStringifyOptions


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
                    message = f"[{group["category"]}] {group["description"]} (input: {test["input"]})"
                    with self.subTest(message=message):
                        self.assertEqual(
                            stringify(test["input"], options), test["output"]
                        )


if __name__ == "__main__":
    unittest.main()


def to_stringify_options(javascript_options) -> JsonQueryStringifyOptions:
    return {
        "operators": javascript_options.get("operators", None),
        "max_line_length": javascript_options.get("maxLineLength", None),
        "indentation": javascript_options.get("indentation", None),
    }
