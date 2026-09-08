"""Decide whether a product specification can be checked."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from spec_refuse.io import open_utf8

EXIT_OK = 0
EXIT_WRONG = 1
EXIT_REFUSE = 2

_DIVIDER = "---"


def _ambiguities() -> list[str]:
    return [
        "The product specification body after the divider was empty.",
        "No library name, module layout, public signatures, JSON keys, or test ids were named.",
        "No algorithm was named, so complexity and benchmarks cannot be measured.",
        "No acceptance-case ids were named.",
        "No third-party dependencies were named; only the standard library is used.",
        "The build rules name DECISIONS.md and MIT, but no product files.",
        "Whether a preamble before 'The specification follows' is itself a spec is unspecified; treated as not a spec.",
        "Whether whitespace or a lone '---' counts as a body is unspecified; treated as no body (fail closed).",
        "Whether inventing a domain library would satisfy 'do not stop' is unspecified; inventing unnamed scope is forbidden.",
    ]


def _product_body(text: str) -> str:
    """Return text after the last specification divider, else the whole text."""
    if _DIVIDER in text:
        return text.rsplit(_DIVIDER, 1)[-1]
    return text


def _has_product_requirements(body: str) -> bool:
    """Fail closed: only non-empty non-separator prose counts as requirements."""
    stripped = body.strip()
    if not stripped:
        return False
    lines = [ln.strip() for ln in stripped.splitlines() if ln.strip()]
    useful = [ln for ln in lines if not set(ln) <= set("-=#*_`~ ")]
    return len(useful) > 0


def check_specification(path: str | Path) -> tuple[int, dict[str, Any]]:
    path = Path(path)
    payload: dict[str, Any] = {
        "verdict": "REFUSED",
        "exit": EXIT_REFUSE,
        "reason_code": "UNSPECIFIED",
        "reason": "",
        "ambiguities": _ambiguities(),
        "spec_path": str(path),
        "acceptance_named": 0,
    }

    if not path.exists() or not path.is_file():
        payload["reason_code"] = "MISSING_SPEC"
        payload["reason"] = f"specification file does not exist: {path}"
        payload["exit"] = EXIT_REFUSE
        payload["verdict"] = "REFUSED"
        return EXIT_REFUSE, payload

    try:
        with open_utf8(path, "r") as fh:
            text = fh.read()
    except UnicodeDecodeError:
        payload["reason_code"] = "NOT_UTF8"
        payload["reason"] = f"specification is not valid UTF-8: {path}"
        payload["exit"] = EXIT_REFUSE
        payload["verdict"] = "REFUSED"
        return EXIT_REFUSE, payload
    except OSError as exc:
        payload["reason_code"] = "UNREADABLE"
        payload["reason"] = f"specification could not be read: {path}: {exc}"
        payload["exit"] = EXIT_REFUSE
        payload["verdict"] = "REFUSED"
        return EXIT_REFUSE, payload

    if text.strip() == "":
        payload["reason_code"] = "EMPTY_SPEC"
        payload["reason"] = "specification file is empty"
        return EXIT_REFUSE, payload

    body = _product_body(text)
    if not _has_product_requirements(body):
        payload["reason_code"] = "NO_PRODUCT_REQUIREMENTS"
        payload["reason"] = (
            "specification body after the divider names no product requirements"
        )
        return EXIT_REFUSE, payload

    payload["reason_code"] = "UNCHECKABLE_BODY"
    payload["reason"] = (
        "specification text is present but this tool has no named checks "
        "for a product domain; refusing rather than treating silence as pass"
    )
    payload["exit"] = EXIT_REFUSE
    payload["verdict"] = "REFUSED"
    return EXIT_REFUSE, payload
