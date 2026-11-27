# harness-kit

Makes Claude Code safe and predictable in a repo. It answers three questions every session needs: **where do things live and what are the rules**, **what counts as done**, and **what must never happen**. Then it helps agree on "done" before a change and checks the work after it.

## Install

```
/plugin install harness-kit@agency-ga
```

## What's inside

| Component | Name | Type | Runs |
|---|---|---|---|
| Skill | `harness-setup` | Procedure | When you ask to set up the harness, or `/harness-kit:harness-setup` |
| Skill | `task-contract` | Procedure | Before a non-trivial change, or `/task-contract` |
| Agent | `verifier` | Read-only reviewer | When you ask for it after a change |
| Hook | secrets guard | Automatic | Before every shell command Claude runs, in every repo |

## harness-setup

Writes three files at the repo root, matched to the stack it finds:

| File | What it holds |
|---|---|
| `CLAUDE.md` | The map (where things live) and the hard rules for this stack, under about 40 lines (60 for a monorepo) |
| `check.sh` | The gate: the checks that must pass before anything is called done. Ends with `GATE: PASS` |
| `.claude/settings.json` | Permissions: what runs freely, what asks first (push, deploys, migrations), what is blocked (secrets, force push, destructive commands) |

What it does, in order:

1. Finds the repo root and every part of the repo (single project or monorepo). Checks the branch: on `main` it suggests a new branch first.
2. Reads the project before writing anything: scripts, installed check tools, folders, deploy targets (Netlify, Cloudflare, Coolify), existing harness files, `.gitignore`.
3. Writes `CLAUDE.md`, `check.sh` and `.claude/settings.json`. Only real paths and commands that exist in the repo. Only gate commands that pass when tried by hand.
4. Checks `.gitignore` covers env files (and `.wrangler/`, `.dev.vars` for Cloudflare, `vendor/` for Composer).
5. Runs `./check.sh` to prove the gate passes.
6. Reports: version, branch, parts found, each file created / merged / unchanged, what was left out and why, with the install command where one would fix it.

What it never does:

- Overwrite an existing `CLAUDE.md`, `check.sh` or `.gitignore`: it proposes a diff instead. Existing `settings.json` is merged, never shrunk.
- Touch `.claude/settings.local.json`, `.env` or `.dev.vars` files.
- Install packages, commit or push.

Supported stacks:

| Stack | Reference | Gate (when the tools are installed) |
|---|---|---|
| Astro + Tailwind v4 (v3 handled) | `references/astro.md` | `astro check`, Prettier, `npm run build` |
| WordPress plugin, at the root or in a subfolder | `references/wordpress-plugin.md` | `php -l`, phpcs with WordPress Coding Standards |
| Monorepos with any of the above | (SKILL.md) | One block per part, each run from its folder |
| Parts without a reference (Vue package, PHP library) | (SKILL.md) | Only the test and build scripts they already have |

Planned: WordPress site, Vue 3 + TypeScript, Laravel.

Example:

```
set up the harness in this repo
```

## task-contract

Turns a request into a short contract before any code changes:

```
Goal: what is true afterwards, as an outcome someone would notice
Scope: files or folders expected to change
Constraints: what must not change
Done when:
- ./check.sh prints GATE: PASS
- 1 to 3 checks tied to the goal
Not verifiable here: what needs a manual check, with the steps
Needs approval: push, deploy, migrations
If blocked: stop, write what was tried to STATE.md
```

- Done-when lines name behaviour, not edits, and are written against the goal: a line that can pass while the goal fails is rejected.
- It waits for your "ok" before any code changes.
- When the work is done, it gives you a ready-to-paste prompt for the verifier.

Example:

```
write a task contract for this: the vCard download is missing the email and phone
```

## verifier

A second opinion from an agent that didn't write the change. Read-only: it never edits a file.

It checks, in order:

1. `./check.sh` passes.
2. Every done-when line has evidence, read against the goal.
3. No test was deleted, skipped or weakened.
4. Nothing outside the scope was touched.
5. Hard rules in `CLAUDE.md`: broken by the change → blocking; already broken before the change → listed as "Pre-existing", not blocking (unless the task names it).

Reply: `ACCEPT` or `REJECT: <reason>` on the first line, then every check with evidence, then "Pre-existing" and "Not verified" when they apply.

Example, in a new chat:

```
Use the verifier on the last commit (git show HEAD).
Goal: …
Done when:
- ./check.sh prints GATE: PASS
- …
```

## Secrets guard (hook)

Runs before every shell command Claude runs, in every repo where harness-kit is enabled. It blocks commands that would read, copy, stage, upload or print a secrets file:

- `.env` and `.env.*` (not `.env.example`, `.env.sample`, `.env.template`, `.env.dist`)
- `.dev.vars` (Cloudflare local secrets)
- `wp-config.php`

Blocked, for example: `cat .env`, `grep DB_ .env`, `source .env`, `cp .env …`, `git add .env`, `git show HEAD:.env`, `curl -F f=@.env …`, a Python or Node one-liner that opens `.env`.

Allowed: existence checks and listings (`ls`, `test -f`, `[ -f … ]`, `find`), writing the file *name* into `.gitignore` (`echo`, `printf`), and git commands that don't show contents (`git ls-files`, `git check-ignore`, `git status`, `git rm --cached`).

Why a hook: `Read(.env)` deny rules in settings stop Claude's file reader, but not a shell command that opens the same file. The hook covers that path.

Limits: it reads the command text, so it's a strong guardrail, not a sandbox. `git add -A` can still stage a secrets file that isn't in `.gitignore`, which is why harness-setup checks `.gitignore` too. It needs `python3`; if the input can't be parsed, the command is allowed and the settings rules still apply.

## Changelog

- 0.4.0: Secrets guard hook: blocks shell commands that read, copy, stage, upload or print `.env*`, `.dev.vars` or `wp-config.php`. Existence checks, `.gitignore` edits and safe git commands stay allowed.
- 0.3.0: New `task-contract` skill: goal, scope, constraints, done-when lines written against the goal, what needs a manual check, and a ready-to-paste verifier prompt at the end.
- 0.2.2: Verifier: rule breaks the change introduced are blocking; pre-existing ones in touched files are listed, not blocking. Reads done-when lines against the goal. Verdict on the first line, then every check with evidence. Can use `git show` to compare with the parent commit.
- 0.2.1: WordPress reference: `WPINC` guards count as direct-access guards; wording for repos with several plugins; compares `Requires PHP` with the local PHP; phpcs and `php -l` skip `node_modules/` and `build/`.
- 0.2.0: WordPress plugin stack. Monorepo support: finds each part, builds one gate that runs every part's checks from its folder, and groups the CLAUDE.md rules by part. Reports missing dependencies and check tools with the install command.
- 0.1.4: Report opens with the skill version. Recommends the install command for `@astrojs/check` when the gate has no type check. Cloudflare repos get `.wrangler/` and `.dev.vars` in the `.gitignore` proposal and deny rules for `.dev.vars`.
- 0.1.3: Blocks `git push -f` as well as `--force`, and proposes it for existing settings. Checks that `.gitignore` covers `.env.*` and flags env files already tracked.
- 0.1.2: Never edits an existing `check.sh`; proposes a diff instead. Trial gate commands stay away from `.env*` and `.claude/settings.local.json`. No proposed lines for missing folders. Astro template no longer mentions migrations.
- 0.1.1: Checks the current branch before suggesting a new one. Detects Cloudflare (`wrangler.jsonc` / `wrangler.toml`) and repos with more than one deploy host.
- 0.1.0: First version. `harness-setup` for Astro, `verifier` agent.
