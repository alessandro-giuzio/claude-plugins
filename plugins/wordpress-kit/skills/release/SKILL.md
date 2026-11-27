---
name: release
description: >
  Cut a new release of one of my custom WordPress plugins: bump the version
  everywhere it appears, write the changelog, build and check the zip, then
  commit and tag locally after approval. Runs only when the user types
  /release.
disable-model-invocation: true
metadata:
  version: "0.2.0"
---

# Release a WordPress plugin

Turn the current state of a custom WordPress plugin into a versioned, checked zip and a local tag. Never push.

This skill is the one exception to the rule that skills never commit: it commits and tags, but only after the user approves the final diff. The exception applies to this skill only.

## 1. Check the ground

1. Run `git status`. If the tree is dirty, stop and ask the user to commit or stash first.
2. Run `git branch --show-current` and say which branch the release will be cut from. If it isn't `main` or `master`, ask whether that's intended.
3. If `./check.sh` exists, run it. If it doesn't end with `GATE: PASS`, stop and report.
4. Find the plugin: the PHP file with a `Plugin Name:` header. If the repo has more than one plugin, ask which one to release.

## 2. Read the current version

Collect every place the version lives (details in `references/version-sources.md`):

- the `Version:` line in the plugin header
- version constants in the main file (`define( '<PREFIX>_VERSION', '…' )`)
- `Stable tag:` in `readme.txt` (or `README.txt`)
- `"version"` in the plugin's `package.json` or `composer.json`, if present
- the latest tag (`git describe --tags --abbrev=0`), if any

If they don't all agree, stop. Show the table of places and values and ask the user which is right. Don't guess.

## 3. Ask for the new version

Show the current version and ask: patch, minor, major, or an exact version. Use semver. Refuse a version that is lower than or equal to the current one, or that already exists as a tag.

## 4. Draft the changelog

1. Read the commits since the last tag (`git log <last-tag>..HEAD --oneline`), or all commits if there is no tag.
2. Write user-facing entries only: what changed for site owners and visitors. Drop internal commits (refactors, CI, formatting, harness files) unless they change behaviour.
3. Use the readme's format:
   ```
   = 1.1.0 =
   * Added: …
   * Fixed: …
   ```
   New version on top, under `== Changelog ==`. If the repo also has a `CHANGELOG.md`, add the same entries there in its existing format.
4. Show the draft and wait for the user's ok or edits.

## 5. Bump

Update every place from step 2 to the new version. Don't touch `Requires at least`, `Tested up to` or `Requires PHP` unless the user asks. Show the full diff.

## 6. Build

- If the repo has a release script, run it: for example `scripts/build-release.sh`, a `release` or `build:zip` script in `composer.json` or `package.json`, or a `Makefile` target. It is the user's own procedure, so its installs inside a staging folder are fine.
- If there is no script and the plugin doesn't need production dependencies (no `require` beyond `php` in `composer.json`, no committed build step), build the zip as in `references/zip.md`.
- If there is no script but the plugin needs production dependencies or a build, stop. Don't install anything. Explain what's needed and suggest adding a release script to the repo.

## 7. Check the zip

All of these must pass (commands in `references/zip.md`):

- One top-level folder named after the plugin slug, with the main plugin file inside it.
- No dev files: `.git`, `.github`, `.claude`, `CLAUDE.md`, `STATE.md`, `check.sh`, `node_modules`, tests, `phpunit.xml`, `.phpcs.xml*`, source maps, `.env*`.
- No paths from this machine (grep for the repo's absolute path and the home folder).
- `php -l` passes on every PHP file in the zip, outside `vendor/`.
- The version in the zipped plugin header is the new version.

If a check fails, stop, report it, and don't commit.

## 8. Commit and tag (after approval)

1. Show a summary: new version, files changed, changelog entries, zip path and size, and the check results.
2. Ask for a yes. Without it, stop here and leave the changes uncommitted.
3. With a yes: commit only the version and changelog changes as `Release x.y.z`, then create an annotated tag `vx.y.z` with the changelog entries as its message. Never commit the zip or build output.
4. Never push.

## 9. Report

- The release: version, branch, commit and tag
- The zip: path and size
- The commands for the user to run when ready: `git push` and `git push origin vx.y.z`
