# Astro + Tailwind v4 templates

Starting points. Adjust every path and command to what the repo really has.

## CLAUDE.md

```markdown
# CLAUDE.md

## Stack
Astro + Tailwind v4 + TypeScript, deployed on <every host found: Netlify, Cloudflare, Coolify>

## Where things live
- Pages and layouts: src/pages, src/layouts
- Components: src/components
- Styles and design tokens: src/styles/global.css
- Content collections: src/content
- Deeper docs: docs/ (open only what the task needs)

## Hard rules
- Tailwind v4 is CSS-first: tokens live in @theme in the main CSS file. Do not create tailwind.config.js.
- Use theme tokens, not arbitrary values like text-[#1a2b3c], unless no token exists.
- Components ship no JavaScript by default. Add client:* only when interaction needs it.
- Every page keeps a unique title, a meta description, one h1, and its JSON-LD.
- Images go through astro:assets with alt text.
- Never read or edit .env files.
- Never push or deploy without asking.

## How to work
- At session start, read STATE.md if it exists.
- Before coding, restate the task: goal, constraints, done when.
- Done means ./check.sh prints GATE: PASS. Paste the output.
- Same error twice: stop and write what you tried to STATE.md.
```

Notes:
- Tailwind v3 project: replace the first hard rule with "Tokens live in tailwind.config.*. Extend the theme there; do not add arbitrary values."
- No `docs/` folder: delete the "Deeper docs" line, and do not propose it later.
- No JSON-LD on the site yet: keep the rule only if the user wants it enforced.

## check.sh

```bash
#!/usr/bin/env bash
set -e
npx astro check
npx prettier --check .
npm run build
echo "GATE: PASS"
```

Notes:
- `npx astro check` needs `@astrojs/check` and `typescript` installed. If they are missing, leave the line out, and in the report give the command to install them (`npm i -D @astrojs/check typescript`) and the line to add to `check.sh` afterwards.
- Before trying `npx prettier --check .`, check that a `.prettierignore` excludes `.env*` and `.claude/`. If there is none, run Prettier on `src/` only.
- `npx prettier --check .` only belongs here if `prettier` is a dependency and the repo already passes it. A repo that has never been formatted will fail on hundreds of files; leave it out and report it.
- If `package.json` has its own `check` or `lint` script, prefer `npm run <script>` over the raw command.

## .claude/settings.json

```json
{
  "$schema": "https://json.schemastore.org/claude-code-settings.json",
  "permissions": {
    "allow": [
      "Bash(./check.sh)",
      "Bash(npx astro check)",
      "Bash(npx prettier *)",
      "Bash(npm run build)",
      "Bash(git commit *)"
    ],
    "ask": [
      "Bash(git push *)"
    ],
    "deny": [
      "Read(./.env)",
      "Read(./.env.*)",
      "Edit(./.env)",
      "Edit(./.env.*)",
      "Bash(git push --force *)",
      "Bash(git push -f *)"
    ]
  }
}
```

Notes:
Deploy rules, added to `ask` for each host the repo deploys to:

| Host | Detected by | Add to `ask` |
|---|---|---|
| Netlify | `netlify.toml` | `"Bash(netlify deploy *)"`, `"Bash(npx netlify deploy *)"` |
| Cloudflare | `wrangler.jsonc` or `wrangler.toml` | `"Bash(wrangler deploy *)"`, `"Bash(npx wrangler deploy *)"` |
| Coolify | `Dockerfile` and no other target | nothing: a push to the deploy branch ships, and `git push` already asks |

- A repo with two hosts gets both sets of rules. When both are connected to the repo, one `git push` deploys twice; say so in `CLAUDE.md`.
- Cloudflare project: also add to `deny`: `"Read(./.dev.vars)"`, `"Edit(./.dev.vars)"`. `.dev.vars` holds local secrets for `wrangler dev`, like `.env`.
- Cloudflare Pages commands (`wrangler pages deploy`) are older; if the repo uses them, add `"Bash(wrangler pages deploy *)"` and `"Bash(npx wrangler pages deploy *)"` too.
- Remove from `allow` any command that is not in this repo's `check.sh`.

## .gitignore

Every Astro repo should ignore:

```
.env
.env.*
!.env.example
```

Cloudflare repos also need:

```
# Cloudflare
.wrangler/
.dev.vars
```
