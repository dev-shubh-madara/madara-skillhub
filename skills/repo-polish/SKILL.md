---
name: repo-polish
description: Cleans up a GitHub repository so it looks professional and is easy to use: README, structure, setup steps, license, screenshots and issue hygiene. Use when the user wants a better README, a repo that attracts stars, or help getting a project ready to share.
---

# Repo polish

## Before you start

Read the repo first: the files, the entry point, how it runs. Do not write a README for code you have not looked at.

## Workflow

1. **Understand it.** What problem it solves, who uses it, how to run it, what is missing.
2. **README.** In this order: name and one-line purpose, a short demo (screenshot, GIF or sample output), install steps that really work, a usage example, configuration, limits, and license. Keep the voice plain and personal, written the way the author would explain it to a friend.
3. **Run the install steps** from a clean folder. Fix the README or the repo until they work.
4. **Structure.** Sensible folders, a `.gitignore`, an `.env.example` for any config, no secrets or junk files committed.
5. **Basics.** License file, a short contributing note if you want contributors, and clear names for files and functions.
6. **Check history for secrets.** If a key was ever committed, tell the user to rotate it. Deleting the file is not enough.
7. **Releases and topics.** Suggest GitHub topics, a short description, and a first tagged release.

## Quality bar

- A stranger can run the project in under five minutes from the README alone.
- No claims in the README that the code does not support.
- No placeholder text left behind.
- Commits are authored by the repo owner, with the author details the user gives you.

## Avoid

- Badge walls and emoji clutter that hide the content.
- Marketing language: "powerful", "seamless", "cutting-edge". Say what it does.
- Copying another project's README structure line for line.
- Adding notes or credits that the owner did not ask for.
