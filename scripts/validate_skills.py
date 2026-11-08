#!/usr/bin/env python3
"""Check that every skill folder in skills/ is well formed.

Rules:
  - the folder has a SKILL.md
  - the frontmatter is valid YAML and is a mapping
  - it has name and description, both plain strings
  - name matches the folder name (lowercase letters, digits, hyphens, max 64)
  - description is 20 to 1024 characters and has no angle brackets
  - the body is not empty and has at least one heading
  - every file the body links to under references/ exists

The frontmatter is parsed with PyYAML when it is installed. Without it, a
strict fallback parser is used that rejects the most common mistake: an
unquoted value that contains ": " (YAML reads that as a nested mapping).

Usage:
  python3 scripts/validate_skills.py [skills_dir]
Exit code is 1 if any skill fails.
"""
import re
import sys
from pathlib import Path

try:
    import yaml
except ImportError:  # the fallback below still catches the usual errors
    yaml = None

NAME_RE = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
REF_RE = re.compile(r"references/[A-Za-z0-9_./-]+\.md")


class FrontmatterError(ValueError):
    pass


def split_frontmatter(text):
    """Return (raw_yaml, body). Raise FrontmatterError if it is missing or unclosed."""
    lines = text.split("\n")
    if not lines or lines[0].strip() != "---":
        raise FrontmatterError("file must start with a --- frontmatter line")
    for i in range(1, len(lines)):
        if lines[i].strip() == "---":
            return "\n".join(lines[1:i]), "\n".join(lines[i + 1:])
    raise FrontmatterError("frontmatter is not closed with ---")


def _fallback_load(raw):
    fields = {}
    for number, line in enumerate(raw.split("\n"), start=2):
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        if line[0] in " \t":
            raise FrontmatterError(f"line {number}: indented lines are not supported without PyYAML")
        key, sep, value = line.partition(":")
        if not sep:
            raise FrontmatterError(f"line {number}: expected key: value")
        value = value.strip()
        if value[:1] in ('"', "'"):
            quote = value[0]
            if len(value) < 2 or value[-1] != quote:
                raise FrontmatterError(f"line {number}: quoted value is not closed")
            value = value[1:-1]
        elif ": " in value or value.endswith(":"):
            raise FrontmatterError(f"line {number}: value contains ': ' and must be quoted")
        fields[key.strip()] = value
    return fields


def load_frontmatter(raw):
    if yaml is None:
        return _fallback_load(raw)
    try:
        data = yaml.safe_load(raw)
    except yaml.YAMLError as exc:
        mark = getattr(exc, "problem_mark", None)
        where = f"line {mark.line + 2}" if mark else "frontmatter"
        problem = getattr(exc, "problem", None) or str(exc).splitlines()[0]
        raise FrontmatterError(f"{where}: invalid YAML ({problem})")
    if not isinstance(data, dict):
        raise FrontmatterError("frontmatter must be a set of key: value pairs")
    return data


def parse_frontmatter(text):
    """Return (fields, body), or (None, text) if the frontmatter is broken."""
    try:
        raw, body = split_frontmatter(text)
        return load_frontmatter(raw), body
    except FrontmatterError:
        return None, text


def check_skill(folder):
    folder = Path(folder)
    skill_md = folder / "SKILL.md"
    if not skill_md.is_file():
        return ["missing SKILL.md"]
    text = skill_md.read_text(encoding="utf-8")
    try:
        raw, body = split_frontmatter(text)
        fields = load_frontmatter(raw)
    except FrontmatterError as exc:
        return [str(exc)]

    problems = []
    name = fields.get("name")
    desc = fields.get("description")
    if not isinstance(name, str) or not name:
        problems.append("frontmatter needs a text name")
    elif len(name) > 64 or not NAME_RE.match(name):
        problems.append(f"name '{name}' must be lowercase letters, digits and hyphens, max 64")
    elif name != folder.name:
        problems.append(f"name '{name}' does not match folder '{folder.name}'")

    if not isinstance(desc, str) or not desc:
        problems.append("frontmatter needs a text description")
    else:
        if len(desc) < 20:
            problems.append("description is too short to trigger reliably")
        if len(desc) > 1024:
            problems.append(f"description is {len(desc)} characters, limit is 1024")
        if "<" in desc or ">" in desc:
            problems.append("description contains angle brackets")

    if not body.strip():
        problems.append("body is empty")
    elif not re.search(r"^#{1,3} ", body, re.M):
        problems.append("body has no headings")

    for ref in sorted(set(REF_RE.findall(body))):
        if not (folder / ref).is_file():
            problems.append(f"links to {ref}, which does not exist")
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
    if yaml is None:
        print("note: PyYAML not installed, using the strict fallback parser\n")
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
