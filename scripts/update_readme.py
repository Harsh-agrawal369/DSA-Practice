"""Generate README.md from Python solution files and the question backlog."""

from __future__ import annotations

import ast
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
README = ROOT / "README.md"
QUESTIONS_FILE = ROOT / "Arrays" / "QuestionsList.txt"
START_MARKER = "<!-- SOLUTIONS:START -->"
END_MARKER = "<!-- SOLUTIONS:END -->"
URL_PATTERN = re.compile(r"https?://\S+")


def title_from_file(path: Path, source: str) -> str:
    """Read the first line of a module docstring, or derive a title from its name."""
    try:
        module = ast.parse(source)
    except SyntaxError:
        module = None

    if module is not None:
        docstring = ast.get_docstring(module)
        if docstring:
            return docstring.splitlines()[0].strip()

    return path.stem.replace("_", " ").replace("-", " ").title()


def solution_row(path: Path) -> tuple[str, str, str]:
    source = path.read_text(encoding="utf-8")
    title = title_from_file(path, source)
    url_match = URL_PATTERN.search(source)
    url = url_match.group(0).rstrip("'\")>,.") if url_match else ""
    relative_path = path.relative_to(ROOT).as_posix()
    solution_link = f"[{path.name}]({relative_path})"
    return title, url, solution_link


def read_questions() -> list[str]:
    if not QUESTIONS_FILE.exists():
        return []
    return [line.strip() for line in QUESTIONS_FILE.read_text(encoding="utf-8").splitlines() if line.strip()]


def render_solutions() -> str:
    rows = []
    for path in sorted(ROOT.glob("**/*.py")):
        if "scripts" in path.parts or any(part.startswith(".") for part in path.relative_to(ROOT).parts):
            continue
        rows.append(solution_row(path))

    if not rows:
        return "No solution files yet. Add a `.py` file in a topic folder to list it here."

    lines = ["| Problem | LeetCode | Solution |", "| --- | --- | --- |"]
    lines.extend(
        f"| {title} | {f'[LeetCode]({url})' if url else '-'} | {solution_link} |"
        for title, url, solution_link in rows
    )
    return "\n".join(lines)


def render_backlog() -> str:
    questions = read_questions()
    if not questions:
        return "No questions in the backlog."
    return "\n".join(f"- {question}" for question in questions)


def update_readme() -> None:
    solutions = render_solutions()
    backlog = render_backlog()
    generated = f"""# DSA Practice

A collection of data structures and algorithms questions and Python solutions.

## Workflow

1. Add a solution inside its topic folder, for example `Arrays/find_missing_and_repeated_values.py`.
2. Start the file with a docstring containing the problem title and URL:

   ```python
   \"\"\"Find Missing and Repeated Values
   https://leetcode.com/problems/find-missing-and-repeated-values/description/
   \"\"\"
   ```

3. Run `python scripts/update_readme.py` to refresh this page.

The generator uses each solution file's first docstring line for the problem name, the first URL it finds for the embedded LeetCode link, and the file path for the embedded repository link.

## Questions Backlog

{backlog}

## Solutions

{START_MARKER}
{solutions}
{END_MARKER}
"""
    README.write_text(generated, encoding="utf-8")


if __name__ == "__main__":
    update_readme()
    print(f"Updated {README.relative_to(ROOT)}")
