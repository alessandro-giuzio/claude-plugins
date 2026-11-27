# content-kit

Writing for my sites. The Monday content brief (a scheduled task) researches the week and proposes three blog ideas; this plugin takes the chosen idea the rest of the way: a draft in the site's Astro content collection, a review, then the Google Business Profile and LinkedIn posts once it's live.

## Install

```
/plugin install content-kit@agency-ga
```

## What's inside

| Component | Name | Type | Runs |
|---|---|---|---|
| Skill | `writing-voice` | Knowledge | Whenever text is written for one of my sites or channels |
| Skill | `blog-post` | Procedure | "write the blog post for this idea", or `/blog-post`, in a site repo |
| Skill | `promote` | Procedure | "promote this post", or `/promote <url>`, after publishing |
| Agent | `post-reviewer` | Read-only reviewer | "use the post-reviewer on <file>", before publishing |

## writing-voice

My Spanish voice (Spain Spanish, "tú" to the reader, "yo" never "nosotros", direct, practical, slightly witty, no buzzwords, never invented facts) and one profile per site with its audience, goal, blog categories, link targets and channel rules.

Profiles: `agencyga.md` (agencyga.es). Planned: `giuz.md`, when giuz.io publishes its first note.

## blog-post

1. **Reads the blog:** the collection schema (`src/content.config.ts`), recent posts, existing topics (stops and suggests an update if the intent is already covered), existing pages for internal links.
2. **Plans and waits:** title (max 60, counted), slug, keywords, category from the allowed set, H2/H3 outline (Search Console query wording as an H2 or FAQ when the brief has one), internal links, sources, meta description (140 to 160, counted).
3. **Writes** after approval: on a `post/<slug>` branch, a new file with frontmatter matching the schema and the draft flag on, the body in my voice with source links, a placeholder image with suggested alt text.
4. **Checks:** `./check.sh` or `astro check`, lengths, internal links.
5. **Reports** and suggests the reviewer, then `/promote` after publishing.

Never commits, publishes or turns the draft flag off.

## promote

For a published post: a Google Business Profile post (max ~1,200 characters, no phone, no hashtags, "Más información" button), LinkedIn post A promoting it (hook first, 3 to 5 hashtags, max ~1,300), and LinkedIn post B (a take on a news link) when you give one. Every post with its character count. Publishes nothing.

## post-reviewer

Read-only check of a draft: every fact sourced and the source opened, nothing invented, voice rules, lengths, frontmatter and category against the schema, links, duplicates. Reply: `READY` or `CHANGES: <n>`, then evidence per check.

## Changelog

- 0.1.0: First version. `writing-voice` (agencyga.es profile), `blog-post`, `promote`, `post-reviewer`.
