# python-ai-rules overview

**What:** rules + templates for AI assistants writing romkey's Python
applications, and a Claude Code plugin that applies them.

## Files

- `RULES.md`: the rules. The one file an AI must read.
- `SKILL.md`: front matter and a short guide that make the repo an Agent
  Skill; `scripts/package-skill.sh` zips it for releases.
- `templates/`: a complete, working example app (src layout, tests,
  Dockerfile, dev/test/lint/prod compose files, workflows, pre-commit,
  Renovate, docs skeletons). New projects copy it.
- `templates/optional/postgres/`: how to add PostgreSQL (or SQLite).
- `skills/`: Claude Code plugin skills `new`, `check`, `release`, `rules`.
- `.claude-plugin/`: plugin + marketplace manifests.
- `UPGRADING.md`: fixes existing repos must apply, newest first.
- `docs/releasing.md`: release strategy. `docs/claude-code.md`: plugin use.
  `docs/configuration.md`: what each template file is and what to change.
- `scripts/sync-ci.py`: generates `.github/workflows/ci.yaml` from the
  template's, so this repo's CI tests `templates/`.
- `docker-compose.lint.yaml`: lints this repo, templates included.

## Conventions

- This repo follows RULES.md where it applies (it is a library of rules,
  not an app: no image of its own): README order and badges, CHANGELOG,
  pre-commit, Renovate, release workflow, MIT.
- Changing a template means testing it like a project (see AGENTS.md).
- Plugin version in `.claude-plugin/plugin.json` equals the release tag.
