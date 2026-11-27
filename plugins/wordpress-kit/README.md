# wordpress-kit

Procedures for my custom WordPress plugins.

## Install

```
/plugin install wordpress-kit@agency-ga
```

## What's inside

| Component | Name | What it does |
|---|---|---|
| Skill | `release` | Runs only on `/release`. Checks the tree and gate, reads the version from every place it lives, asks for the bump, drafts the changelog, bumps, builds (with the repo's own release script when there is one), checks the zip, then commits `Release x.y.z` and tags `vx.y.z` after approval. Never pushes. |

## Rules

- `/release` is the only skill in my plugins allowed to commit: it commits and tags after I approve the final diff. Every other skill never commits.
- It runs the repo's own release script, including installs inside its staging folder. Without a script it installs nothing.
- Out of scope for now: GitHub releases and WordPress.org SVN deploys.

## Changelog

- 0.1.0: First version. `release` skill.
