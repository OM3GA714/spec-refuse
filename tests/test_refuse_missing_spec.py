"""Acceptance tests for a missing or empty product specification.

These tests exist before the implementation. A missing specification must
REFUSE (exit 2). It must never pass (exit 0). Silence is not agreement.
"""

from __future__ import annotations

import json
import os
import tempfile
import unittest
from pathlib import Path


class TestRefuseMissingSpecification(unittest.TestCase):
    def test_A001_missing_spec_file_exits_2(self) -> None:
        from spec_refuse.check import check_specification

        missing = Path(tempfile.gettempdir()) / "spec-refuse-no-such-spec.md"
        if missing.exists():
            missing.unlink()
        code, payload = check_specification(missing)
        self.assertEqual(code, 2, "missing spec must REFUSE, not pass or fail")
        self.assertEqual(payload["verdict"], "REFUSED")

    def test_A002_empty_spec_file_exits_2(self) -> None:
        from spec_refuse.check import check_specification

        with tempfile.TemporaryDirectory() as td:
            path = Path(td) / "SPEC.md"
            path.write_text("", encoding="utf-8")
            code, payload = check_specification(path)
        self.assertEqual(code, 2, "empty spec body must REFUSE")
        self.assertEqual(payload["verdict"], "REFUSED")
        self.assertEqual(payload["reason_code"], "EMPTY_SPEC")

    def test_A003_divider_only_spec_exits_2(self) -> None:
        from spec_refuse.check import check_specification

        text = (
            "You are building a standalone open-source Python library.\n"
            "The specification follows.\n"
            "---\n"
        )
        with tempfile.TemporaryDirectory() as td:
            path = Path(td) / "SPEC.md"
            path.write_text(text, encoding="utf-8")
            code, payload = check_specification(path)
        self.assertEqual(code, 2)
        self.assertEqual(payload["verdict"], "REFUSED")
        self.assertEqual(payload["reason_code"], "NO_PRODUCT_REQUIREMENTS")

    def test_A004_empty_spec_never_exits_0(self) -> None:
        from spec_refuse.check import check_specification

        with tempfile.TemporaryDirectory() as td:
            path = Path(td) / "SPEC.md"
            path.write_text("The specification follows.\n---\n\n", encoding="utf-8")
            code, payload = check_specification(path)
        self.assertNotEqual(code, 0, "silence must never read as agreement")
        self.assertNotEqual(payload.get("verdict"), "OK")

    def test_A005_cli_missing_spec_process_exit_2(self) -> None:
        import subprocess
        import sys

        env = dict(os.environ)
        src = str(Path(__file__).resolve().parents[1] / "src")
        env["PYTHONPATH"] = src + os.pathsep + env.get("PYTHONPATH", "")
        missing = str(Path(tempfile.gettempdir()) / "spec-refuse-absent-cli.md")
        proc = subprocess.run(
            [sys.executable, "-m", "spec_refuse", "check", missing],
            capture_output=True,
            text=True,
            env=env,
        )
        self.assertEqual(proc.returncode, 2)
        self.assertIn("REFUSED", proc.stdout)

    def test_A006_conformance_counts_named_zero_when_spec_empty(self) -> None:
        from spec_refuse.conformance import conformance_report

        with tempfile.TemporaryDirectory() as td:
            path = Path(td) / "SPEC.md"
            path.write_text("The specification follows.\n---\n", encoding="utf-8")
            report = conformance_report(path)
        self.assertEqual(report["acceptance_named"], 0)
        self.assertEqual(report["acceptance_pass"], 0)
        self.assertEqual(report["acceptance_fail"], 0)
        self.assertEqual(report["acceptance_not_implemented"], 0)
        self.assertEqual(report["verdict"], "REFUSED")
        self.assertEqual(report["exit"], 2)

    def test_A007_benchmark_refuses_when_no_algorithm_named(self) -> None:
        from spec_refuse.benchmark import run_benchmark

        with tempfile.TemporaryDirectory() as td:
            path = Path(td) / "SPEC.md"
            path.write_text("---\n", encoding="utf-8")
            code, table = run_benchmark(path)
        self.assertEqual(code, 2)
        self.assertEqual(table["verdict"], "REFUSED")
        self.assertEqual(table["reason_code"], "NO_ALGORITHM_NAMED")
        self.assertEqual(table["rows"], [])

    def test_A008_payload_is_json_object_with_required_keys(self) -> None:
        from spec_refuse.check import check_specification

        with tempfile.TemporaryDirectory() as td:
            path = Path(td) / "SPEC.md"
            path.write_text("", encoding="utf-8")
            code, payload = check_specification(path)
        self.assertEqual(code, 2)
        for key in ("verdict", "exit", "reason_code", "reason", "ambiguities"):
            self.assertIn(key, payload)
        self.assertIsInstance(payload["ambiguities"], list)
        self.assertGreaterEqual(len(payload["ambiguities"]), 1)
        raw = json.dumps(payload)
        self.assertIsInstance(raw, str)


class TestEncodingContract(unittest.TestCase):
    def test_E001_open_wrapper_passes_utf8(self) -> None:
        from spec_refuse.io import open_utf8

        with tempfile.TemporaryDirectory() as td:
            path = Path(td) / "x.txt"
            path.write_text("café — Ω", encoding="utf-8")
            with open_utf8(path, "r") as fh:
                self.assertEqual(fh.encoding.lower(), "utf-8")
                self.assertEqual(fh.read(), "café — Ω")

    def test_E002_module_reconfigures_stdout(self) -> None:
        import spec_refuse

        self.assertTrue(getattr(spec_refuse, "_STDOUT_RECONFIGURED", False))


if __name__ == "__main__":
    unittest.main()
