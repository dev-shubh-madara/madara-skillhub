# README template and pre-publish checks

## Skeleton

```markdown
# project-name

One sentence: what it does and for whom.

![demo](docs/demo.gif)

## Why I made it
Two or three sentences in the author's own words.

## Quick start
    git clone https://github.com/OWNER/REPO
    cd REPO
    cp .env.example .env      # fill in the values
    pip install -r requirements.txt
    python main.py

## Usage
A real example with real output.

## Configuration
| Variable | Required | What it does |
|---|---|---|

## How it works
A short paragraph or a small diagram.

## Limits
What it does not do yet. Known issues.

## License
MIT
```

Cut any section that has nothing true to say.

## Pre-publish checklist

- [ ] Fresh clone, follow the README exactly, it runs.
- [ ] `.gitignore` covers `.env`, `node_modules/`, `__pycache__/`, `venv/`, build output, OS files.
- [ ] `.env.example` lists every variable the code reads.
- [ ] No secrets in the history:
      `git log -p | grep -iE "api[_-]?key|secret|token|password" | head`
      For a deeper scan, run a tool like gitleaks. A leaked key must be rotated.
- [ ] No large binaries or data dumps committed by accident (`git count-objects -vH`).
- [ ] License file present and the copyright line has the owner's name.
- [ ] Repo description and 4 to 8 topics set on GitHub.
- [ ] A screenshot or GIF near the top.
- [ ] First release tagged (`v0.1.0`) with a few lines on what is in it.

## Voice

Write like the owner explains the project to a friend: first person, short sentences, specific. Remove phrases such as "powerful", "seamless", "leverage", "cutting-edge", "robust solution", and any line that only describes the README itself.
