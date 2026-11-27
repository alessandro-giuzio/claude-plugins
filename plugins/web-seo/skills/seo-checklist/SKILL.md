---
name: seo-checklist
description: >
  My on-page and local SEO rules, applied before a page change is done. Use
  when creating or editing a page, layout, template or content file on a
  client site, or when asked to check SEO, title and meta, local SEO or
  hreflang.
metadata:
  version: "0.1.1"
---

# SEO checklist

Apply these rules to every page you create or change. Before reporting the change as done, go through the list for each changed page and say which items fail. Fix what is in scope; list the rest.

## Every page

1. A unique `<title>`, about 50 to 60 characters, main keyword near the start.
2. A meta description, about 120 to 160 characters, written for the reader, not stuffed.
3. Exactly one `h1`, and headings that don't skip levels.
4. A canonical URL, matching the site's trailing-slash convention.
5. Structured data that matches the page type and the visible content (the `schema-generator` skill writes it).
6. Alt text on every meaningful image; `alt=""` on decorative ones. Width and height set, so the layout doesn't shift.
7. At least one internal link to the page and one from it, with descriptive anchor text (not "click here").
8. The right `lang` on `<html>` (`es`, `en-GB`). Multilingual sites: `hreflang` alternates for every language plus `x-default`.
9. Open Graph title, description and image for sharing.
10. Not accidentally hidden: no stray `noindex`, the page is in the sitemap, `robots.txt` doesn't block it.

## Local business pages

11. Name, address and phone (NAP) written exactly the same everywhere on the site and in the schema.
12. The town or service area named in the title, the `h1` and the first paragraph.
13. A clickable phone link (`tel:`) and the address as text, not only inside an image or a map.
14. One page per main service, each with its own title, `h1` and `Service` schema; no near-duplicate pages per town.

## How to report

For each changed page, a short list: item number, pass or fail, and the fix for each fail. Don't rewrite page copy to hit a length target without the user's say-so; propose the new text instead.
