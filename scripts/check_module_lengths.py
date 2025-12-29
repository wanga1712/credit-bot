"""Utility to ensure modules respect the 150-line limit."""

from __future__ import annotations

import pathlib
import sys
from typing import Iterable


MAX_LINES = 150
PROJECT_ROOT = pathlib.Path(__file__).resolve().parents[1]
TARGET_DIRS = ("credit_bot",)
EXCLUDED_FILES = {"__init__.py"}


def iter_python_files() -> Iterable[pathlib.Path]:
    """Yield Python files under target directories."""

    for target in TARGET_DIRS:
        base = PROJECT_ROOT / target
        for path in base.rglob("*.py"):
            if path.name in EXCLUDED_FILES:
                continue
            yield path


def file_exceeds_limit(path: pathlib.Path) -> bool:
    """Return True if file exceeds the configured line limit."""

    with path.open("r", encoding="utf-8") as fh:
        return sum(1 for _ in fh) > MAX_LINES


def main() -> int:
    offenders = [path for path in iter_python_files() if file_exceeds_limit(path)]
    if offenders:
        print("Modules exceeding 150 lines:")
        for path in offenders:
            print(f" - {path.relative_to(PROJECT_ROOT)}")
        return 1
    print("All modules comply with the 150-line limit.")
    return 0


if __name__ == "__main__":
    sys.exit(main())

