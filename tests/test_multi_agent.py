import contextlib
import io
import json
import tempfile
import unittest
from datetime import datetime
from pathlib import Path
from unittest.mock import patch

import multi_agent as app


def tool_call(name, arguments):
    return {"function": {"name": name, "arguments": arguments}}


class MultiToolTests(unittest.TestCase):
    def test_three_tools_and_dispatch(self):
        self.assertEqual(set(app.FUNCTIONS), {"calculate", "notes", "current_time"})
        name, result = app.dispatch(tool_call("calculate", {"expression": "3 * 250"}))
        self.assertEqual((name, result["result"]), ("calculate", 750))

    def test_bad_calls_become_errors(self):
        bad_calls = [None, [], {}, {"function": None},
                     tool_call([], {}), tool_call("missing", {}),
                     tool_call("calculate", {}), tool_call("calculate", {"expression": 8}),
                     tool_call("notes", {"action": "delete"}),
                     tool_call("notes", {"action": "save", "text": ""}),
                     tool_call("notes", {"action": "list", "path": "elsewhere"}),
                     tool_call("current_time", {"utc_offset_minutes": True}),
                     tool_call("current_time", {"utc_offset_minutes": 9999}),
                     tool_call("notes", "not JSON"), tool_call("notes", "[]")]
        for call in bad_calls:
            with self.subTest(call=call):
                self.assertIn("error", app.dispatch(call)[1])

    def test_json_string_arguments(self):
        self.assertEqual(app.dispatch(tool_call("calculate", '{"expression":"2+3"}'))[1]["result"], 5)

    def test_notes_persist_and_duplicate_is_not_added(self):
        with tempfile.TemporaryDirectory() as folder, patch.object(app, "NOTES_FILE", Path(folder) / "notes.json"):
            self.assertEqual(app.notes("list"), {"notes": []})
            self.assertEqual(app.notes("save", "learn Python")["status"], "saved")
            self.assertEqual(app.notes("save", "learn Python")["status"], "already saved")
            self.assertEqual(json.loads(app.NOTES_FILE.read_text()), ["learn Python"])
            self.assertEqual(app.notes("list"), {"notes": ["learn Python"]})

    def test_invalid_file_is_not_overwritten(self):
        with tempfile.TemporaryDirectory() as folder, patch.object(app, "NOTES_FILE", Path(folder) / "notes.json"):
            app.NOTES_FILE.write_text("broken JSON")
            self.assertIn("error", app.notes("save", "new"))
            self.assertEqual(app.NOTES_FILE.read_text(), "broken JSON")

    def test_file_error_is_observation(self):
        with patch.object(Path, "exists", side_effect=PermissionError("denied")):
            self.assertIn("error", app.notes("list"))

    def test_time_offset(self):
        result = app.current_time()
        parsed = datetime.fromisoformat(result["india"])
        self.assertEqual(parsed.utcoffset().total_seconds(), 330 * 60)
        self.assertEqual(parsed, datetime.fromisoformat(result["utc"]))

    def test_memory_survives_intervening_turn(self):
        history = [{"role": "system", "content": app.SYSTEM}, {"role": "user", "content": "250 * 3?"}]
        replies = iter([
            {"role": "assistant", "tool_calls": [tool_call("calculate", {"expression": "250*3"})]},
            {"role": "assistant", "content": "750"},
            {"role": "assistant", "content": "You are welcome!"},
        ])
        with contextlib.redirect_stdout(io.StringIO()):
            app.run_turn(history, "test", lambda *_: next(replies))
            history.append({"role": "user", "content": "Thanks"})
            app.run_turn(history, "test", lambda *_: next(replies))
            history.append({"role": "user", "content": "Add 50 to that result"})

            def model(messages, _):
                self.assertTrue(any(m.get("role") == "tool" and json.loads(m["content"]).get("result") == 750 for m in messages))
                return {"role": "assistant", "content": "Earlier result is in context."}

            app.run_turn(history, "test", model)

    def test_greeting_has_no_side_effect_when_model_answers_directly(self):
        history = []
        with patch.object(app, "dispatch") as dispatch:
            app.run_turn(history, "test", lambda *_: {"role": "assistant", "content": "Hi!"})
            dispatch.assert_not_called()

    def test_observation_preserved_after_network_failure(self):
        history = []
        replies = iter([{ "role": "assistant", "tool_calls": [tool_call("calculate", {"expression": "2+3"})]}])

        def model(*_):
            try:
                return next(replies)
            except StopIteration:
                raise RuntimeError("Network unavailable")

        with contextlib.redirect_stdout(io.StringIO()), self.assertRaises(RuntimeError):
            app.run_turn(history, "test", model)
        self.assertEqual(json.loads(history[-1]["content"])["result"], 5)

    def test_loop_limit(self):
        reply = {"role": "assistant", "tool_calls": [tool_call("calculate", {"expression": "1+1"})]}
        with contextlib.redirect_stdout(io.StringIO()), self.assertRaisesRegex(RuntimeError, "6 model rounds"):
            app.run_turn([], "test", lambda *_: reply)


if __name__ == "__main__":
    unittest.main()
