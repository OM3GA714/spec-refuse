# Decisions

Fail-closed choices made where the received text was silent.

## D001 — The product specification body is empty

**Choice:** Treat the received message as a build wrapper plus an empty product specification.

The wrapper ends with “The specification follows.” and a divider `---`.
Nothing follows the divider. No library domain, filename (other than
`DECISIONS.md` in the wrapper), public signature, JSON key, test id,
algorithm, acceptance-case id, or third-party dependency was named.

**Rejected alternative:** Invent a domain library (JSON validator, graph
library, etc.) so that “do not stop” can be satisfied by activity.
Inventing unnamed scope is listed as a defect in the wrapper.

## D002 — Missing specification → exit 2, never 0

**Choice:** `check_specification` returns exit 2 (`REFUSED`) when the spec
file is missing, empty, not UTF-8, unreadable, or has no product-requirement
prose after the divider.

**Rejected alternative:** Exit 0 with “nothing to check”. Silence must never
read as agreement.

## D003 — A non-empty body still does not pass

**Choice:** Even if someone later writes prose after the divider, this tool
still REFUSES unless a later version is given named checks. This version has
no product-domain checks because none were specified.

**Rejected alternative:** Exit 0 when any non-empty text exists. That would
treat the presence of words as correctness.

## D004 — Acceptance-case ids in this repository

**Choice:** The wrapper asked for “every acceptance case id” but named none.
The tests `A001`–`A008` and `E001`–`E002` are tests of the *wrapper’s* fail-closed
rules, not product acceptance cases. Conformance reports `acceptance_named: 0`.

**Rejected alternative:** Relabel A001–A008 as the specification’s acceptance
cases. That would invent ids the specification did not name.

## D005 — Benchmark

**Choice:** `run_benchmark` returns exit 2, empty `rows`, empty
`scaling_ratios`, and `complexity_estimate: "UNIDENTIFIED"`.

**Rejected alternative:** Time a dummy loop and publish a table. That would
be a complexity claim with no named algorithm.

## D006 — Dependencies

**Choice:** Standard library only. The wrapper allows dependencies the
specification names; the specification named none.

## D007 — Encoding

**Choice:** Every file open in this package goes through `open_utf8`, which
sets `encoding="utf-8"`. Package import calls `sys.stdout.reconfigure(encoding="utf-8")`
when that method exists. If reconfigure raises, `_STDOUT_RECONFIGURED` is
False; we do not pretend it succeeded.

## D008 — CLI default path

**Choice:** With no path argument, the CLI reads `SPEC.md` in the current
working directory. A missing file is REFUSED, not treated as a default-pass.

## D009 — What counts as a product-requirement body

**Choice:** After the last `---` divider, strip whitespace. If nothing
remains, or only rule-out lines made of `-=#*_`~ ` characters remain, there
are no product requirements.

**Rejected alternative:** Treat the wrapper preamble (build rules, report
order) as the product specification. Those rules constrain the *build
process*, not a library’s public API.

## D010 — Repository name

**Choice:** `spec-refuse`. The specification did not name a repository.
The name states the only behaviour that could be implemented without
inventing a domain.

## D011 — Public visibility

**Choice:** The repository is created public, as the wrapper required.
`LICENSE` is MIT, copyright OM3GA714 (the controlling GitHub account).

## D012 — Tests that import the implementation

The wrapper required writing each failing test before the code that
satisfies it. The tests in `tests/test_refuse_missing_spec.py` were written
and run red (`ModuleNotFoundError` / wrong exit) before
`src/spec_refuse/` existed as an implementation.
