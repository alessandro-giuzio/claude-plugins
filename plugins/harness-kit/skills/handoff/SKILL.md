---
name: handoff
description: >
  Write STATE.md so a fresh session can pick up this work: where it stands,
  decisions, open risks, the next action, and which skills to load.
disable-model-invocation: true
argument-hint: "What will the next session focus on?"
metadata:
  version: "0.6.2"
---

# Handoff

Capture the state of the current work in `STATE.md` at the repo root, so the next session (started with "read STATE.md and continue") picks up exactly where this one stopped.

## 1. Gather

- The conversation: the goal, the task contract if there was one, what was tried, what worked, what didn't.
- `git branch --show-current`, `git status --short`, and `git log --oneline -10`.
- The existing `STATE.md`, if any: its decisions carry over.
- If the user passed an argument, it says what the next session will focus on: shape the next action and suggested skills around it.

## 2. Draft

Use this shape. Point to what already exists (commits, branches, the contract, docs, issues) by hash, path or URL instead of copying it.

```markdown
# STATE.md

Updated: <YYYY-MM-DD> · Branch: <branch>

## Goal
<one or two lines; the task contract's goal if there was one>

## Where it stands
Step <n> of <m>: <what that step is>
Done: <short list, each pointing to its commit or file>

## Decisions
- <decision>. <reason>.

## Open risks
- <what is untested, uncertain or fragile>

## Next action
<the exact next command or edit>

## Suggested skills
- <skill>: <why the next session needs it>

## References
- <commits, contract, docs, issue links>
```

Rules for the content:

- Decisions keep their reason, so the next session doesn't reopen them. Carry over decisions from an existing `STATE.md` that still hold; drop ones that were reversed and say so.
- "Next action" is concrete enough to run without rereading the conversation.
- Suggested skills name real skills available in this setup (for example `task-contract`, the `verifier` agent, `web-seo:seo-checklist`, `wp-security-reviewer`).
- Record only what this session saw. Reviews often run in another chat: if the verifier's verdict isn't in this conversation, write "Verifier: not run in this session (paste the verdict if it ran elsewhere)" under Open risks, and don't make "run the verifier" the next action on that basis alone.
- Replace every secret, token, password and personal detail with `<REDACTED>`.
- Keep it under about 60 lines.

## 3. Write

- No `STATE.md` yet: create it.
- `STATE.md` exists: show the diff and write after the user's ok.
- Leave committing to the user. Mention whether the repo tracks `STATE.md` in git or ignores it, so they can choose.

Adapted from Matt Pocock's `handoff` skill (MIT). See THIRD-PARTY-NOTICES.md.
