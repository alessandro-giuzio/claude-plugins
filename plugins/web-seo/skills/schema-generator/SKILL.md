---
name: schema-generator
description: >
  Write JSON-LD structured data into a client site page, following the site's
  existing schema pattern. Use when asked for schema, structured data,
  JSON-LD, rich results or a schema.org type, and when a page's structured
  data must match its changed content.
metadata:
  version: "0.1.1"
---

# Schema generator

Write complete, valid JSON-LD for a client site page and put it in the page, following the pattern the site already uses.

## 1. Gather the facts from the repo first

Look before asking:

- Existing structured data: search for `application/ld+json`, `@graph`, `schema.org`. Note the pattern (one `@graph` or separate blocks), the `@id` scheme, and the entities already defined (business, website, person).
- Business facts: site config files (for example `src/site.config.ts`, `src/data/*`), the footer and contact page for name, address, phone and hours, and existing `sameAs` links.
- The page itself: its canonical URL, title, description, and what it is about (service, FAQ, article).

Ask the user only for what the repo doesn't have. Every value the repo and the user can't supply becomes a visible placeholder such as `"YOUR_VALUE_HERE"`, listed in the report.

## 2. Choose the pattern

- The site already has structured data: follow it exactly (graph or blocks, `@id` scheme, where it is rendered). Reuse existing `@id`s for shared entities instead of redefining them.
- New site: one `@graph` per page, entities linked by `@id`.
- Separate blocks only if the user asks or the site already works that way.

## 3. Generate

Templates and type rules: `references/types.md`. In short:

- `@context` is `https://schema.org`. Use the most specific `@type` (`Plumber`, not `LocalBusiness`).
- Every entity gets an `@id`: canonical URL plus a fragment (`https://example.com/#business`, `https://example.com/servicios/fontaneria/#service`).
- Phone in international format (`+34…`, `+44…`); `addressCountry` as an ISO code (`ES`, `GB`); dates and hours in ISO 8601.
- `areaServed` uses typed places (`City`, `AdministrativeArea`), not plain strings.
- Every visible fact in the schema must match the page (name, address, phone, prices, FAQ text). Schema that says something the page doesn't is a problem, not an improvement.

## 4. Put it in the page

- Astro: render it in the layout's `<head>`, the way the site already does; otherwise `<script type="application/ld+json" set:html={JSON.stringify(schema)} />`, with the object built in the frontmatter.
- WordPress: output it from the site's own plugin or theme on `wp_head`, encoded with `wp_json_encode()`.
- Anywhere else: ask where it should go.
- Show the diff and leave committing to the user. If the user only wants the JSON, give it in the reply instead of editing.

## 5. Check and report

1. Parse the generated JSON (for example `node -e "JSON.parse(require('fs').readFileSync(0,'utf8'))"` on it) and fix any error.
2. Run the repo's `./check.sh` if it exists.
3. Report in a few lines: the types used and why, the `@id`s, any placeholders, and which rich results the page may be eligible for. Don't promise FAQ rich results: Google shows them only for a small set of authoritative sites.
4. End with: test the live page in Google's Rich Results Test (https://search.google.com/test/rich-results) and the Schema Markup Validator (https://validator.schema.org/).
