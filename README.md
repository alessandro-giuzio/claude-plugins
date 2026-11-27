# claude-plugins

My Claude Code plugins, published as the private marketplace **`agency-ga`**. They hold the way I work on client sites (Astro, Vue, WordPress, Laravel) so that every Claude Code session follows the same rules without me repeating them.

## Install

In Claude Code, one command at a time:

```
/plugin marketplace add alessandro-giuzio/claude-plugins
/plugin install harness-kit@agency-ga
/plugin install web-seo@agency-ga
/plugin install wordpress-kit@agency-ga
/plugin install content-kit@agency-ga
```

Update after a new version is pushed:

```
/plugin marketplace update agency-ga
```

The repo is private, so the machine needs GitHub access (`gh auth login`).

## Plugins

| Plugin | Version | In one line |
|---|---|---|
| [harness-kit](plugins/harness-kit) | 0.6.1 | Sets up the rules, the definition of done and safe permissions in a repo; agrees what "done" means before a change; verifies the work after it; guards secrets files from shell commands |
| [web-seo](plugins/web-seo) | 0.1.1 | Writes JSON-LD schema into pages, applies my on-page and local SEO checklist, reviews changed pages |
| [wordpress-kit](plugins/wordpress-kit) | 0.2.0 | `/wordpress-kit:release` for my WordPress plugins (version bump, changelog, checked zip, local tag) and a WordPress security reviewer |
| [content-kit](plugins/content-kit) | 0.1.1 | My Spanish voice and site profiles, blog post drafts in an Astro content collection, GBP and LinkedIn posts, post reviewer |

#Slash commands are listed with the plugin prefix (`/harness-kit:retro`). Typing the short name (`/retro`) finds the same command in the autocomplete.

## How they fit together

A typical change on a client site:

1. **Once per repo:** `harness-kit` writes `CLAUDE.md`, `check.sh` and `.claude/settings.json`.
2. **Before the change:** `task-contract` (harness-kit) agrees the goal and the done-when lines.
3. **During the change:** `seo-checklist` (web-seo) loads when a page is edited; `schema-generator` adds structured data.
4. **After the change:** the `verifier` agent (harness-kit) checks the work against the contract; `seo-checker` (web-seo) reviews the changed pages.
5. **For WordPress plugins:** `wp-security-reviewer` on changed PHP, then `/wordpress-kit:release`.

For blog content: the Monday content brief (a scheduled task) proposes ideas → `blog-post` (content-kit) drafts the chosen one → `post-reviewer` checks it → publish → `promote` writes the GBP and LinkedIn posts.

## Shared rules

- Skills never overwrite existing files without approval: they merge, propose diffs and report.
- Skills never commit, push or install packages. One exception: wordpress-kit's `/wordpress-kit:release` commits and tags after approval, and never pushes.
- Every version change bumps `plugin.json`, `.claude-plugin/marketplace.json` and the plugin's changelog.

## Working on a plugin

1. Edit it in `plugins/<name>/`.
2. Test without installing: `claude --plugin-dir ./plugins/<name>`, from a test repo on a branch, in a new chat.
3. Validate: `claude plugin validate ./plugins/<name>` and `claude plugin validate .`
4. Bump the version in the plugin's `plugin.json` and in `.claude-plugin/marketplace.json`; add a changelog line to the plugin's README.
5. Commit and push. Machines pick it up with `/plugin marketplace update agency-ga` (or at startup with auto-update).

## Global settings

`settings/` holds my baseline ask and deny rules for `~/.claude/settings.json`, with install steps. See [settings/README.md](settings/README.md).
