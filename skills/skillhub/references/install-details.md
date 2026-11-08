# Install details

## Getting the files without a shell

Fetch raw files from:

```
https://raw.githubusercontent.com/dev-shubh-madara/madara-skillhub/main/INSTALL.md
https://raw.githubusercontent.com/dev-shubh-madara/madara-skillhub/main/skills/<name>/SKILL.md
https://raw.githubusercontent.com/dev-shubh-madara/madara-skillhub/main/skills/<name>/references/<file>.md
```

The skill list is: skillhub, frontend-builder, backend-api-builder, coding-teacher, study-coach, business-planner, health-info-guide, research-writer, career-builder, data-analyst, repo-polish. If a fetch fails, report it and continue with the others.

## Chat install with propose_skills

- Send the complete SKILL.md text for each skill, not a summary.
- If the skill has a `references/` file, fold its content into the end of the SKILL.md under a heading `## Reference`, since a chat skill save only keeps one file. Remove the line that points to the separate file.
- Three proposals per call. Install `skillhub` first.
- The user must tap save on each card. Do not say it is installed until they confirm or the tool reports it.

## Claude Code install

```
git clone https://github.com/dev-shubh-madara/madara-skillhub
cd madara-skillhub
python3 scripts/validate_skills.py
python3 scripts/install.py --all
```

Skills go to `~/.claude/skills/<name>/`. A new session picks them up.

## Fit questions (ask at most three)

1. What level are you at in this area: beginner, intermediate, advanced?
2. What do you mainly want help with right now?
3. Which tools, languages or subjects do you use?

## Verify after install

For each skill, give one prompt from `evals/triggers.json` under "should". If the user tries it and the skill does not seem to apply, check the skill is saved and enabled, then try the prompt again in a new chat.
