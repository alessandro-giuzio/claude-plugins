# Where a WordPress plugin's version lives

| Place | Example | Find it with |
|---|---|---|
| Plugin header | ` * Version:           1.0.0` | `grep -n "^\s*\*\s*Version:" <main-file>.php` |
| Version constant | `define( 'HITZORDU_VERSION', '1.0.0' );` | `grep -n "_VERSION'" <main-file>.php` |
| readme stable tag | `Stable tag: 1.0.0` | `grep -n "^Stable tag:" readme.txt README.txt` |
| package.json | `"version": "1.0.0"` | only if the plugin folder has one |
| composer.json | `"version": "1.0.0"` | rarely set; only if present |
| Block metadata | `"version": "1.0.0"` in `block.json` | only if blocks carry a version |
| Latest tag | `v1.0.0` | `git describe --tags --abbrev=0` |

Notes:

- `Stable tag` must equal the plugin header version for WordPress.org; keep them equal in every release, even for plugins not on WordPress.org.
- A release script may already check header against constant (hitzordu's does). Keep the skill's own check anyway: it runs before anything is changed.
- `block.json` versions are cache-busters for block assets. Bump them only if they currently match the plugin version.
