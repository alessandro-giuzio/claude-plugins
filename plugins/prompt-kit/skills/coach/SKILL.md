---
name: coach
description: >
  Rewrites a rough prompt so the first answer is usable, and says what changed.
  Use when asked to "improve this prompt", "rewrite my prompt", "write a prompt
  for", or "how should I ask Claude", including prompts for skills, CLAUDE.md,
  scheduled tasks and subagent briefs.
argument-hint: "the rough prompt"
metadata:
  version: "0.1.0"
---

# Prompt coach

Turn a rough prompt into one that gets a usable first answer, and show what changed so the user learns the habit, not just the fix.

## 1. Classify

Decide what the prompt is, then read only the matching reference:

- **Chat request**: sent once, in a chat or in Claude Code (a code task, a bug, writing or client work, research, a question) → `references/chat.md`
- **Saved prompt**: read again and again (a skill, CLAUDE.md, an agent file, project instructions, a scheduled-task prompt) → `references/saved.md`. If the `writing-for-agents` skill is available, apply it as well.
- **Handover**: a brief for another agent or a fresh chat, which starts with no context (a verifier prompt, a subagent brief, a "continue this" note) → `references/handover.md`

## 2. Find the gaps

Check the rough prompt for these parts:

1. **Goal**: the outcome someone would notice, not only the action
2. **Reason and audience**: why it matters and who it is for
3. **Material**: files, links, examples, data, or where to find them
4. **Done when**: how the user will judge the answer
5. **Constraints**: what must stay as it is, written as the behaviour wanted
6. **Output shape**: format, length, language, where it goes

Fill gaps from the conversation, the open repo and what is known about the user. Ask only about gaps that would change the result and can't be filled that way: at most three short questions, then wait. For smaller gaps, write a placeholder in angle brackets, such as `<client name>`, for the user to fill.

## 3. Rewrite

- Keep the user's language and voice. Scale to the task: a quick question stays one or two sentences; only a big task gets headings.
- Open with the goal and the reason in one sentence.
- Point to material by path or link when the receiver can open it; paste only what it can't reach.
- Write constraints as the behaviour wanted ("keep one h1"), without capitals, MUST or exclamation marks.
- Keep one task per prompt. If the rough prompt holds two, write two and say which to send first.
- For a big, risky or ambiguous task, end with "Ask me what's unclear before starting" or "Show me a plan first and wait for my ok".
- Use the reference's pattern as a starting shape. Drop any line that adds nothing for this task.

## 4. Reply

- The rewritten prompt in one code block, ready to copy.
- **What changed**: up to four bullets, each naming the habit and the change (for example "Reason added: the tagline is for first-time visitors").
- **Where to send it**, when it matters: a new chat, Claude Code in the repo, or a harness-kit skill that already does the job (`task-contract` for a code change bigger than one line, `/harness-kit:handoff` for a STATE.md).

Stop after the reply. The user decides whether to send the prompt.
