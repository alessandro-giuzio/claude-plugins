# harness-kit

Sets up a Claude Code harness in a client repo, and checks work before it is called done.

## What's inside

| Component | Name | What it does |
|---|---|---|
| Skill | `harness-setup` | Writes `CLAUDE.md`, `check.sh` and `.claude/settings.json` for the repo's stack. Runs the gate to prove it passes. |
| Skill | `task-contract` | Turns a request into goal, scope, constraints and done-when lines before any code changes. Ends with a ready-to-paste verifier prompt. |
| Agent | `verifier` | Read-only reviewer. Runs `./check.sh`, checks the done-when lines, replies ACCEPT or REJECT. |

## Use

In a project root:

- `/harness-setup` or "set up the harness in this repo"
- "write a task contract for this" or `/task-contract`, before a change
- "use the verifier on this change", after it

## Supported stacks

- Astro + Tailwind v4 (`references/astro.md`)
- WordPress plugin, at the repo root or in a subfolder (`references/wordpress-plugin.md`)
- Monorepos containing any of the above. Parts without a reference (for example a Vue package or a plain PHP library) get their own existing test and build scripts in the gate.

Planned: WordPress site, Vue 3 + TypeScript, Laravel. Each one is a new file in `skills/harness-setup/references/`.

## What stays in the repo

The three generated files are committed per project. Project-specific skills (component conventions, release steps) also stay in that repo's `.claude/skills/`.

## Changelog

- 0.3.0: New `task-contract` skill: goal, scope, constraints, done-when lines written against the goal, what needs a manual check, and a ready-to-paste verifier prompt at the end.
- 0.2.2: Verifier: rule breaks the change introduced are blocking; pre-existing ones in touched files are listed, not blocking. Reads done-when lines against the goal. Verdict on the first line, then every check with evidence. Can use `git show` to compare with the parent commit.
- 0.2.1: WordPress reference: `WPINC` guards count as direct-access guards; wording for repos with several plugins; compares `Requires PHP` with the local PHP; phpcs and `php -l` skip `node_modules/` and `build/`.
- 0.2.0: WordPress plugin stack. Monorepo support: finds each part, builds one gate that runs every part's checks from its folder, and groups the CLAUDE.md rules by part. Reports missing dependencies and check tools with the install command.
- 0.1.4: Report opens with the skill version. Recommends the install command for `@astrojs/check` when the gate has no type check. Cloudflare repos get `.wrangler/` and `.dev.vars` in the `.gitignore` proposal and deny rules for `.dev.vars`.
- 0.1.3: Blocks `git push -f` as well as `--force`, and proposes it for existing settings. Checks that `.gitignore` covers `.env.*` and flags env files already tracked.
- 0.1.2: Never edits an existing `check.sh`; proposes a diff instead. Trial gate commands stay away from `.env*` and `.claude/settings.local.json`. No proposed lines for missing folders. Astro template no longer mentions migrations.
- 0.1.1: Checks the current branch before suggesting a new one. Detects Cloudflare (`wrangler.jsonc` / `wrangler.toml`) and repos with more than one deploy host.
- 0.1.0: First version. `harness-setup` for Astro, `verifier` agent.
