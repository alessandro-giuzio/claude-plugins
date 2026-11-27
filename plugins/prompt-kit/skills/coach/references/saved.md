# Saved prompts

Prompts read again and again: skills, agent files, CLAUDE.md, project instructions, scheduled-task prompts. Every line is paid for on every run, and nobody is there to clarify, so they need tighter rules than a chat message. If the `writing-for-agents` skill is available, apply it too; this file is the short version.

## All saved prompts

- Write instructions for the model, verb first: "Read `check.sh`", not "You should read the gate".
- Write the behaviour wanted. Reserve "never" for hard limits, and give the reason for any rule that isn't obvious.
- Keep the main file short. Move long detail, templates and examples into reference files the prompt points to.
- Cut lines that change nothing: if the model would do it anyway, delete it.
- Use the exact words the user types, so triggers and outputs match how the user talks.
- Test it on a real case before relying on it, and fix the prompt when the output misses.

## Skill descriptions

The description is always in context and decides when the skill loads.

- Third person, saying what the skill does, then "Use when…" with the phrases the user would actually type.
- Two to four lines. Manual-only skills (`disable-model-invocation: true`) can be one line, since only the user starts them.
- Fold or quote a description that contains ": ", or the YAML breaks.

Bad: `description: SEO stuff for pages`
Better: `description: Checks a page against my on-page and local SEO rules. Use when a page, layout or content file changes, or when asked to "check the SEO" or "is this page SEO-ready".`

## Agent files (subagents)

- Say what it checks, what it must not do (usually: edit nothing), and the exact reply format, verdict first.
- Limit its tools to what the job needs.
- Give examples in the description of when to call it.

## CLAUDE.md and project instructions

- A map and hard rules, not explanations: where things live, what must never happen, what "done" means.
- About 40 lines for one project. Point to deeper docs instead of copying them.
- One rule per line, each one checkable.

## Scheduled-task prompts

Each run starts fresh, with no memory of the chat that created it.

- Write it as a complete, standalone instruction: what to produce, from which sources, for whom.
- Say where the output goes (a file name pattern, an artifact, an email) and what to do when a source is empty or unreachable.
- Keep dates relative ("the past seven days"), never the creation date.

## Rule of thumb

If the user has corrected the same thing twice, the correction becomes one line in the saved prompt. If a line has never changed an output, remove it.
