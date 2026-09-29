"""Regenerate README.md whenever a solution file changes."""

from __future__ import annotations

import time
from pathlib import Path

from update_readme import ROOT, update_readme

POLL_SECONDS = 1


def solution_files() -> list[Path]:
    return [
        path
        for path in ROOT.glob("**/*.py")
        if "scripts" not in path.parts
        and not any(part.startswith(".") for part in path.relative_to(ROOT).parts)
    ]


def file_state() -> dict[Path, int]:
    return {path: path.stat().st_mtime_ns for path in solution_files()}


def watch() -> None:
    update_readme()
    previous_state = file_state()
    print("Watching solution files for README changes...")

    while True:
        time.sleep(POLL_SECONDS)
        current_state = file_state()
        if current_state != previous_state:
            update_readme()
            previous_state = current_state
            print("README updated.")


if __name__ == "__main__":
    try:
        watch()
    except KeyboardInterrupt:
        print("README watcher stopped.")
