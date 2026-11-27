---
name: task-contract
description: >
  This skill should be used when the user starts a non-trivial change in a
  repo ("fix", "add", "build", "refactor" something bigger than a one-line
  edit), asks to "write a task contract", "what's the done-when", "define
  done for this", or runs /task-contract. It turns the request into a goal,
  scope, constraints and done-when lines that the verifier agent can check,
  and waits for the user to confirm before any code changes.
metadata:
  version: "0.6.0"
---

# Task contract

Turn a request into a short contract before writing code, so "done" is agreed up front and the `verifier` agent has something concrete to check.

Skip it for trivial edits (a typo, a one-line config change) unless the user asks for one.

## 1. Read the ground rules

- `CLAUDE.md`: the hard rules and where things live.
- `check.sh`: what the gate runs. If there is no `check.sh`, say so: the contract can't use the gate, and suggest the `harness-setup` skill.
- `STATE.md`, if it exists: work already in progress that this task may continue or conflict with.
- Only the code needed to name the right files and functions. Don't start the change.

## 2. Draft the contract

Use exactly these headings:

```
Goal: <what is true afterwards, as an outcome a user or developer would notice, not the implementation>
Scope: <files or folders expected to change>
Constraints: <what must not change; any CLAUDE.md hard rule this task is likely to touch>
Done when:
- ./check.sh prints GATE: PASS
- <1 to 3 checks tied to the goal>
Not verifiable here: <what the gate and code reading can't prove, with the manual steps to check it>
Needs approval: push, deploy, migrations<, anything else specific to this task>
If blocked: stop, write what was tried to STATE.md, don't guess
```

Rules for the done-when lines:

- Each line must be checkable by running a command or reading the code, and name the behaviour, not the edit ("the vCard includes email and phone for a new profile", not "changed the meta keys").
- Write them against the goal. A line that can pass while the goal still fails is a bad line: if the goal is "the fields are filled", "the reader uses the right key names" isn't enough, because the fields also have to be saved.
- If a line depends on a running app (a browser, a WordPress install, a live API), move it to "Not verifiable here" with the manual steps.
- If the task should fix an old rule break in a file it touches, name it in a done-when line. Otherwise the verifier treats old breaks as pre-existing and doesn't block on them.

## 3. Confirm

Show the contract and ask the user to confirm or edit it. Don't change any code until they confirm. A short "ok" counts.

If the task will span more than one session, offer to copy the contract into `STATE.md`. Don't create or edit `STATE.md` without that yes.

## 4. After the work

When the change is finished and `./check.sh` passes, end with a ready-to-paste verifier prompt:

```
Use the verifier on <the uncommitted changes | the last commit (git show HEAD) | branch <name>>.
<the confirmed contract>
```

Suggest running it in a new chat, so the verifier has no memory of how the change was made.
