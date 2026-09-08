"""Benchmark runner. Refuses when no algorithm is named."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from spec_refuse.check import EXIT_REFUSE, check_specification


def run_benchmark(path: str | Path) -> tuple[int, dict[str, Any]]:
    code, payload = check_specification(path)
    table: dict[str, Any] = {
        "verdict": "REFUSED",
        "exit": EXIT_REFUSE,
        "reason_code": "NO_ALGORITHM_NAMED",
        "reason": (
            "no algorithm, input family, or size sequence was named; "
            "a fabricated timing table would be a pass invented from silence"
        ),
        "rows": [],
        "scaling_ratios": [],
        "complexity_estimate": "UNIDENTIFIED",
        "spec_check_exit": code,
        "spec_reason_code": payload.get("reason_code"),
    }
    return EXIT_REFUSE, table
