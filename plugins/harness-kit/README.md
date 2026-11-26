# harness-kit

Sets up a Claude Code harness in a client repo, and checks work before it is called done.

## What's inside

| Component | Name | What it does |
|---|---|---|
| Skill | `harness-setup` | Writes `CLAUDE.md`, `check.sh` and `.claude/settings.json` for the repo's stack. Runs the gate to prove it passes. |
| Agent | `verifier` | Read-only reviewer. Runs `./check.sh`, checks the done-when lines, replies ACCEPT or REJECT. |

## Use

In a project root:

- `/harness-setup` or "set up the harness in this repo"
- "use the verifier on this change"

## Supported stacks

- Astro + Tailwind v4

Planned: Vue 3 + TypeScript, Laravel, WordPress plugin, WordPress site. Each one is a new file in `skills/harness-setup/references/`.

## What stays in the repo

The three generated files are committed per project. Project-specific skills (component conventions, release steps) also stay in that repo's `.claude/skills/`.

## Changelog

- 0.1.1: Checks the current branch before suggesting a new one. Detects Cloudflare (`wrangler.jsonc` / `wrangler.toml`) and repos with more than one deploy host.
- 0.1.0: First version. `harness-setup` for Astro, `verifier` agent.
