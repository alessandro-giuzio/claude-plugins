# Chat requests

Prompts sent once, in a chat or in Claude Code. Pick the pattern that fits, then trim it. Each pattern is a shape, not a form.

## Code change (Claude Code, in the repo)

A change bigger than one line goes through harness-kit: rewrite it as a task-contract request, so goal, scope and done-when get agreed before any edit.

```
write a task contract for this: <outcome someone would notice>, because <reason>.
<anything Claude can't find in the repo: a design decision, a client request, a link>
```

A one-line change:

```
<the change>, in <file or component>. <reason, if it isn't obvious>.
```

Bad: `add a span after the h1`
Better: `write a task contract for this: visitors see one short sentence under the home page title, so they get the story before scrolling. Text: "Learning the craft on a small red roaster in Brighton."`
Why: the goal leaves the right element (`<p>`, not `<span>`) to Claude, and the contract adds scope and done-when.

## Bug

```
<what happened> when <steps>. Expected <what should happen>.
Error: <exact message, or "none">
Where: <page, file, environment (local, Netlify, Coolify)>
Already tried: <what, and what it changed>
Find the cause and show the evidence before changing code.
```

Bad: `the form doesn't work, fix it`
Better: `The contact form on /contacto returns a 500 on submit, locally and on Netlify. Expected the thank-you page. Error in the Netlify function log: "Missing RESEND_API_KEY". Already tried: redeploying. Find the cause and show the evidence before changing code.`

## Writing and client work

```
Write <what> for <who>, so that <the one thing they should do or understand>.
Material: <thread, notes, page, or a file to read>
Voice: <mine (my writing-voice skill) | formal | friendly>, in <language>. <length>.
Done when: <how you'll judge it, e.g. "under 120 words, one clear ask, no jargon">
```

For Spanish text on my own sites and channels, the content-kit `writing-voice` skill already holds the voice: say which site, and skip the voice line.

Bad: `write an email to the client about the delay`
Better: `Write an email to the client (a local plumbing company) explaining the service pages go live next Friday, not this one, because the photos arrived late. He should reply with yes or a question. Friendly, English, under 120 words. Done when it names the new date, gives the reason in one line and ends with one clear ask.`

## Research

```
I need to decide <decision>. Find out <question>.
Scope: <time range, region, kinds of sources, what to skip>
Give me: <a table, a short summary, a recommendation with trade-offs>, with sources.
Say what you couldn't verify.
```

Bad: `best headless CMS?`
Better: `I need to choose a CMS for a 20-page Astro client site the client edits weekly. Compare Decap, Keystatic and Sanity on cost, editing experience for a non-technical client, and Netlify fit. Current versions only. Give me a table plus a recommendation with trade-offs, with sources. Say what you couldn't verify.`

## Review or feedback

```
Review <the work> as <who: a client, a senior front-end dev, an SEO>.
Look for <what matters: bugs, clarity, accessibility, conversions>.
List problems ranked by impact, each with the fix. <Rewrite it | Don't rewrite it>.
```

## Quick question

One line of context is usually all it needs: stack, version, what is already ruled out.

Bad: `how do I do container queries`
Better: `In Tailwind v4 (CSS-first, no config file), how do I make a card switch to two columns when its container is wider than 32rem?`

## Habits behind every pattern

- The reason lets Claude make the small calls you didn't spell out.
- One real example beats a paragraph describing it.
- "Done when" is how you'll judge the answer; saying it up front gets the answer you'll accept.
- A fresh chat for each unrelated task: old context steers new answers.
- When an answer misses the same way twice, the fix belongs in a skill or CLAUDE.md, not in the next message.
