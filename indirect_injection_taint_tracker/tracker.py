"""Core Indirect Injection Taint Tracker implementation."""
from typing import Dict, List, Set, Optional, Any


class TaintedValue:
    def __init__(self, value: Any, source: str, is_tainted: bool = True):
        self.value = value
        self.source = source
        self.is_tainted = is_tainted

    def __str__(self) -> str:
        return str(self.value)


class TaintTracker:
    def __init__(self, sensitive_tools: Optional[Set[str]] = None):
        self.sensitive_tools = sensitive_tools if sensitive_tools else {"bash", "write_file", "drop_db", "send_email"}
        self.taint_registry: Dict[str, TaintedValue] = {}

    def mark_untrusted(self, identifier: str, raw_data: Any, source_name: str) -> TaintedValue:
        tv = TaintedValue(raw_data, source_name, is_tainted=True)
        self.taint_registry[identifier] = tv
        return tv

    def is_tainted(self, identifier_or_val: Any) -> bool:
        if isinstance(identifier_or_val, TaintedValue):
            return identifier_or_val.is_tainted
        if isinstance(identifier_or_val, str) and identifier_or_val in self.taint_registry:
            return self.taint_registry[identifier_or_val].is_tainted
        return False

    def check_tool_invocation(self, tool_name: str, params: Dict[str, Any]) -> Tuple_Result:
        if tool_name not in self.sensitive_tools:
            return True, "Tool is not in privileged sink list"

        for param_name, param_val in params.items():
            if self.is_tainted(param_val):
                return False, f"Privileged tool '{tool_name}' received tainted parameter '{param_name}' from untrusted source"

        return True, "All parameters clean"


Tuple_Result = Any
