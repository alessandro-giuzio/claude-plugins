---
name: harness-setup
description: >
  This skill should be used when the user asks to "set up the harness",
  "add the harness kit", "add CLAUDE.md and check.sh", "prepare this repo
  for Claude Code", or runs /harness-setup in a project. It writes a short
  CLAUDE.md, a check.sh gate and .claude/settings.json permissions, matched
  to the project's stack. Version 0.1.0 supports Astro + Tailwind v4 only.
metadata:
  version: "0.1.4"
---

# Harness setup

Install three files in the current repo so that every Claude Code session knows where things live, what counts as done, and what it must never touch:

- `CLAUDE.md`: the map and the hard rules
- `check.sh`: the only definition of done
- `.claude/settings.json`: what runs freely, what asks first, what is blocked

## 1. Confirm the ground

1. Confirm the working directory is the project root (it contains `package.json`).
2. Detect the stack. Look for `astro` in `package.json` dependencies or an `astro.config.*` file.
3. If the project is not Astro, stop. Say that this version supports Astro only and name the stack that was found. Do not improvise templates for another stack.
4. Run `git status`. If the tree is dirty, ask the user to commit or stash first.
5. Run `git branch --show-current`.
   - On `main` or `master` with existing history: suggest a branch, `git switch -c add-claude-harness`, and wait for the answer.
   - On any other branch: say which branch the files will be written to and continue. Do not suggest a new branch.

## 2. Read the project before writing anything

Read `references/astro.md` for the templates. Then check what this repo really has, because the templates are a starting point and the repo is the truth:

- `package.json`: scripts, and whether `@astrojs/check`, `typescript` and `prettier` are installed
- Tailwind: v4 (CSS-first, `@theme` in a CSS file) or v3 (`tailwind.config.*` exists)
- Folders: which of `src/pages`, `src/layouts`, `src/components`, `src/styles`, `src/content` exist, and where the main CSS file is
- Deploy targets: `netlify.toml` (Netlify), `wrangler.jsonc` or `wrangler.toml` (Cloudflare), a `Dockerfile` (Coolify or Docker). A repo can have more than one; record every target found.
- Existing harness files: `CLAUDE.md`, `check.sh`, `.claude/settings.json`, `.claude/settings.local.json`
- `.gitignore`: whether it ignores every env file (`.env` and `.env.*`, except a committed `.env.example`)

## 3. Write CLAUDE.md

- Start from the template in `references/astro.md`.
- Replace every path with the real one. Delete lines for folders that do not exist, and never propose a line that points to a missing folder (for example the "Deeper docs: docs/" line when there is no `docs/`).
- Drop any hard rule that does not apply (for example the Tailwind v4 rule in a v3 project; write the v3 equivalent instead).
- Keep the file under about 40 lines.
- If `CLAUDE.md` already exists, do not overwrite it. Show the user what would be added or changed and ask before editing.

## 4. Write check.sh

- If `check.sh` already exists, do not edit it, not even a comment. Run it, report whether it passes, and propose any change as a diff for the user to approve.
- Otherwise, start from the gate in `references/astro.md`.
- Run each gate command by hand first. Put only the commands that pass into `check.sh`.
- Keep trial runs away from private files. Before running a command that scans the whole tree (such as `npx prettier --check .`), make sure it cannot read `.env*`, `.dev.vars` or `.claude/settings.local.json`: pass explicit paths, or check that a `.prettierignore` excludes them. If a command's output names one of those files anyway, do not open it, and say so in the report.
- For each command that fails or is not installed, leave it out and record why. Do not fix unrelated failures as part of setup.
- If the gate ends up with no type check (only a build), say so in the report and give the install command for the user to run, for example `npm i -D @astrojs/check typescript`, then the line to add to `check.sh`. Do not run the install.
- The last line is always `echo "GATE: PASS"`.
- Run `chmod +x check.sh`.

## 5. Write .claude/settings.json

- Start from the permissions in `references/astro.md`.
- Keep in `allow` only the commands that are in this repo's `check.sh`, plus `./check.sh` and `git commit`.
- Add the deploy rules for every target found in step 2, and only those. The rules per host are in `references/astro.md`.
- If `.claude/settings.json` already exists, merge: add missing rules, keep every existing rule, never remove a `deny` entry. Check the `deny` list against the template too, and propose any missing entry (for example the short `-f` form of force push).
- Cloudflare repos: add the `.dev.vars` deny rules from `references/astro.md`.
- Never read, edit or create `.claude/settings.local.json`.

## 6. Check .gitignore

- If `.gitignore` does not cover `.env.*` (only `.env`, or a list of named env files), propose adding `.env.*` and `!.env.example` as a diff. Do not edit `.gitignore` without approval.
- Cloudflare repos (step 2 found `wrangler.jsonc` or `wrangler.toml`): the proposal also covers `.wrangler/` (local Wrangler state) and `.dev.vars` (local secrets), if they are missing.
- Run `git ls-files '.env*'`. If an env file other than `.env.example` is already tracked, flag it at the top of the report: ignoring it now does not remove it from history.

## 7. Prove it

1. Run `./check.sh` and read the full output.
2. If it does not end with `GATE: PASS`, fix the harness files (not the project code) until it does, or remove the failing command and record it.

## 8. Report

Do not commit. End with a short report:

- First line: `harness-setup 0.1.4`, so the user can see which version ran
- The branch the files were written to
- The deploy targets detected
- The three files, and for each one: created, merged, or unchanged with proposed changes
- `.gitignore`: covers env files, or the proposed line
- The gate commands that are in `check.sh`
- Anything left out and why (a gate command that fails, a rule that did not apply)
- The `GATE: PASS` output, pasted
- One next step: review the diff, then commit the kit

## Rules for this skill

- Never read or edit `.env` or `.dev.vars` files while inspecting the project.
- Never push, deploy or install packages. If a gate tool is missing, report it and let the user decide.
- Never invent a path or a script name. Every path and command written into the harness files must exist in this repo.
