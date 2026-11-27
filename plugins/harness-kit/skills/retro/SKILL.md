---
name: retro
description: >
  Retrospective on a Claude Code session. Proposes improvements to this repo's
  harness (check.sh, CLAUDE.md, settings, reviewer rules) and notes for my plugins.
disable-model-invocation: true
argument-hint: "Which session, or what went wrong?"
metadata:
  version: "0.6.1"
---

# Retro

Look back on a session and improve the agent's **environment**, so the next run goes better. The output is a ranked list of proposed changes, each with its evidence and a diff.

## 1. Read the session

- The current conversation, unless the user names another session. For an earlier one, read its transcript (Claude Code keeps them under `~/.claude/projects/`, one folder per repo).
- If the user passed an argument, start from what it says went wrong.
- Quote only what carries the signal, and redact every secret (`<REDACTED>`).

## 2. Read the harness

`CLAUDE.md`, `check.sh`, `.claude/settings.json`, `STATE.md`, the repo's own scripts (`package.json`, `composer.json`), CI config, and any reviewer agents in use (the harness-kit `verifier`, `seo-checker`, `wp-security-reviewer`).

## 3. Find candidates

Go through each category. Every candidate needs evidence from the session: a step that took too long, a mistake, a prompt, a missing fact.

- **Navigation.** The agent spent turns finding a file or a fact. → One pointer line in `CLAUDE.md` naming where it lives. `CLAUDE.md` holds the map and the hard rules, nothing else.
- **Gate.** The agent made a mistake a check could have caught. → A line in `check.sh`. Look at the repo's existing scripts first: a check that exists but isn't wired into the gate is the finding. A repo whose gate only builds is a finding too.
- **Mechanical vs judgement.** A mistake with a fixed pattern (a banned function, an import shape, a file in the wrong folder) gets a check: a lint rule, a gate line or a hook. A judgement call (consistency, "matches the surrounding code") gets a rule in `CLAUDE.md` for the reviewer to apply. Prefer the check.
- **Reviewer rules.** A reviewer missed a problem → a new or sharper rule. A reviewer blocked something it shouldn't have → a rule to clarify or remove (for example a rule that flagged problems older than the change).
- **Permissions.** Prompts that interrupted safe, repeated commands → `allow`. A risky command that ran without asking → `ask` or `deny`.
- **Lean CLAUDE.md.** Over about 40 lines (60 in a monorepo), lines the model follows anyway, stale lines, instructions that belong in a reviewer or a check.
- **Tool economy.** Expensive or repeated tool calls that a script, a narrower command or a pointer would save.
- **Information access.** A fact the agent needed and couldn't get: dev server logs, a read-only connection to a service, a doc.
- **Plugin gaps.** A problem that would happen in any repo, not just this one (a template line, a skill step, a reviewer rule) belongs in a plugin, not in this repo.

Done when every category has been checked against the session, and each candidate has evidence or was dropped.

## 4. Present

Order by severity: what caused a wrong result first, then what cost the most time.

For each candidate:

- category and one-line problem
- evidence: the quote or step from the session
- the proposed change as a diff, and the file it goes in

Then ask which to apply. Apply only the approved repo changes, show the result, and leave committing to the user.

For **plugin gaps**, end with a block ready to paste into the Harness Lab project:

```
Plugin: <harness-kit | web-seo | wordpress-kit | content-kit>
File: <path in the plugin>
Change: <what to change>
Evidence: <repo, session, what happened>
```

## Reference: why reviewers carry the rules

Work goes through two stages. The implementing agent carries the most context: exploring, writing, debugging. A reviewer gets a diff and little else. So standards belong with the reviewer and with checks, and `CLAUDE.md` stays short: the map, the hard rules, and pointers to the rest.

Adapted from Matt Pocock's `retro` skill (MIT). See THIRD-PARTY-NOTICES.md.
