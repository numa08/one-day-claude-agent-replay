import os
import re
import unittest

from agent_replay.parse import parse_file, parse_lines
from agent_replay.render import render_html
from agent_replay.cli import main, format_stats

SAMPLE = os.path.join(os.path.dirname(__file__), "..", "examples", "sample.jsonl")


class T(unittest.TestCase):
    def setUp(self):
        self.p = parse_file(SAMPLE)

    def test_no_double_count(self):
        u = self.p["stats"]["usage"]
        self.assertEqual(u["input"], 1700)
        self.assertEqual(u["output"], 250)

    def test_tool_pairing_and_error(self):
        ev = self.p["events"]
        use = [e for e in ev if e["kind"] == "tool_use"]
        res = {e["id"]: e for e in ev if e["kind"] == "tool_result"}
        self.assertEqual(len(use), 2)
        self.assertTrue(res["t1"]["error"])
        self.assertFalse(res["t2"]["error"])
        self.assertEqual(self.p["stats"]["errors"], 1)
        self.assertEqual(self.p["stats"]["tools"], {"Bash": 1, "Edit": 1})

    def test_bad_lines_skipped(self):
        self.assertEqual(self.p["stats"]["skipped"], 1)
        r = parse_lines(['{"type":"assistant","message":5}', "[]", ""])
        self.assertEqual(r["events"], [])

    def test_cost_positive(self):
        self.assertGreater(self.p["stats"]["cost_usd"], 0)

    def test_html_safe_and_offline(self):
        h = render_html(self.p)
        self.assertEqual(h.count("</script>"), 2)  # data + app only
        self.assertIsNone(re.search(r'(src|href)="https?://', h))

    def test_cli(self):
        import tempfile
        out = os.path.join(tempfile.mkdtemp(), "o.html")
        self.assertEqual(main([SAMPLE, "-o", out]), 0)
        self.assertTrue(os.path.getsize(out) > 1000)
        self.assertIn("tokens:", format_stats(self.p["stats"]))
        self.assertEqual(main(["/nonexistent.jsonl"]), 1)


if __name__ == "__main__":
    unittest.main()
