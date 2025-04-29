import unittest
from jsonquerylang.operators import extend_operators


class CompileTestCase(unittest.TestCase):
    def test_custom_operator_at(self):
        """Test defining a custom operator at a given precedence"""

        ops = [{"add": "+", "subtract": "-"}, {"eq": "=="}]

        self.assertEqual(
            extend_operators(ops, [{"name": "aboutEq", "op": "~=", "at": "=="}]),
            [{"add": "+", "subtract": "-"}, {"eq": "==", "aboutEq": "~="}],
        )

    def test_custom_operator_after(self):
        """Test defining a custom operator after a given precedence"""

        ops = [{"add": "+", "subtract": "-"}, {"eq": "=="}]

        self.assertEqual(
            extend_operators(ops, [{"name": "aboutEq", "op": "~=", "after": "+"}]),
            [{"add": "+", "subtract": "-"}, {"aboutEq": "~="}, {"eq": "=="}],
        )

    def test_custom_operator_before(self):
        """Test defining a custom operator before a given precedence"""

        ops = [{"add": "+", "subtract": "-"}, {"eq": "=="}]

        self.assertEqual(
            extend_operators(ops, [{"name": "aboutEq", "op": "~=", "before": "=="}]),
            [{"add": "+", "subtract": "-"}, {"aboutEq": "~="}, {"eq": "=="}],
        )

    def test_multiple_custom_operators(self):
        """Test defining multiple custom operators"""

        ops = [{"add": "+", "subtract": "-"}, {"eq": "=="}]

        self.assertEqual(
            extend_operators(
                ops,
                [
                    {"name": "first", "op": "op1", "before": "=="},
                    {"name": "second", "op": "op2", "before": "op1"},
                ],
            ),
            [
                {"add": "+", "subtract": "-"},
                {"second": "op2"},
                {"first": "op1"},
                {"eq": "=="},
            ],
        )
