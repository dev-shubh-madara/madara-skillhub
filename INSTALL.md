# Install instructions (for Claude)

A user has pointed you at this repo and asked you to install its skills. Do this, in order.

1. Read `skills/skillhub/SKILL.md`. It is the installer and it has the full procedure.
2. List the folders inside `skills/`. Each folder is one skill and each has a `SKILL.md`.
3. If the user said "all", install every skill in `skills/`. If they named topics, install only those.
4. Before installing, check every skill with `scripts/audit_skill.py` if you have a shell, or by reading it yourself if you do not. Skip and report any skill that fails.
5. Install:
   - With a shell (Claude Code): run `python3 scripts/install.py --all` (or `--only name1,name2`). It copies the skills into `~/.claude/skills/`.
   - In a Claude chat that has a skill-saving tool (such as `propose_skills`): call it with each skill's name, description and full `SKILL.md` text, three per call. Add the skill's `references/` file at the end under `## Reference`, since a chat skill keeps one file. The user taps save on each card. Details are in `skills/skillhub/references/install-details.md`.
6. Tell the user what was installed, what was skipped and why, and one example prompt for each installed skill.

Do not install anything that is not inside `skills/`. Do not edit the skills while installing unless the user asks for a personal fit (see the fit step in `skillhub`).

## If you cannot save skills in this chat

Many chats have no tool that saves skills. Do not pretend to install. Tell the user to:

1. Turn on **Code execution and file creation** in **Settings > Capabilities**.
2. Download the ZIPs from https://github.com/dev-shubh-madara/madara-skillhub/tree/main/dist
3. Go to **Customize > Skills**, tap **+**, **Create skill**, **Upload a skill**, and upload each ZIP.

Then list the skills with one line each, so they can pick which ZIPs they want.
