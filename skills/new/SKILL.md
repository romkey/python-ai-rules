---
name: new
description: Scaffold a new Python application that follows romkey's Python AI coding rules.
argument-hint: "[repo-name]"
disable-model-invocation: true
---

Create a new Python application from the python-ai-rules templates.
Arguments: `$ARGUMENTS` (repo name; optional).

1. Read `${CLAUDE_PLUGIN_ROOT}/RULES.md` in full. Everything below follows it.
2. Work out the repo name (lowercase, hyphens). Default it to the current
   directory's name. The package name is the same in snake_case.
3. Ask what the app does and how it runs (HTTP service, worker, command),
   what it talks to, and whether it needs a database (RULES.md §5:
   PostgreSQL by default; SQLite only if the owner says so). Don't invent
   details; leave TODOs for anything unknown. Ask which license to use:
   MIT (the default) or another (RULES.md §11), and whether to publish to
   PyPI (RULES.md §9; if so, check the name is free there).
4. Target directory: the current directory if it is empty or already named
   after the repo, otherwise `./<repo-name>`. Never overwrite an existing
   file without asking.
5. Copy `${CLAUDE_PLUGIN_ROOT}/templates/.` (dotfiles included) into the
   target, then delete `optional/` from the copy. If the app needs a
   database, first apply `optional/postgres/README.md`.
6. If the owner chose a license other than MIT, replace `LICENSE` with that
   license's official text (`gh api licenses/<id> --jq .body`, placeholders
   filled in) and update `pyproject.toml`'s `license`, the README badge and
   the License section.
7. Fill in placeholders everywhere, file contents and names
   (`src/example_app/`): `example-app` → repo name, `example_app` →
   package name, `PROJECT` → title, the LICENSE year → current year, and
   the `vX.Y.Z` in AGENTS.md → `metadata.version` in
   `${CLAUDE_PLUGIN_ROOT}/SKILL.md`. Replace the example
   server, settings, tests, README and docs with the real app, keeping
   their conventions (settings from the environment, `--version`, SIGTERM,
   `/healthz` for services), or leave them clearly marked TODO. Generate
   `.env.example` for every variable the real app uses (RULES.md §2).
8. Look up current versions (RULES.md §8): Python with a slim image, uv,
   the actions in `.github/workflows/`, pre-commit hook revs, the lint and
   gitleaks images. Update any that are stale, then `uv lock`.
9. `git init`, `ln -s AGENTS.md CLAUDE.md`, then run
   `docker compose -f docker-compose.test.yaml run --rm test`,
   `docker compose -f docker-compose.lint.yaml run --rm lint` and
   `docker compose -f docker-compose.prod.yaml build`. Fix failures.
   If the human asks you to create the GitHub repo: create it, push the
   initial commit to `main` (the one commit allowed before protection),
   then run `scripts/setup-github.sh` to protect `main` and enable the
   security features. All later changes go through PRs.
10. If publishing to PyPI, tell the human the one-time setup in
   `${CLAUDE_PLUGIN_ROOT}/docs/releasing.md` (trusted publisher or
   `PYPI_API_TOKEN` secret, then `PYPI_PUBLISH=true`); don't do it unasked.
11. Report what you created, what is still TODO, and what you didn't test.
   Don't create a GitHub repo, commit, or push unless asked.
