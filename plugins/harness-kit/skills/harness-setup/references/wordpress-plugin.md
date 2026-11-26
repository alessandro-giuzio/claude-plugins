# WordPress plugin templates

Starting points for a custom WordPress plugin, at the repo root or in a subfolder of a monorepo. Adjust every path and command to what the repo really has. `<plugin>` below is the plugin's folder (`.` when it is the repo root) and `<prefix>` its function and option prefix.

## What to look for

- The main plugin file: the PHP file with the `Plugin Name:` header. Read `Text Domain`, `Requires PHP` and any `define()` constants for the prefix.
- `composer.json`: autoloading (PSR-4 namespace), `path` repositories pointing to other parts of a monorepo, and `require-dev` tools.
- Check tools: `squizlabs/php_codesniffer` with `wp-coding-standards/wpcs`, `phpstan/phpstan` (with `szepeviktor/phpstan-wordpress`), `pestphp/pest` or `phpunit/phpunit`. Installed means listed in `require-dev` and present in `<plugin>/vendor/bin`.
- Folders: `src/` or `includes/` (classes), `admin/` or `src/Admin` (admin screens), `blocks/` (block editor), `public/` or `assets/` (front-end files), `languages/`, `uninstall.php`.
- Build output that is generated, not edited (for example `public/js/` when it is in `.gitignore`).

## CLAUDE.md

```markdown
# CLAUDE.md

## Stack
WordPress plugin <name> (PHP <version>), Composer autoloading (<Namespace>\)

## Where things live
- Plugin bootstrap: <plugin>/<main-file>.php
- Classes: <plugin>/src (PSR-4, <Namespace>\)
- Admin screens: <plugin>/src/Admin
- Blocks: <plugin>/blocks
- Generated, do not edit: <plugin>/public/js (built from <source part>)

## Hard rules
- Edit only inside this plugin. Never WordPress core, other plugins, themes or wp-config.php.
- Escape on output (esc_html, esc_attr, esc_url, wp_kses) and sanitize on input.
- Every form, AJAX handler and REST route checks a nonce or permission callback and a capability.
- Every query with variables goes through $wpdb->prepare().
- Every PHP file exits if ABSPATH is not defined.
- Prefix functions, hooks, options and constants with <prefix>.
- User-facing strings go through __() / _e() with the text domain <text-domain>.
- Never run WP-CLI against a live site. Local copy only.
- Never read or edit .env files.
- Never push, deploy or release without asking.

## How to work
- At session start, read STATE.md if it exists.
- Before coding, restate the task: goal, constraints, done when.
- Done means ./check.sh prints GATE: PASS. Paste the output.
- Same error twice: stop and write what you tried to STATE.md.
```

Notes:
- Delete the lines for folders that do not exist (no `blocks/`, no generated output).
- No `ABSPATH` guard in the existing files: keep the rule, and mention in the report that existing files do not follow it yet.
- Monorepo: this block becomes the plugin's group under "Hard rules", headed with its folder. The "How to work" section appears once for the whole repo.

## check.sh

Single plugin at the repo root:

```bash
#!/usr/bin/env bash
set -e
find . -name '*.php' -not -path './vendor/*' -print0 | xargs -0 -n1 php -l > /dev/null
./vendor/bin/phpcs --standard=WordPress --extensions=php --ignore=vendor/ .
echo "GATE: PASS"
```

Plugin in a monorepo subfolder:

```bash
# WordPress plugin
(cd <plugin> && find . -name '*.php' -not -path './vendor/*' -print0 | xargs -0 -n1 php -l > /dev/null)
(cd <plugin> && ./vendor/bin/phpcs --standard=WordPress --extensions=php --ignore=vendor/ .)
```

Notes:
- `php -l` needs only PHP, so it always belongs in the gate. It catches syntax errors, nothing more.
- phpcs needs `squizlabs/php_codesniffer` and `wp-coding-standards/wpcs` installed. If they are missing, leave the line out, and in the report give the install command (`composer require --dev wp-coding-standards/wpcs` in `<plugin>`) and the gate line above. A plugin that has never run phpcs will have many findings: say so, and recommend fixing them as their own task before adding the line.
- PHPStan or tests already set up for the plugin (`./vendor/bin/phpstan analyse`, `./vendor/bin/pest`, `composer test`): add them, after trying them by hand.
- If `<plugin>/vendor/` is missing, nothing that needs it can run: report `composer install` (in `<plugin>`).

## .claude/settings.json

```json
{
  "$schema": "https://json.schemastore.org/claude-code-settings.json",
  "permissions": {
    "allow": [
      "Bash(./check.sh)",
      "Bash(php -l *)",
      "Bash(./vendor/bin/phpcs *)",
      "Bash(./vendor/bin/phpcbf *)",
      "Bash(git commit *)"
    ],
    "ask": [
      "Bash(git push *)",
      "Bash(wp *)",
      "Bash(composer require *)",
      "Bash(composer update *)"
    ],
    "deny": [
      "Read(./.env)",
      "Read(./.env.*)",
      "Edit(./.env)",
      "Edit(./.env.*)",
      "Edit(**/wp-config.php)",
      "Read(**/wp-config.php)",
      "Bash(wp db reset *)",
      "Bash(wp db drop *)",
      "Bash(git push --force *)",
      "Bash(git push -f *)"
    ]
  }
}
```

Notes:
- Remove from `allow` any tool that is not installed. Add the commands of any PHPStan or test tool that is in the gate.
- Monorepo: commands run from a subfolder match as written, so allow the subshell form used in `check.sh` too, for example `"Bash((cd <plugin> && ./vendor/bin/phpcs *))"`, or simply rely on `"Bash(./check.sh)"`.
- `wp-config.php` is not normally in a plugin repo; the deny rules protect a local WordPress install the repo may sit inside.

## .gitignore

```
vendor/
node_modules/
*.zip
.env
.env.*
!.env.example
```

Plus any build output the plugin generates from another part (for example `<plugin>/public/js/`).
