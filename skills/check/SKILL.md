---
name: check
description: Audit the current Python project against romkey's Python AI coding rules and report or fix what doesn't comply.
argument-hint: "[fix]"
disable-model-invocation: true
---

Audit this repository against python-ai-rules. Arguments:
`$ARGUMENTS` (`fix` to apply fixes; otherwise only report).

1. Read `${CLAUDE_PLUGIN_ROOT}/RULES.md` and
   `${CLAUDE_PLUGIN_ROOT}/UPGRADING.md` in full, and compare against the
   files in `${CLAUDE_PLUGIN_ROOT}/templates/`. Find the rules version this
   repo follows in its AGENTS.md (missing means v0.0.0); every UPGRADING.md
   entry newer than that is a finding, most important first.
2. Check each section of RULES.md against this repo: layout, Python
   version in `.python-version`/`requires-python`/Dockerfile, uv and
   `uv.lock`, mypy strict and ruff settings, configuration from the
   environment (`docs/configuration.md` and `.env.example` complete and
   generated per §2), pip install instructions in the README,
   logging, entry point, tests and coverage, database choice, Dockerfile
   stages and the four compose files, `.gitignore`/`.dockerignore`,
   pre-commit, workflows (including stale action versions: look them up),
   Renovate, release setup, README order/badges/AI disclosure, CHANGELOG,
   docs/, AGENTS.md, LICENSE.
3. If this repo hasn't been set up with these rules before (no AGENTS.md
   pointing at them), ask the owner whether to use MIT or keep/choose
   another license before changing `LICENSE` (RULES.md §11).
4. If `gh` is available, check the GitHub side too: a "Protect main"
   ruleset requiring "CI passed" and "Lint"
   (`gh api repos/{owner}/{repo}/rulesets`), and secret scanning enabled
   (`gh api repos/{owner}/{repo} --jq .security_and_analysis`). Fixing
   these means running `scripts/setup-github.sh`, which changes repo
   settings: ask first.
5. If Docker is available, run
   `docker compose -f docker-compose.test.yaml run --rm test` and
   `docker compose -f docker-compose.lint.yaml run --rm lint`.
6. Report findings grouped by RULES.md section, most important first, each
   with the file and a one-line fix. Note anything that is deliberately
   different as fine, not a finding.
7. With `fix`: apply the fixes, re-run the tests and lint, update
   CHANGELOG.md under Unreleased, set the version line in AGENTS.md to
   `metadata.version` in `${CLAUDE_PLUGIN_ROOT}/SKILL.md`, and
   summarize. Ask before anything destructive or breaking, such as
   deleting files or renaming commands, options, environment variables or
   endpoints (RULES.md §9).
