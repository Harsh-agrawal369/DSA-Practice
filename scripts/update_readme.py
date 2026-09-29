"""Generate README.md from Python solution files."""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
README = ROOT / "README.md"
START_MARKER = "<!-- SOLUTIONS:START -->"
END_MARKER = "<!-- SOLUTIONS:END -->"
SLUG_SEPARATOR_PATTERN = re.compile(r"[^a-z0-9]+")


def problem_title(path: Path) -> str:
    return path.stem.replace("_", " ").replace("-", " ").title()


def leetcode_slug(path: Path) -> str:
    slug = SLUG_SEPARATOR_PATTERN.sub("-", path.stem.lower()).strip("-")
    return slug


def solution_row(path: Path) -> tuple[str, str, str, str]:
    relative_path = path.relative_to(ROOT).as_posix()
    solution_link = f"[{path.name}]({relative_path})"
    domain = path.relative_to(ROOT).parts[0]
    leetcode_link = f"[LeetCode](https://leetcode.com/problems/{leetcode_slug(path)}/description/)"
    return domain, problem_title(path), leetcode_link, solution_link


def render_solutions() -> str:
    rows = []
    for path in sorted(ROOT.glob("**/*.py")):
        if "scripts" in path.parts or any(part.startswith(".") for part in path.relative_to(ROOT).parts):
            continue
        rows.append(solution_row(path))

    if not rows:
        return "No solution files yet. Add a `.py` file in a topic folder to list it here."

    lines = ["| Domain | Problem | LeetCode | Solution |", "| --- | --- | --- | --- |"]
    lines.extend(
        f"| {domain} | {title} | {leetcode_link} | {solution_link} |"
        for domain, title, leetcode_link, solution_link in rows
    )
    return "\n".join(lines)


def update_readme() -> None:
    solutions = render_solutions()
    generated = f"""# DSA Practice

A collection of LeetCode questions and Python solutions organized by domain.

## Workflow

1. Create a `.py` file inside a domain folder using the exact LeetCode question name in kebab-case. For example:

   `Arrays/find-missing-and-repeated-values.py`

2. Save the file. The local README watcher updates this page automatically.

You can also run `python scripts/update_readme.py` manually. The README uses the filename to create the LeetCode URL and the parent folder to determine the domain.

## Solutions

{START_MARKER}
{solutions}
{END_MARKER}
"""
    README.write_text(generated, encoding="utf-8")


if __name__ == "__main__":
    update_readme()
    print(f"Updated {README.relative_to(ROOT)}")
