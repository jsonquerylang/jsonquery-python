import unittest
from jsonquery import jsonquery

data = [
    {"name": "Chris", "age": 23, "scores": [7.2, 5, 8.0]},
    {"name": "Joe", "age": 32, "scores": [6.1, 8.1]},
    {"name": "Emily", "age": 19},
]


class JSONQueryTestCase(unittest.TestCase):
    def test_jsonquery(self):
        """Test jsonquery (test and execute)"""
        self.assertEqual(
            jsonquery(data, ["sort", ["get", "name"]]),
            [
                {"name": "Chris", "age": 23, "scores": [7.2, 5, 8.0]},
                {"name": "Emily", "age": 19},
                {"name": "Joe", "age": 32, "scores": [6.1, 8.1]},
            ],
        )

    def test_jsonquery_str1(self):
        """Test jsonquery parsing a query text"""
        self.assertEqual(
            jsonquery(data, "sort(.name)"),
            [
                {"name": "Chris", "age": 23, "scores": [7.2, 5, 8.0]},
                {"name": "Emily", "age": 19},
                {"name": "Joe", "age": 32, "scores": [6.1, 8.1]},
            ],
        )

    def test_jsonquery_str2(self):
        """Test jsonquery parsing a query text with options"""
        options = {"functions": {"times": lambda factor: lambda x: x * factor}}
        self.assertEqual(jsonquery(4, "times(3)", options), 12)

    def test_options1(self):
        """Test defining a custom function"""

        def times(value):
            return lambda array: list(map(lambda item: item * value, array))

        query = ["times", 2]

        self.assertEqual(
            jsonquery([2, 3, 4], query, {"functions": {"times": times}}), [4, 6, 8]
        )


if __name__ == "__main__":
    unittest.main()
