#!/usr/bin/env python3
"""Build one upload-ready ZIP per skill into dist/.

Each ZIP has the skill folder at its root, which is the layout claude.ai
expects:  frontend-builder.zip -> frontend-builder/SKILL.md, references/...

Usage:
  python3 scripts/package.py            # build all
  python3 scripts/package.py --check    # fail if dist/ is out of date
"""
import argparse
import importlib.util
import io
import sys
import zipfile
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
SKILLS = REPO / "skills"
DIST = REPO / "dist"
FIXED_TIME = (2026, 1, 1, 0, 0, 0)   # fixed timestamps so the same input gives the same ZIP


def load_validator():
    spec = importlib.util.spec_from_file_location("validate_skills", REPO / "scripts" / "validate_skills.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def build_zip(folder):
    buffer = io.BytesIO()
    with zipfile.ZipFile(buffer, "w", zipfile.ZIP_DEFLATED) as zf:
        for path in sorted(folder.rglob("*")):
            if path.is_file() and path.name != ".skillhub" and "__pycache__" not in path.parts:
                info = zipfile.ZipInfo(f"{folder.name}/{path.relative_to(folder).as_posix()}", FIXED_TIME)
                info.compress_type = zipfile.ZIP_DEFLATED
                info.external_attr = 0o644 << 16
                zf.writestr(info, path.read_bytes())
    return buffer.getvalue()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true", help="exit 1 if any ZIP in dist/ is missing or stale")
    args = parser.parse_args()

    validator = load_validator()
    folders = sorted(p for p in SKILLS.iterdir() if p.is_dir())
    DIST.mkdir(exist_ok=True)
    stale = []
    for folder in folders:
        problems = validator.check_skill(folder)
        if problems:
            print(f"FAIL  {folder.name}: " + "; ".join(problems))
            return 1
        data = build_zip(folder)
        target = DIST / f"{folder.name}.zip"
        if args.check:
            if not target.is_file() or target.read_bytes() != data:
                stale.append(target.name)
            continue
        target.write_bytes(data)
        print(f"built dist/{target.name}  ({len(data) // 1024 + 1} KB)")

    expected = {f"{f.name}.zip" for f in folders}
    extra = sorted(p.name for p in DIST.glob("*.zip") if p.name not in expected)
    if args.check:
        if stale or extra:
            print("dist/ is out of date. Run: python3 scripts/package.py")
            for name in stale + extra:
                print(f"  - {name}")
            return 1
        print(f"dist/ is up to date ({len(folders)} ZIPs)")
    elif extra:
        for name in extra:
            (DIST / name).unlink()
            print(f"removed old dist/{name}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
