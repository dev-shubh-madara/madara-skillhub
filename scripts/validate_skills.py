#!/usr/bin/env python3
"""Check that every skill folder in skills/ is well formed.

Rules:
  - the folder has a SKILL.md
  - frontmatter has name and description
  - name matches the folder name (lowercase letters, digits, hyphens)
  - description is 1 to 1024 characters and has no angle brackets
  - the body is not empty

Usage:
  python3 scripts/validate_skills.py [skills_dir]
Exit code is 1 if any skill fails.
"""
import re
import sys
from pathlib import Path

NAME_RE = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")


def parse_frontmatter(text):
    """Return (fields, body) or (None, text) if there is no frontmatter."""
    if not text.startswith("---"):
        return None, text
    parts = text.split("\n")
    end = None
    for i in range(1, len(parts)):
        if parts[i].strip() == "---":
            end = i
            break
    if end is None:
        return None, text
    fields = {}
    for line in parts[1:end]:
        if ":" in line:
            key, _, value = line.partition(":")
            fields[key.strip()] = value.strip()
    return fields, "\n".join(parts[end + 1:])


def check_skill(folder):
    problems = []
    skill_md = folder / "SKILL.md"
    if not skill_md.is_file():
        return ["missing SKILL.md"]
    fields, body = parse_frontmatter(skill_md.read_text(encoding="utf-8"))
    if fields is None:
        return ["missing or unclosed frontmatter"]
    name = fields.get("name", "")
    desc = fields.get("description", "")
    if not name:
        problems.append("frontmatter has no name")
    elif not NAME_RE.match(name):
        problems.append(f"name '{name}' must be lowercase letters, digits and hyphens")
    elif name != folder.name:
        problems.append(f"name '{name}' does not match folder '{folder.name}'")
    if not desc:
        problems.append("frontmatter has no description")
    else:
        if len(desc) > 1024:
            problems.append(f"description is {len(desc)} characters, limit is 1024")
        if "<" in desc or ">" in desc:
            problems.append("description contains angle brackets")
    if not body.strip():
        problems.append("body is empty")
    return problems


def main():
    root = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).resolve().parent.parent / "skills"
    if not root.is_dir():
        print(f"skills folder not found: {root}")
        return 1
    folders = sorted(p for p in root.iterdir() if p.is_dir())
    if not folders:
        print("no skills found")
        return 1
    failed = 0
    for folder in folders:
        problems = check_skill(folder)
        if problems:
            failed += 1
            print(f"FAIL  {folder.name}")
            for p in problems:
                print(f"      - {p}")
        else:
            print(f"ok    {folder.name}")
    print(f"\n{len(folders) - failed} of {len(folders)} skills passed")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
