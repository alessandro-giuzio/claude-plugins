# Baseline permissions

The `ask` and `deny` rules I want in every repo, including repos without a harness. They live in my user settings, `~/.claude/settings.json`, next to my own allow list, model, hooks and plugins.

This file is the versioned copy. The live copy is the one on each machine.

## What it does

- **Deny:** reading or editing `.env`, `.env.*` and `.dev.vars` anywhere; editing `wp-config.php`; force pushes; destructive database and Docker commands (`migrate:fresh`, `migrate:reset`, `db:wipe`, `supabase db reset`, `wp db drop` / `reset`, `docker volume rm`, `docker system prune`).
- **Ask:** `git push`, deploys (Netlify, Wrangler, Supabase), `php artisan migrate`, every `wp` command, `composer require`, `npm install`.

Project settings from harness-kit add to these. A deny anywhere wins.

## Install on a machine

1. Back up: `cp ~/.claude/settings.json ~/.claude/settings.backup.json`
2. Merge `baseline-permissions.json` into `~/.claude/settings.json`: add its `ask` and `deny` lists under `permissions`, keeping the existing `allow` list and every other key. Or ask Claude Code to do the merge and show the diff first.
3. Restart Claude Code and run `/permissions` to check the rules loaded.

## Limits

- Read/Edit deny rules stop Claude's file tools, not every shell command (`cat .env` is a Bash command). Keep production secrets off dev machines where possible.
- `Read(**/.env.*)` also blocks `.env.example`.

## Changelog

- 2026-11-26: first version, applied on my Mac. Allow list cleaned at the same time (one-off rules removed; `npm install` and `composer require` moved to ask; `python3 -c` and a `.env` grep removed).
