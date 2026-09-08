"""CLI: python -m spec_refuse <check|conformance|benchmark> [SPEC]"""

from __future__ import annotations

import json
import sys
from pathlib import Path

from spec_refuse.benchmark import run_benchmark
from spec_refuse.check import check_specification
from spec_refuse.conformance import conformance_report

_USAGE = "usage: python -m spec_refuse <check|conformance|benchmark> [SPEC.md]"


def _print(obj: object) -> None:
    sys.stdout.write(json.dumps(obj, indent=2, ensure_ascii=False))
    sys.stdout.write("\n")
    sys.stdout.flush()


def main(argv: list[str] | None = None) -> int:
    args = list(sys.argv[1:] if argv is None else argv)
    if not args:
        sys.stdout.write("REFUSED: no command. " + _USAGE + "\n")
        return 2
    cmd = args[0]
    spec = Path(args[1]) if len(args) > 1 else Path("SPEC.md")
    if cmd == "check":
        code, payload = check_specification(spec)
        sys.stdout.write(f"{payload['verdict']}: {payload.get('reason', '')}\n")
        _print(payload)
        return code
    if cmd == "conformance":
        report = conformance_report(spec)
        sys.stdout.write(f"{report['verdict']}: conformance\n")
        _print(report)
        return int(report["exit"])
    if cmd == "benchmark":
        code, table = run_benchmark(spec)
        sys.stdout.write(f"{table['verdict']}: {table.get('reason', '')}\n")
        _print(table)
        return code
    sys.stdout.write(f"REFUSED: unknown command {cmd!r}. {_USAGE}\n")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
