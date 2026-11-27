---
name: harness-setup
description: >
  This skill should be used when the user asks to "set up the harness",
  "add the harness kit", "add CLAUDE.md and check.sh", "prepare this repo
  for Claude Code", or runs /harness-setup in a project. It writes a short
  CLAUDE.md, a check.sh gate and .claude/settings.json permissions, matched
  to the project's stack. Supports Astro + Tailwind v4, WordPress plugins,
  and monorepos that contain them.
metadata:
  version: "0.6.0"
---

# Harness setup

Install three files at the root of the current repo so that every Claude Code session knows where things live, what counts as done, and what it must never touch:

- `CLAUDE.md`: the map and the hard rules
- `check.sh`: the only definition of done
- `.claude/settings.json`: what runs freely, what asks first, what is blocked

## 1. Confirm the ground

1. Find the repo root with `git rev-parse --show-toplevel` and work from there. The harness files always go at the root, even in a monorepo.
2. Find the parts of the repo. A repo is a single project or a monorepo with several parts in subfolders. Look at the root and one or two levels down (for example `plugins/*`, `packages/*`, `apps/*`, `wp-content/plugins/*`):
   - **Astro**: `astro` in a `package.json`, or an `astro.config.*` file. Reference: `references/astro.md`.
   - **WordPress plugin**: a PHP file whose header contains `Plugin Name:`. Reference: `references/wordpress-plugin.md`.
   - **Other parts** (a Vue package, a plain PHP library, anything without a reference): note the folder and the test or build scripts its `package.json` or `composer.json` already defines.
3. If no part is Astro or a WordPress plugin, stop. Say which stacks are supported and which were found. Do not improvise templates for another stack.
4. Run `git status`. If the tree is dirty, ask the user to commit or stash first.
5. Run `git branch --show-current`.
   - On `main` or `master` with existing history: suggest a branch, `git switch -c add-claude-harness`, and wait for the answer.
   - On any other branch: say which branch the files will be written to and continue. Do not suggest a new branch.

## 2. Read the project before writing anything

Read the reference for every supported part found. Then check what this repo really has, because the templates are a starting point and the repo is the truth:

- For each part: its folder, its `package.json` or `composer.json` scripts, and which check tools are actually installed (look in `require-dev` / `devDependencies` and in `vendor/bin` / `node_modules/.bin`). The reference lists what to look for per stack.
- Folders inside each part that the reference mentions, and which of them exist.
- Deploy targets: `netlify.toml` (Netlify), `wrangler.jsonc` or `wrangler.toml` (Cloudflare), a `Dockerfile` (Coolify or Docker). A repo can have more than one; record every target found.
- Existing harness files: `CLAUDE.md`, `check.sh`, `.claude/settings.json`, `.claude/settings.local.json`
- `.gitignore`: whether it ignores every env file (`.env` and `.env.*`, except a committed `.env.example`), plus the stack-specific lines in each reference.

## 3. Write CLAUDE.md

- Start from the template in the reference. In a monorepo, start with a short "Parts" section (one line per part: folder and what it is), then the hard rules grouped by part, each group headed with its folder.
- Replace every path with the real one. Delete lines for folders that do not exist, and never propose a line that points to a missing folder (for example the "Deeper docs: docs/" line when there is no `docs/`).
- Drop any hard rule that does not apply, and write the right equivalent where one exists (for example the Tailwind v3 rule in a v3 project).
- Keep the file under about 40 lines for a single project, about 60 for a monorepo.
- If `CLAUDE.md` already exists, do not overwrite it. Show the user what would be added or changed and ask before editing.

## 4. Write check.sh

- If `check.sh` already exists, do not edit it, not even a comment. Run it, report whether it passes, and propose any change as a diff for the user to approve.
- Otherwise, start from the gate in each reference. In a monorepo, run each part's checks from its own folder in a subshell, for example `(cd packages/core && ./vendor/bin/pest)`, one block per part, with a comment naming the part.
- For parts without a reference, use only the test and build scripts that part already defines (for example `npm test`, `npm run build`, `composer test`). Never invent one.
- Run each gate command by hand first. Put only the commands that pass into `check.sh`.
- Keep trial runs away from private files. Before running a command that scans the whole tree (such as `npx prettier --check .`), make sure it cannot read `.env*`, `.dev.vars` or `.claude/settings.local.json`: pass explicit paths, or check that an ignore file excludes them. If a command's output names one of those files anyway, do not open it, and say so in the report.
- For each command that fails or is not installed, leave it out and record why. Do not fix unrelated failures as part of setup.
- If a part's dependencies are not installed (no `vendor/` or `node_modules/`), its checks cannot run: leave them out and give the user the install command (`composer install`, `npm install`) in the report.
- If a part has no static check (only a build, or only a lint), say so in the report and give the install command and the gate line from its reference. Do not run the install.
- The last line is always `echo "GATE: PASS"`.
- Run `chmod +x check.sh`.

## 5. Write .claude/settings.json

- Start from the permissions in the references. In a monorepo, combine them: one `allow`, one `ask` and one `deny` list, with no duplicates.
- Keep in `allow` only the commands that are in this repo's `check.sh` (written as Claude would run them, with the subshell form if used), plus `./check.sh` and `git commit`.
- Add the deploy rules for every target found in step 2, and only those. The rules per host are in `references/astro.md`.
- If `.claude/settings.json` already exists, merge: add missing rules, keep every existing rule, never remove a `deny` entry. Check the `deny` list against the templates too, and propose any missing entry (for example the short `-f` form of force push).
- Cloudflare repos: add the `.dev.vars` deny rules from `references/astro.md`.
- Never read, edit or create `.claude/settings.local.json`.

## 6. Check .gitignore

- If `.gitignore` does not cover `.env.*` (only `.env`, or a list of named env files), propose adding `.env.*` and `!.env.example` as a diff. Do not edit `.gitignore` without approval.
- Add to the same proposal any stack-specific line a reference lists and the repo is missing (for example `.wrangler/` and `.dev.vars` for Cloudflare, `vendor/` for Composer).
- Run `git ls-files '.env*'`. If an env file other than `.env.example` is already tracked, flag it at the top of the report: ignoring it now does not remove it from history.

## 7. Prove it

1. Run `./check.sh` and read the full output.
2. If it does not end with `GATE: PASS`, fix the harness files (not the project code) until it does, or remove the failing command and record it.

## 8. Report

Do not commit. End with a short report:

- First line: `harness-setup 0.6.0`, so the user can see which version ran
- The branch the files were written to
- The parts found (folder and stack) and the deploy targets detected
- The three files, and for each one: created, merged, or unchanged with proposed changes
- `.gitignore`: covers what it should, or the proposed lines
- The gate commands that are in `check.sh`, by part
- Anything left out and why (a gate command that fails, a tool that is not installed, a part without a reference, a rule that did not apply), with the install command where one fixes it
- The `GATE: PASS` output, pasted
- One next step: review the diff, then commit the kit

## Rules for this skill

- Never read or edit `.env` or `.dev.vars` files while inspecting the project, and never `wp-config.php`.
- Never push, deploy or install packages. If a gate tool or a dependency is missing, report it and let the user decide.
- Never invent a path or a script name. Every path and command written into the harness files must exist in this repo.
