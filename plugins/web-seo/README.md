# web-seo

My SEO conventions for client sites, Astro and WordPress.

## What's inside

| Component | Name | What it does |
|---|---|---|
| Skill | `schema-generator` | Writes JSON-LD into the page, following the site's existing schema pattern (one `@graph` by default for new sites). Facts come from the repo; unknowns become visible placeholders. |
| Skill | `seo-checklist` | My on-page and local SEO rules. Loads when a page is created or edited, and is applied before a page change is called done. |
| Agent | `seo-checker` | Read-only review of changed pages against the checklist: pass or fail per item, with the fix. |

## Install

```
/plugin install web-seo@agency-ga
```

## Use

- "add LocalBusiness schema to the homepage", "add FAQ schema to this page"
- creating or editing a page loads the checklist by itself
- "run the SEO checker on what changed"

## Notes

- Replaces my claude.ai account skill `schema-generator`. This plugin is the source of truth; delete the account skill once the plugin is installed in the app too.
- Add new checklist rules as they come up in real client work.

## Changelog

- 0.1.0: First version. `schema-generator` (moved from my account skill, now writes into the page and follows the site's pattern), `seo-checklist`, `seo-checker` agent.
