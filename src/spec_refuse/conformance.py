"""Conformance report. Counts the specification requires, fail-closed."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from spec_refuse.check import EXIT_REFUSE, check_specification


def conformance_report(path: str | Path) -> dict[str, Any]:
    code, payload = check_specification(path)
    named = int(payload.get("acceptance_named", 0))
    report: dict[str, Any] = {
        "verdict": payload["verdict"],
        "exit": code,
        "reason_code": payload.get("reason_code"),
        "reason": payload.get("reason"),
        "acceptance_named": named,
        "acceptance_pass": 0,
        "acceptance_fail": 0,
        "acceptance_not_implemented": 0,
        "checks_run": 1,
        "checks_pass": 0,
        "checks_fail": 0,
        "checks_refuse": 1 if code == EXIT_REFUSE else 0,
        "ambiguities": payload.get("ambiguities", []),
        "spec_path": str(path),
    }
    return report
