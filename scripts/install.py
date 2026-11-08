#!/usr/bin/env python3
"""Install skills from this repo into Claude Code's skills folder.

Examples:
  python3 scripts/install.py --list
  python3 scripts/install.py --all
  python3 scripts/install.py --only frontend-builder,study-coach
  python3 scripts/install.py --all --dry-run
  python3 scripts/install.py --all --dest ./.claude/skills     # one project only

Every skill is audited first. A skill that fails the audit is skipped.
Folders installed by this script get a .skillhub marker file, so a later run
can update them without touching skills you wrote yourself. Use --force to
overwrite a folder that has no marker.
"""
import argparse
import importlib.util
import shutil
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
SKILLS = REPO / "skills"
MARKER = ".skillhub"


def load_module(name, filename):
    spec = importlib.util.spec_from_file_location(name, Path(__file__).resolve().parent / filename)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def available():
    return sorted(p.name for p in SKILLS.iterdir() if p.is_dir() and (p / "SKILL.md").is_file())


def describe(name):
    validate = load_module("validate_skills", "validate_skills.py")
    fields, _ = validate.parse_frontmatter((SKILLS / name / "SKILL.md").read_text(encoding="utf-8"))
    return (fields or {}).get("description", "")


def main():
    parser = argparse.ArgumentParser(description="Install skills from madara-skillhub")
    parser.add_argument("--list", action="store_true", help="show available skills and exit")
    parser.add_argument("--all", action="store_true", help="install every skill")
    parser.add_argument("--only", help="comma separated skill names")
    parser.add_argument("--dest", default=str(Path.home() / ".claude" / "skills"), help="target folder")
    parser.add_argument("--dry-run", action="store_true", help="show what would happen, change nothing")
    parser.add_argument("--force", action="store_true", help="overwrite folders not installed by this script")
    args = parser.parse_args()

    names = available()
    if args.list or not (args.all or args.only):
        for name in names:
            print(f"{name:22} {describe(name)[:90]}")
        if not args.list:
            print("\nChoose with --all or --only name1,name2")
        return 0

    if args.all:
        chosen = names
    else:
        chosen = [n.strip() for n in args.only.split(",") if n.strip()]
        unknown = [n for n in chosen if n not in names]
        if unknown:
            print("Unknown skills: " + ", ".join(unknown))
            print("Available: " + ", ".join(names))
            return 1

    if "skillhub" in names and "skillhub" not in chosen and args.all:
        chosen.insert(0, "skillhub")

    audit = load_module("audit_skill", "audit_skill.py")
    validate = load_module("validate_skills", "validate_skills.py")
    dest = Path(args.dest).expanduser()
    installed, skipped = [], []

    for name in chosen:
        source = SKILLS / name
        problems = validate.check_skill(source)
        findings = [f for f in audit.audit_folder(source) if f[0] == "high"]
        if problems or findings:
            reason = "; ".join(problems + [f"{f[3]} ({f[1].name}:{f[2]})" for f in findings])
            skipped.append((name, reason))
            continue
        target = dest / name
        if target.exists() and not (target / MARKER).exists() and not args.force:
            skipped.append((name, "a skill with this name exists and was not installed by skillhub (use --force)"))
            continue
        if args.dry_run:
            installed.append(name)
            continue
        if target.exists():
            shutil.rmtree(target)
        shutil.copytree(source, target)
        (target / MARKER).write_text("installed by madara-skillhub\n", encoding="utf-8")
        installed.append(name)

    verb = "Would install" if args.dry_run else "Installed"
    print(f"{verb} {len(installed)} skill(s) into {dest}")
    for name in installed:
        print(f"  + {name}")
    for name, reason in skipped:
        print(f"  - skipped {name}: {reason}")
    return 1 if skipped else 0


if __name__ == "__main__":
    sys.exit(main())
