# prompt-kit

A prompt coach. Paste a rough prompt and it rewrites it so the first answer is usable, then tells you which habit each change applies, so you learn the pattern instead of depending on the coach.

## What's inside

| Type | Name | Kind | When it runs |
|---|---|---|---|
| Skill | `coach` | Procedure | "improve this prompt: …", "write a prompt for …", or `/prompt-kit:coach <prompt>` |

References (loaded only when needed):

- `references/chat.md`: patterns for prompts sent once: code change, bug, writing and client work, research, review, quick question. Each with a bad and a better example.
- `references/saved.md`: rules for prompts read every run: skills and their descriptions, agent files, CLAUDE.md, project instructions, scheduled-task prompts.
- `references/handover.md`: briefs for another agent or a fresh chat (verifier, subagent), with a pattern taken from a real verifier handover.

## How it works

1. **Classifies** the prompt: chat request, saved prompt, or handover.
2. **Finds the gaps** among six parts: goal, reason and audience, material, done when, constraints, output shape. It fills what it can from the chat and the repo, asks at most three questions when a gap would change the result, and leaves `<placeholders>` for the rest.
3. **Rewrites** it in your language and voice, scaled to the task: a quick question stays short.
4. **Replies** with the prompt in a copy-ready block, up to four "what changed" bullets, and where to send it. It doesn't send the prompt itself.

It hands off to skills that already do the job: a code change bigger than one line becomes a `task-contract` request (harness-kit), and a "continue tomorrow" note becomes `/harness-kit:handoff`. For saved prompts it also applies the `writing-for-agents` skill when that skill is installed.

## Install

```
/plugin install prompt-kit@agency-ga
```

## Changelog

- 0.1.0: First version: `coach` skill with chat, saved and handover references.
