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


if __name__ == "__main__":
    unittest.main()
