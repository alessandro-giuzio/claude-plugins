---
name: blog-post
description: >
  This skill should be used when the user asks to "write the blog post",
  "write a post about", "draft this idea", "turn this brief idea into a
  post", pastes an idea from the Monday content brief, or runs /blog-post,
  in the repo of one of my Astro sites. It plans the post, waits for
  approval, then writes it as a draft entry in the site's content collection,
  in my voice, without committing or publishing.
metadata:
  version: "0.1.0"
---

# Blog post

Turn an idea (usually one of the three from the Monday content brief) into a finished draft in the site's Astro content collection.

Load the `writing-voice` skill first and use the site profile for this repo.

## 1. Read the blog before planning

- The collection schema: `src/content.config.ts` (or `src/content/config.ts`). Note the blog collection's folder, file format (`.md` or `.mdx`), required fields, the draft field (if any), the category field and its allowed values, image fields.
- Two or three recent posts: their frontmatter, length, heading style, components used in MDX, how internal links and images are written.
- All existing posts' titles, slugs and descriptions, to check the topic isn't covered. If it is, stop and suggest updating that post instead.
- Pages that exist (`src/pages`), for internal links.
- Details: `references/astro-collections.md`.

## 2. Plan and wait for approval

Show the plan:

- Title: Spanish, specific, max 60 characters (state the count). Slug.
- Target keyword and 2 to 3 secondary keywords, with the search intent.
- Category: one value the schema or site profile allows.
- Outline: H2/H3 structure, 5 to 8 sections, ending with a checklist or next step. When the brief gives a Search Console query, use its exact wording as an H2 or a FAQ question.
- Internal links: 1 to 3 existing URLs.
- Sources: the URLs behind every news fact.
- Meta description: 140 to 160 characters (state the count).

Don't write the post until the user approves or edits the plan.

## 3. Write

1. Check the branch: on `main` or `master`, suggest `post/<slug>` and wait for the answer.
2. Create the file in the collection folder, named by the slug. Never overwrite an existing file.
3. Frontmatter exactly as the schema requires. Set the draft field to true if the schema has one; if it doesn't, ask how drafts are kept out of the live site before writing.
4. Body in my voice: short paragraphs, the planned headings, source links on every fact, no invented numbers or quotes, a local angle where the profile asks for it, the closing checklist.
5. Images: don't download or generate any. Use the schema's image field with a clearly marked placeholder path and suggest what the image should show, with alt text.
6. If the site has the `web-seo` plugin, apply its `seo-checklist`, and use `schema-generator` only if the site already adds schema to posts.

## 4. Check

- Run `./check.sh` if it exists (an Astro build validates the frontmatter against the schema); otherwise `npx astro check` if installed.
- Recount title and meta description. Count words.
- Confirm every internal link points to an existing page or post.

## 5. Report

- File path, branch, word count, title and meta lengths, category.
- Internal links and sources used.
- Placeholders left (image), and anything that needs a fact check.
- Next steps: read the draft; in a new chat, "use the post-reviewer on <file>"; when published, `/promote` with the live URL.

Never commit, publish, or change the draft flag to false.
