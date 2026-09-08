"""UTF-8 file opens. Required for Windows-safe behaviour."""

from __future__ import annotations

from pathlib import Path
from typing import IO, Any


def open_utf8(path: str | Path, mode: str = "r", **kwargs: Any) -> IO[str]:
    kwargs["encoding"] = "utf-8"
    return open(path, mode, **kwargs)
