"""Unit tests for indirect-injection-taint-tracker."""
import unittest
from indirect_injection_taint_tracker.tracker import TaintTracker


class TestTaintTracker(unittest.TestCase):
    def setUp(self):
        self.tracker = TaintTracker()

    def test_clean_parameters(self):
        ok, msg = self.tracker.check_tool_invocation("bash", {"cmd": "ls"})
        self.assertTrue(ok)

    def test_tainted_parameter_blocked(self):
        tainted = self.tracker.mark_untrusted("doc", "payload", "web")
        ok, msg = self.tracker.check_tool_invocation("write_file", {"content": tainted})
        self.assertFalse(ok)
        self.assertIn("tainted", msg)
