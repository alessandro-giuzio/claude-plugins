# wordpress-kit

Procedures for my custom WordPress plugins. The first one is `/release`: from a clean repo to a versioned, checked zip and a local tag, with every place the version lives kept in sync.

## Install

```
/plugin install wordpress-kit@agency-ga
```

## What's inside

| Component | Name | Type | Runs |
|---|---|---|---|
| Skill | `release` | Procedure | Only when you type `/release` (never on its own) |

## /release

1. **Checks the ground:** clean working tree, the branch it's cutting from, `./check.sh` passes. Asks which plugin if the repo has several.
2. **Reads the version** from every place it lives: plugin header, `*_VERSION` constant, `Stable tag` in readme.txt, `package.json` / `composer.json` / `block.json` when versioned, latest git tag. Any mismatch stops the release.
3. **Asks for the bump:** patch, minor, major or an exact version. Refuses a version that isn't higher or already exists as a tag.
4. **Drafts the changelog** from the commits since the last tag: user-facing entries only, in readme.txt format (and CHANGELOG.md if the repo has one). Waits for your ok.
5. **Bumps** every version place and shows the diff.
6. **Builds:** with the repo's own release script when there is one (for example `scripts/build-release.sh`). Without a script, it zips the plugin folder minus dev files, but only if no production dependencies or build step are needed; otherwise it stops and suggests adding a script.
7. **Checks the zip:** one top folder named after the slug, no dev files (`.git`, `.claude`, `CLAUDE.md`, `check.sh`, tests, `node_modules`, source maps, `.env*`), no paths from this machine, `php -l` on every PHP file, new version in the zipped header.
8. **Commits and tags after your yes:** `Release x.y.z` and an annotated tag `vx.y.z` with the changelog as its message. The zip is never committed.
9. **Reports** the version, commit, tag, zip path and size, and the push commands for you to run.

Never pushes. Never installs anything outside the repo's own release script.

## Rules

- `/release` is the only skill in my plugins allowed to commit, and only after approval.
- Out of scope for now: GitHub releases and WordPress.org SVN deploys.

## Changelog

- 0.1.0: First version. `release` skill.
