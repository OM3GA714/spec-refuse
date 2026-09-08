# spec-refuse

Fail-closed checker for a product specification that was never supplied.

This is not a domain library. The build request asked for a standalone
open-source Python library under an MIT licence, then said “The
specification follows” and ended. No public API, algorithm, acceptance
case, or dependency was named. Inventing one would have been extra scope.

What this package does instead is the only check the wrapper made
decidable:

- exit `0` — checked and correct
- exit `1` — checked and wrong
- exit `2` — could not check (REFUSE)

A missing, empty, unreadable, non-UTF-8, or divider-only specification
REFUSES. It never exits `0`. Silence is not agreement.

Standard library only. Python 3.9+.

## Install / run

```
PYTHONPATH=src python -m spec_refuse check SPEC.md
PYTHONPATH=src python -m spec_refuse conformance SPEC.md
PYTHONPATH=src python -m spec_refuse benchmark SPEC.md
PYTHONPATH=src python -m unittest discover -s tests -v
```

## Contract

| Exit | Verdict  | Meaning                                      |
| ---: | -------- | -------------------------------------------- |
|    0 | OK       | Specification present and all named checks passed. This version has no named product checks, so this exit is unused. |
|    1 | WRONG    | Specification present and a named check failed. Unused in this version. |
|    2 | REFUSED  | Could not check. The received specification is empty. |

## What this does not cover

- It does not invent a product domain.
- It does not time an unnamed algorithm and call the result a complexity class.
- It does not treat “the file exists” as “the product is correct”.
- An evidence path is not opened, because no evidence path was named.

See `DECISIONS.md` for every fail-closed choice.
