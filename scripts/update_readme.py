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

Practice common data structures and algorithms with Python solutions to LeetCode problems. Solutions are organized by domain, and the README index is generated automatically from the files in this repository.

## Setup

Clone the repository and move into its folder:

```powershell
git clone https://github.com/Harsh-agrawal369/DSA-Practice.git
cd DSA-Practice
```

Install the local post-push hook once:

```powershell
powershell -ExecutionPolicy Bypass -File scripts/install-post-push-hook.ps1
```

The hook waits for the GitHub Actions README commit after `git push`, then pulls it with rebase so your local branch stays synchronized.

## Add A Solution

Create a Python file inside the appropriate domain folder. Use the exact LeetCode question name in kebab-case. For example:

```text
Arrays/find-missing-and-repeated-values.py
```

The updater automatically uses:

- The parent folder as the domain.
- The filename as the problem name and LeetCode URL slug.
- The filename and path as the repository solution link.

No question names or links need to be added manually anywhere.

## README Updates

After a solution is pushed, GitHub Actions runs `scripts/update_readme.py` and commits the updated README automatically. You can also update it manually:

```powershell
python scripts/update_readme.py
```

For local README updates whenever a Python file is saved, open `.vscode/tasks.json` and uncomment line 11:

```json
"runOn": "folderOpen"
```

Then allow automatic tasks when VS Code asks. This local watcher is optional; the GitHub Actions updater still works without it.

## CI/CD Flow

1. Create or delete a solution `.py` file and commit your change locally.
2. Run `git push`.
3. GitHub Actions checks out the branch and runs `scripts/update_readme.py`. The workflow runs for any branch that contains `.github/workflows/update-readme.yml`.
4. The script rebuilds the Solutions table from all available solution files.
5. GitHub Actions commits the updated README to the remote branch.
6. The local post-push hook detects that commit and runs `git pull --rebase`.

This keeps the README synchronized without manually adding or removing question entries.

## Solutions

{START_MARKER}
{solutions}
{END_MARKER}
"""
    README.write_text(generated, encoding="utf-8")


if __name__ == "__main__":
    update_readme()
    print(f"Updated {README.relative_to(ROOT)}")
