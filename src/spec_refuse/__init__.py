"""spec_refuse — fail-closed gate for an absent product specification.

Exit contract
-------------
0  checked and correct
1  checked and wrong
2  could not check (REFUSE)

A missing, empty, or divider-only specification cannot be checked.
It must REFUSE. Silence is never treated as agreement.
"""

from __future__ import annotations

import sys

_STDOUT_RECONFIGURED = False

if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        _STDOUT_RECONFIGURED = True
    except (OSError, ValueError, AttributeError):
        _STDOUT_RECONFIGURED = False

__all__ = ["__version__", "_STDOUT_RECONFIGURED"]
__version__ = "0.1.0"
