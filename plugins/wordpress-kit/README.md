# wordpress-kit

Procedures for my custom WordPress plugins: `/wordpress-kit:release` takes a clean repo to a versioned, checked zip and a local tag; `wp-security-reviewer` checks changed PHP for the security mistakes that matter in WordPress.

## Install

```
/plugin install wordpress-kit@agency-ga
```

## What's inside

| Component | Name | Type | Runs |
|---|---|---|---|
| Skill | `release` | Procedure | Only when you type `/wordpress-kit:release` (never on its own) |
| Agent | `wp-security-reviewer` | Read-only reviewer | When you ask for a security review, or before a release |

## /wordpress-kit:release

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

## wp-security-reviewer

Read-only review of changed plugin or theme PHP (or the changes since the last tag, before a release). It follows each value from where it comes in to where it goes out, and checks:

| # | Check | Looks for |
|---|---|---|
| 1 | Output escaping | `esc_html()`, `esc_attr()`, `esc_url()`, `wp_json_encode()`, `wp_kses()` matched to the context |
| 2 | Input handling | `wp_unslash()` plus a sanitiser for the type, and an allow-list or range |
| 3 | Nonces | on every form and AJAX action that changes data |
| 4 | Capabilities | `current_user_can()` with the right capability; `nopriv` handlers that change data |
| 5 | REST routes | a real `permission_callback`, argument validation |
| 6 | SQL | `$wpdb->prepare()`, `esc_like()`, no table or column names from input |
| 7 | Redirects and URLs | `wp_safe_redirect()` + `exit`, the HTTP API for remote requests |
| 8 | Files | `wp_handle_upload()` with allowed types, safe paths, no includes from input |
| 9 | Dangerous functions | `eval`, `extract` on input, `unserialize` on user data, shell functions |
| 10 | Direct access | `ABSPATH` or `WPINC` guard in every PHP file |
| 11 | Data exposure | secrets in code, personal data in logs or responses |

Problems the change introduced block; problems already in untouched lines are listed as "Pre-existing". Reply: `SAFE` or `ISSUES: <n>`, then each problem with file, line, the risk in one sentence and the fix.

Example:

```
run the WordPress security review on this change
```

## Rules

- `/wordpress-kit:release` is the only skill in my plugins allowed to commit, and only after approval.
- Out of scope for now: GitHub releases and WordPress.org SVN deploys.

## Changelog

- 0.2.0: New `wp-security-reviewer` agent: read-only review of changed PHP against 11 WordPress security checks; introduced problems block, pre-existing ones are listed.
- 0.1.0: First version. `release` skill.
