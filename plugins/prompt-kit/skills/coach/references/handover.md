# Handovers

Briefs for another agent or a fresh chat: a verifier prompt, a subagent brief, a "continue this" note. The receiver starts with nothing, so the brief carries everything it needs and nothing it doesn't.

## What a brief needs

1. **The job in one line**, and whether the receiver may change things or only report.
2. **Where**: repo path, branch, files, URLs. Point to them; don't paste what it can read.
3. **The contract**: goal, scope, constraints and done-when, copied as agreed.
4. **What to check or do**, in order.
5. **What to leave alone**: files, commands, secrets, pushes.
6. **The reply format**: verdict or answer first, then evidence for each point, then what it couldn't verify.

## Pattern

```
<Check | Do> <the job> in <repo path>, on <branch | the uncommitted changes | the last commit>.
Read CLAUDE.md for the hard rules. <Edit nothing | Edit only <files>>. Never read .env files.

Goal: <outcome>
Scope: <files>
Constraints: <what must not change>
Done when:
- <checkable line>
- <checkable line>

For each done-when line and constraint, give concrete evidence (command output, file:line, an excerpt).
Compare "unchanged" claims against the last commit, not only the diff.
Start the reply with <ACCEPT or REJECT | the answer>. End with what you couldn't verify.
```

Good example (a real verifier handover): it named the branch, restated the contract, asked for evidence per line, told the verifier to compare against HEAD in a temporary directory, to check untracked files, and to say what it couldn't verify. The result was an ACCEPT with evidence and honest limits.

## Habits

- Ask for evidence, not opinions: "quote the output", "file and line".
- Ask it to look for reasons to reject; a reviewer told to approve will approve.
- Say what it can't do (write STATE.md, push) so it reports instead of trying.
- For "continue this tomorrow", use `/harness-kit:handoff`, which writes STATE.md in the right shape.
- If the receiver needs a skill, name it: "use the seo-checklist skill".
