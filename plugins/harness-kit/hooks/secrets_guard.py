#!/usr/bin/env python3
"""harness-kit secrets guard (PreToolUse hook for Bash).

Blocks shell commands that would read, copy, stage or print secrets files:
.env and .env.* (except .env.example / .env.sample / .env.template),
.dev.vars, wp-config.php.

Allowed: existence checks and listings (ls, test, [ ], stat, find),
writing the file NAME somewhere (echo/printf, e.g. into .gitignore),
and git commands that don't show contents (ls-files, check-ignore, status, rm).

Exit 2 = block (stderr goes back to Claude). Exit 0 = allow.
If the input can't be parsed, the command is allowed: the permission
rules in settings.json still apply.
"""
import json
import re
import shlex
import sys

SECRET = re.compile(
    r"(?:^|[\s/'\"=<>(:@])"
    r"(\.env(?:\.[A-Za-z0-9_-]+)?|\.dev\.vars|wp-config\.php)"
    r"(?=$|[\s'\";|&)<>])"
)
SAFE_ENV_SUFFIXES = {".env.example", ".env.sample", ".env.template", ".env.dist"}

ALLOWED_FIRST = {"ls", "test", "[", "[[", "stat", "find", "echo", "printf", "touch", "mkdir", "which", "type"}
ALLOWED_GIT = {"ls-files", "check-ignore", "status", "rm", "mv"}
SKIP_PREFIX = {"sudo", "command", "builtin", "nice", "time", "env"}


def secret_names(text):
    found = []
    for m in SECRET.finditer(text):
        name = m.group(1)
        if name in SAFE_ENV_SUFFIXES:
            continue
        found.append(name)
    return found


def segments(command):
    # Split on command separators; a rough split is enough for a guard.
    return [s for s in re.split(r"\|\||&&|[;|\n]|\$\(|`", command) if s.strip()]


def first_word(seg):
    try:
        tokens = shlex.split(seg, posix=True)
    except ValueError:
        tokens = seg.split()
    tokens = [t for t in tokens if not re.match(r"^[A-Za-z_][A-Za-z0-9_]*=", t)]
    while tokens and tokens[0] in SKIP_PREFIX:
        tokens = tokens[1:]
    return tokens


def blocked_reason(command):
    for seg in segments(command):
        names = secret_names(seg)
        if not names:
            continue
        tokens = first_word(seg)
        if not tokens:
            continue
        head = tokens[0].rsplit("/", 1)[-1]
        if head in ALLOWED_FIRST and "<" not in seg:
            continue
        if head == "git":
            sub = next((t for t in tokens[1:] if not t.startswith("-")), "")
            if sub in ALLOWED_GIT:
                continue
        return names[0], seg.strip()
    return None


def main():
    try:
        data = json.load(sys.stdin)
        command = data.get("tool_input", {}).get("command", "")
    except Exception:
        return 0
    if not isinstance(command, str) or not command:
        return 0
    hit = blocked_reason(command)
    if not hit:
        return 0
    name, seg = hit
    sys.stderr.write(
        f"Blocked by the harness-kit secrets guard: `{seg}` would read, copy, stage or print {name}, "
        "which holds secrets. Don't retry another way. If a value from it is needed, ask the user to "
        "check it, or use .env.example for the variable names.\n"
    )
    return 2


if __name__ == "__main__":
    sys.exit(main())
