# Building and checking the zip without a release script

Only for plugins that need no build and no production dependencies. Run from the repo root. `<slug>` is the plugin folder name, `<plugin>` its path.

## Build

```bash
mkdir -p dist
VERSION=<new-version>
STAGE=$(mktemp -d)
rsync -a \
  --exclude '.git' --exclude '.github' --exclude '.claude' \
  --exclude 'CLAUDE.md' --exclude 'STATE.md' --exclude 'check.sh' \
  --exclude 'node_modules' --exclude 'tests' --exclude 'phpunit.xml*' \
  --exclude '.phpcs.xml*' --exclude 'phpcs.xml*' --exclude '*.map' \
  --exclude '.env*' --exclude '.DS_Store' --exclude 'dist' \
  --exclude 'composer.lock' --exclude 'package-lock.json' \
  <plugin>/ "$STAGE/<slug>/"
(cd "$STAGE" && zip -qr "$OLDPWD/dist/<slug>-$VERSION.zip" <slug>)
rm -rf "$STAGE"
```

If the plugin ships a `.distignore`, use it instead of the list above (`rsync --exclude-from=.distignore`).

## Check

```bash
ZIP=dist/<slug>-<new-version>.zip
unzip -l "$ZIP" | head -20                                   # one top folder, main file inside
unzip -l "$ZIP" | grep -E '\.git/|\.claude|CLAUDE\.md|STATE\.md|check\.sh|node_modules|/tests/|phpunit|phpcs|\.map$|\.env' && echo "DEV FILES FOUND"
CHECK=$(mktemp -d) && unzip -q "$ZIP" -d "$CHECK"
grep -rlF "$(git rev-parse --show-toplevel)" "$CHECK" && echo "MACHINE PATHS FOUND"
grep -rlF "$HOME" "$CHECK" && echo "HOME PATHS FOUND"
find "$CHECK" -name '*.php' -not -path '*/vendor/*' -print0 | xargs -0 -n1 php -l > /dev/null
grep -n "Version:" "$CHECK"/<slug>/<main-file>.php
rm -rf "$CHECK"
```

Any "FOUND" line or `php -l` error fails the release.
