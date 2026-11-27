# web-seo

My SEO conventions for client sites, Astro and WordPress. Generic SEO tools tell you what is wrong; this plugin applies the way I build pages: schema that matches the page, the checks I run on every page, and the local SEO rules my small-business clients need.

## Install

```
/plugin install web-seo@agency-ga
```

## What's inside

| Component | Name | Type | Runs |
|---|---|---|---|
| Skill | `schema-generator` | Procedure | When you ask for schema / structured data / JSON-LD, or a schema.org type |
| Skill | `seo-checklist` | Knowledge | By itself, whenever a page, layout, template or content file is created or edited |
| Agent | `seo-checker` | Read-only reviewer | When you ask for it after a page change |

## schema-generator

Writes JSON-LD into the page and keeps it consistent with the rest of the site.

1. **Reads the repo first:** existing structured data (`application/ld+json`, `@graph`), site config, footer and contact page for name, address, phone and hours. Asks only for what's missing.
2. **Follows the site's pattern:** if the site already uses one `@graph`, it adds to it and reuses existing `@id`s (for example a `Person` shared between two sites). New sites get one `@graph` per page with entities linked by `@id`.
3. **Generates** with the most specific type (`Plumber`, not `LocalBusiness`), stable `@id`s, international phone numbers, ISO country codes and typed `areaServed`. Every fact must match the visible page.
4. **Puts it in the page:** Astro layout `<head>` (`set:html={JSON.stringify(schema)}`), or `wp_head` from my own plugin or theme with `wp_json_encode()`. Shows the diff.
5. **Checks** that the JSON parses, runs `./check.sh` if present, and reports types, `@id`s, placeholders and possible rich results.

Types covered (templates in `references/types.md`): LocalBusiness and subtypes, Service, FAQPage, WebSite, WebPage, Person, Organization.

Never: invents values (unknowns become visible placeholders, listed in the report), commits, edits WordPress core or third-party plugins, or promises FAQ rich results (Google shows them only for a few authoritative sites).

Example:

```
add LocalBusiness and Service schema to the boiler repair page
```

## seo-checklist

Applied to every page that is created or changed, before the change is called done.

| Every page | Local business pages |
|---|---|
| 1. Unique title, ~50–60 characters | 11. NAP identical everywhere, schema included |
| 2. Meta description, ~120–160 characters | 12. Town or area in title, h1 and first paragraph |
| 3. One h1, no skipped heading levels | 13. Clickable `tel:` link, address as text |
| 4. Canonical URL, trailing-slash convention | 14. One page per main service, no near-duplicate town pages |
| 5. Structured data matching the page | |
| 6. Alt text, image width and height | |
| 7. Internal links in and out, descriptive anchors | |
| 8. `lang`, and `hreflang` + `x-default` on multilingual sites | |
| 9. Open Graph title, description, image | |
| 10. Indexable: no stray `noindex`, in the sitemap, not blocked | |

It reports pass or fail per item and proposes new copy instead of rewriting it without asking.

## seo-checker

Read-only review of the pages in the current change (or the pages you name). Includes pages whose layout or shared components changed.

Reply: `PASS` or `ISSUES: <n>` on the first line, then one table per page (item, pass or fail, fix with file and line), then "Not verified" for anything that needs the live site.

Example:

```
run the SEO checker on what changed
```

## Notes

- Replaces my claude.ai account skill `schema-generator`. This plugin is the source of truth.
- New checklist rules get added as they come up in real client work.

## Changelog

- 0.1.0: First version. `schema-generator` (moved from my account skill, now writes into the page and follows the site's pattern), `seo-checklist`, `seo-checker` agent.
