import sys
import types
import unittest
from unittest.mock import patch


datasets_stub = types.ModuleType("datasets")
datasets_stub.Dataset = object
datasets_stub.load_dataset = lambda *args, **kwargs: None
with patch.dict(sys.modules, {"datasets": datasets_stub}):
    from training.data_prep import escape_terminal_controls


class EscapeTerminalControlsTests(unittest.TestCase):
    def test_escapes_ansi_and_osc_controls(self):
        text = "\x1b[31mred\x1b[0m\x1b]52;c;payload\x07"

        self.assertEqual(
            escape_terminal_controls(text),
            r"\x1b[31mred\x1b[0m\x1b]52;c;payload\x07",
        )

    def test_escapes_control_characters_and_preserves_line_breaks(self):
        self.assertEqual(
            escape_terminal_controls("first\r\nsecond\t\u009b"),
            "first\\x0d\nsecond\\x09\\x9b",
        )


if __name__ == "__main__":
    unittest.main()
