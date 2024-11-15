import unittest
import json
import re
from os import path

from jsonquery import parse


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
                    message = f"[{group["category"]}] {group["description"]} (input: {test["input"]})"

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


if __name__ == "__main__":
    unittest.main()
