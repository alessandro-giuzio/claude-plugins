# claude-plugins

Private marketplace `agency-ga`: my own Claude Code plugins.

## Install

```
/plugin marketplace add alessandro-giuzio/claude-plugins
/plugin install harness-kit@agency-ga
/plugin install web-seo@agency-ga
```

Update after a new version is pushed:

```
/plugin marketplace update agency-ga
```

## Plugins

| Plugin | Version | What it does |
|---|---|---|
| [harness-kit](plugins/harness-kit) | 0.3.0 | Harness setup (Astro, WordPress plugins, monorepos), task contracts, verifier agent |
| [web-seo](plugins/web-seo) | 0.1.0 | Schema generator, SEO checklist, SEO checker agent (Astro and WordPress client sites) |

## Working on a plugin

1. Edit it in `plugins/<name>/`.
2. Test without installing: `claude --plugin-dir ./plugins/<name>` from a test repo on a branch.
3. Validate: `claude plugin validate ./plugins/<name>`.
4. Bump the version in the plugin's `plugin.json` and in `.claude-plugin/marketplace.json`, and add a changelog line to the plugin's README.
5. Commit and push.

## Global settings

`settings/` holds my baseline ask and deny rules for `~/.claude/settings.json`, with install steps. See [settings/README.md](settings/README.md).
