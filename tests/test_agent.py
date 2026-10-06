import contextlib
import io
import json
import unittest
from unittest.mock import patch

from agent import TOOLS, calculate, run_turn


class CalculatorTests(unittest.TestCase):
    def test_arithmetic(self):
        for expression, expected in [("(250 * 3) * 0.9", 675), ("-2 ** 2", -4),
                                     ("18 / 100 * 1250", 225), ("7 // 2 + 7 % 2", 4)]:
            with self.subTest(expression=expression):
                self.assertEqual(calculate(expression)["result"], expected)

    def test_invalid_and_unsafe_expressions(self):
        for expression in ["1/0", "__import__('os').getcwd()", "True", "x+1", "2**999999",
                           "1e309", "(-1)**0.5", "2+", "", None, "1" * 201]:
            with self.subTest(expression=expression):
                self.assertIn("error", calculate(expression))


class LoopTests(unittest.TestCase):
    def test_only_one_exposed_tool(self):
        self.assertEqual([t["function"]["name"] for t in TOOLS], ["calculate"])

    def test_greeting_does_not_call_tool(self):
        with patch("agent.calculate") as calculator:
            answer = run_turn([], "test", lambda *_: {"role": "assistant", "content": "Hello!"})
            calculator.assert_not_called()
        self.assertEqual(answer, "Hello!")

    def test_tool_result_is_returned_to_model(self):
        messages = [{"role": "user", "content": "What is 2+3?"}]
        output = io.StringIO()

        def model(history, _):
            if history[-1]["role"] == "tool":
                self.assertEqual(json.loads(history[-1]["content"])["result"], 5)
                return {"role": "assistant", "content": "The answer is 5."}
            return {"role": "assistant", "content": "", "tool_calls": [
                {"function": {"name": "calculate", "arguments": {"expression": "2+3"}}}]}

        original = calculate

        def check_printed(expression):
            self.assertIn("[raw tool call]", output.getvalue())
            return original(expression)

        with contextlib.redirect_stdout(output), patch("agent.calculate", side_effect=check_printed):
            self.assertEqual(run_turn(messages, "test", model), "The answer is 5.")

    def test_bad_arguments_and_unknown_tools_return_errors(self):
        for function in [{"name": "delete", "arguments": {}},
                         {"name": "calculate", "arguments": {"other": 1}},
                         {"name": "calculate", "arguments": "invalid JSON"}]:
            replies = iter([
                {"role": "assistant", "tool_calls": [{"function": function}]},
                {"role": "assistant", "content": "Please clarify."},
            ])
            history = []
            with contextlib.redirect_stdout(io.StringIO()):
                run_turn(history, "test", lambda *_: next(replies))
            self.assertIn("error", json.loads(history[1]["content"]))

    def test_repeated_calls_are_bounded(self):
        reply = {"role": "assistant", "tool_calls": [
            {"function": {"name": "calculate", "arguments": {"expression": "1+1"}}}]}
        with contextlib.redirect_stdout(io.StringIO()), self.assertRaisesRegex(RuntimeError, "5 model rounds"):
            run_turn([], "test", lambda *_: reply)


if __name__ == "__main__":
    unittest.main()
