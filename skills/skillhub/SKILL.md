---
name: skillhub
description: "Installs and fits the skills from the Madara SkillHub repo. Use when the user shares the madara-skillhub repo link, or says install all skills, add these skills, set up my skills, or list the available skill packs."
---

# SkillHub installer

This skill installs the other skills in this repo into the user's Claude and fits them to the person.

## When to use

- The user sends the repo link and says "install all skills" or similar.
- The user asks which skill packs exist, or asks for one by topic ("install the frontend one").
- The user wants to remove or update an installed pack.

## Procedure

1. **Find the repo contents.** With a shell, clone the repo. Without one, fetch `INSTALL.md` and each `skills/<name>/SKILL.md` from the repo page. Do not guess file contents.
2. **List the packs.** Read each `SKILL.md` frontmatter and show a short table: name, one line on what it does.
3. **Pick what to install.**
   - "all" means every pack in `skills/` except `skillhub` itself, which is installed first and always.
   - A topic means the matching packs only. If a topic matches nothing, say so, do not substitute.
4. **Audit before install.** For each pack run `python3 scripts/audit_skill.py skills/<name>`. If there is no shell, read the pack and look for the same things by hand: scripts that download and run code, encoded blobs, requests to unknown hosts, reads of credentials or `.env` files. A pack that fails is skipped and reported.
5. **Fit (only if the user did not say "just install").** Ask at most three short questions: their level, their main goal, and their stack or field. Save the answers as a short profile (template below). Packs read it to set depth and examples.
6. **Install.**
   - Shell available: `python3 scripts/install.py --all` or `--only a,b`. Use `--dry-run` first if the user is unsure.
   - Chat with a skill-saving tool (such as `propose_skills`): send each pack's name, description and complete `SKILL.md`. Three per call.
   - Chat without one: say plainly that you can't save skills here. Give the ZIP download links from the repo's `dist/` folder and the upload steps: **Customize > Skills**, **+**, **Create skill**, **Upload a skill**. Code execution must be on in **Settings > Capabilities**.
7. **Verify.** For each installed pack, give the user one example prompt that should trigger it. Check `evals/triggers.json` for the prompts that should and should not trigger it.
8. **Report.** Installed, skipped (with reason), and the profile if one was made. Keep it short.

## Profile template

```
# Skill profile
Level: beginner | intermediate | advanced
Goal: what they want the packs to help with
Stack or field: languages, tools, or subject
Language for replies: English unless they say otherwise
```

In Claude Code, put it in the project `CLAUDE.md`. In chat, give it to the user to keep in their Claude preferences.

## Updating and removing

- Update: re-run the install for that pack. Show what changed in the description or workflow if you can.
- Remove: with a shell, delete the folder from `~/.claude/skills/`. In chat, tell the user to remove it from their skills settings, since you cannot do it for them.

## Rules

- Install only what is inside `skills/` of this repo.
- Never claim a pack is installed until the install step actually succeeded.
- Never hide a failed audit. Say which pack failed and what was found.
- Do not promise a fixed speedup. Say what the pack changes about how Claude works, and let the user judge the results.

## Reference

Read `references/install-details.md` when fetching files without a shell, installing in chat, or verifying after install. It has the checklists, templates and worked examples for this skill.

## Self-check before replying

Run through these before you send the answer. Fix anything that fails.

- Did each install step actually succeed before I reported it as installed?
- Did every skill pass the audit, and did I report any that did not?
- Did I give one test prompt per installed skill?
- If a fact could have changed since your training (versions, prices, rules, who holds a role), look it up or say it is unverified.
