import unittest
from jsonquery import compile

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

    def test_get1(self):
        """Get a property"""
        self.assertEqual(go({"name": "Chris"}, ["get", "name"]), "Chris")

    def test_get2(self):
        """Get a nested property"""
        self.assertEqual(
            go({"address": {"city": "Rotterdam"}}, ["get", "address", "city"]),
            "Rotterdam",
        )

    def test_sort1(self):
        """Test sort array by name (asc)"""
        self.assertEqual(
            go(friends, ["sort", ["get", "name"]]),
            [
                {"name": "Chris", "age": 23, "scores": [7.2, 5, 8.0]},
                {"name": "Emily", "age": 19},
                {"name": "Joe", "age": 32, "scores": [6.1, 8.1]},
            ],
        )

    def test_sort2(self):
        """Test sort array by age (asc)"""
        self.assertEqual(
            go(friends, ["sort", ["get", "age"]]),
            [
                {"name": "Emily", "age": 19},
                {"name": "Chris", "age": 23, "scores": [7.2, 5, 8.0]},
                {"name": "Joe", "age": 32, "scores": [6.1, 8.1]},
            ],
        )

    def test_sort3(self):
        """Test sort array (desc)"""
        self.assertEqual(
            go(friends, ["sort", ["get", "name"], "desc"]),
            [
                {"name": "Joe", "age": 32, "scores": [6.1, 8.1]},
                {"name": "Emily", "age": 19},
                {"name": "Chris", "age": 23, "scores": [7.2, 5, 8.0]},
            ],
        )

    def test_sort4(self):
        """Test sort array with numbers"""
        self.assertEqual(
            go([32, 19, 23], ["sort"]),
            [19, 23, 32],
        )


def go(data, query):
    evaluate = compile(query)

    return evaluate(data)


if __name__ == "__main__":
    unittest.main()
