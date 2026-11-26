# claude-plugins

Private marketplace `agency-ga`: my own Claude Code plugins.

## Install

```
/plugin marketplace add alessandro-giuzio/claude-plugins
/plugin install harness-kit@agency-ga
```

Update after a new version is pushed:

```
/plugin marketplace update agency-ga
```

## Plugins

| Plugin | Version | What it does |
|---|---|---|
| [harness-kit](plugins/harness-kit) | 0.1.3 | Sets up CLAUDE.md, check.sh and permissions in a repo; verifier agent |

## Working on a plugin

1. Edit it in `plugins/<name>/`.
2. Test without installing: `claude --plugin-dir ./plugins/<name>` from a test repo on a branch.
3. Validate: `claude plugin validate ./plugins/<name>`.
4. Bump the version in the plugin's `plugin.json` and in `.claude-plugin/marketplace.json`, and add a changelog line to the plugin's README.
5. Commit and push.
