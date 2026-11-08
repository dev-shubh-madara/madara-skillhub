# Madara SkillHub

A set of Claude skills for the work I kept repeating: building sites and APIs, learning to code, studying for exams, planning a small business, careers, data and repo cleanup. Plus an installer skill, so you can put all of it into Claude with one message.

I built this because most skills I found on GitHub were either too generic or never tested. Each pack here has a defined workflow, a quality bar, a self-check it runs before answering, a reference file with templates and worked examples, and a list of prompts it should and should not react to.

## Install

**In a Claude chat**

Send the link to this repo and write:

> Install all skills from this repo.

Claude reads `INSTALL.md`, checks each skill, and shows you a save card for each one. Tap save on the ones you want.

You can also ask for a few: "install only the frontend and study packs from this repo."

**In Claude Code**

```
git clone https://github.com/dev-shubh-madara/madara-skillhub
cd madara-skillhub
python3 scripts/install.py --all
```

Useful options:

```
python3 scripts/install.py --list                  # see what is available
python3 scripts/install.py --only study-coach      # just one
python3 scripts/install.py --all --dry-run         # show what would happen
python3 scripts/install.py --all --dest ./.claude/skills   # this project only
```

Or as a plugin:

```
/plugin marketplace add dev-shubh-madara/madara-skillhub
/plugin install madara-skillhub
```

## What is inside

| Skill | What it does |
|---|---|
| `skillhub` | Installs and fits the other skills to you |
| `frontend-builder` | Landing pages, dashboards, animated sites, responsive fixes |
| `backend-api-builder` | APIs, auth, databases, rate limits, deployment notes |
| `coding-teacher` | Concept, solved example, a harder one you answer, then revision notes |
| `study-coach` | Exam plans, practice tests, revision loops |
| `business-planner` | Idea testing, pricing, first customers, 30 day plan |
| `health-info-guide` | General health information with clear safety limits |
| `research-writer` | Sourced reports and assignments |
| `career-builder` | Resume, LinkedIn, portfolio, interview practice |
| `data-analyst` | Clean, analyze and chart CSV or Excel data |
| `repo-polish` | README, structure and setup checks for your GitHub repo |

## How a skill is built

```
skills/study-coach/
├── SKILL.md                    # when to use it, the workflow, quality bar, self-check
└── references/plan-templates.md   # templates and examples, read only when needed
```

The self-check is the part that matters most for accuracy. Before replying, Claude goes through a short list for that field: did every number come from code that ran, does every claim have a real source, is there an emergency sign in the message, did I invent anything on the resume. If something fails, it fixes it first.

## How it stays safe

- `scripts/audit_skill.py` scans a skill before install for code that downloads and runs things, decodes hidden blobs, reads keys or `.env` files, or tells the assistant to hide things from you. A skill that fails is not installed.
- The installer only touches folders it created itself (it leaves a `.skillhub` marker). A skill you wrote with the same name is not overwritten unless you pass `--force`.
- `scripts/validate_skills.py` parses each skill's frontmatter as real YAML and checks names, descriptions and reference links.
- A GitHub Action runs the validator, the audit and a dry-run install on every push.

The audit is a pattern check. It is not a guarantee, so read any skill you do not know before installing it.

## Check it yourself

```
python3 scripts/validate_skills.py
python3 scripts/audit_skill.py skills/*
```

`evals/triggers.json` lists prompts that should and should not trigger each skill. I run them by hand in a fresh chat with one skill installed.

## Limits

- A skill is a set of instructions that Claude reads when a request matches. It does not retrain Claude, and results still depend on the task and on you checking the output.
- I have not measured a fixed speedup, so I do not claim one.
- The health pack gives general information only. It does not diagnose and it is not a substitute for a doctor.
- In the normal Claude chat you still tap save on each skill. Claude cannot install them silently.

## Add a skill

1. Make `skills/your-skill/SKILL.md` with `name` (same as the folder) and `description` in the frontmatter.
2. Put the workflow, quality bar and a self-check in the body. Quote the description if it contains a colon.
3. Put long templates in `references/` and link them from the body.
4. Add should and should-not prompts to `evals/triggers.json`.
5. Run the two scripts above.

## License

MIT. See `LICENSE`.
