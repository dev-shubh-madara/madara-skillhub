#!/usr/bin/env python3
"""Basic safety scan for a skill folder before it is installed.

This is a pattern check, not a guarantee. It catches the common bad signs:
  - code that downloads and runs other code
  - encoded blobs that get decoded and executed
  - shell=True, eval and exec
  - reads of ssh keys, cloud credentials or .env files in code
  - text in markdown that tries to steer the assistant against the user

Usage:
  python3 scripts/audit_skill.py skills/frontend-builder [more folders...]
Exit code is 1 if any folder has a high severity finding.
"""
import re
import sys
from pathlib import Path

CODE_SUFFIXES = {".py", ".sh", ".bash", ".js", ".mjs", ".ts", ".ps1", ".bat"}
TEXT_SUFFIXES = {".md", ".txt", ".json", ".yaml", ".yml"}

CODE_RULES = [
    ("high", r"(curl|wget)[^\n|]*\|\s*(sudo\s+)?(ba)?sh", "downloads and pipes into a shell"),
    ("high", r"base64[^\n]*(-d|--decode|b64decode)[^\n]*(exec|eval|\|\s*(ba)?sh)", "decodes a blob and runs it"),
    ("high", r"\b(eval|exec)\s*\(", "uses eval or exec"),
    ("high", r"shell\s*=\s*True", "runs a shell command string"),
    ("high", r"os\.system\s*\(", "runs a shell command string"),
    ("high", r"(\.ssh/|id_rsa|\.aws/credentials|\.netrc)", "touches ssh keys or cloud credentials"),
    ("high", r"open\([^)]*\.env['\"]", "reads a .env file"),
    ("medium", r"(requests|urllib|httpx|fetch)\b[^\n]*https?://", "makes a network request"),
    ("medium", r"\brm\s+-rf\b", "deletes recursively"),
    ("medium", r"\bchmod\s+(\+x|7[0-7][0-7])", "changes file permissions"),
]

TEXT_RULES = [
    ("high", r"ignore (all |any )?(previous|prior|above) (instructions|rules)", "tries to override earlier instructions"),
    ("high", r"(do not|don't|never) (tell|inform|show) the user", "asks to hide things from the user"),
    ("high", r"(send|post|upload|exfiltrate)[^\n]{0,60}(token|password|api[_ -]?key|secret|credential)", "asks to send secrets somewhere"),
    ("medium", r"disable (the )?(safety|security|verification)", "asks to turn off safety checks"),
]


def scan_file(path):
    findings = []
    suffix = path.suffix.lower()
    if suffix in CODE_SUFFIXES:
        rules = CODE_RULES
    elif suffix in TEXT_SUFFIXES:
        rules = TEXT_RULES
    else:
        return findings
    try:
        lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
    except OSError as exc:
        return [("medium", path, 0, f"could not read file: {exc}")]
    for number, line in enumerate(lines, start=1):
        for severity, pattern, message in rules:
            if re.search(pattern, line, re.IGNORECASE):
                findings.append((severity, path, number, message))
    return findings


def audit_folder(folder):
    folder = Path(folder)
    findings = []
    if not (folder / "SKILL.md").is_file():
        findings.append(("high", folder, 0, "no SKILL.md in this folder"))
    for path in sorted(folder.rglob("*")):
        if path.is_file() and ".git" not in path.parts:
            findings.extend(scan_file(path))
    return findings


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        return 2
    exit_code = 0
    for arg in sys.argv[1:]:
        findings = audit_folder(arg)
        highs = [f for f in findings if f[0] == "high"]
        label = "FAIL" if highs else ("warn" if findings else "ok  ")
        print(f"{label}  {arg}")
        for severity, path, number, message in findings:
            where = f"{path}:{number}" if number else str(path)
            print(f"      [{severity}] {where}  {message}")
        if highs:
            exit_code = 1
    return exit_code


if __name__ == "__main__":
    sys.exit(main())
