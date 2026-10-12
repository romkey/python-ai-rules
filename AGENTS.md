# Instructions for AI assistants

This repo holds the rules, templates and Claude Code plugin. It follows its
own [RULES.md](RULES.md) where it applies. Read [docs/overview.md](docs/overview.md)
first.

- Changing a template means testing it like a project, from `templates/`:
  `docker compose -f docker-compose.test.yaml run --rm test` and
  `docker compose -f docker-compose.prod.yaml build`, plus
  `docker compose -f docker-compose.lint.yaml run --rm lint` here.
- Never edit `.github/workflows/ci.yaml` directly; edit
  `templates/.github/workflows/ci.yaml` and run `scripts/sync-ci.py`.
- After changing `skills/` or `.claude-plugin/`, run `claude plugin validate .`.
- A release bumps `version` in `.claude-plugin/plugin.json` and
  `metadata.version` in `SKILL.md` to match the tag.
- `SKILL.md` makes this repo an Agent Skill; `scripts/package-skill.sh`
  zips it. Keep its links relative and its `name` equal to the repo name.
- `main` is protected: branch, open a PR, and let CI and Lint pass.
- If a change means repos already following the rules must update
  something, add an entry to UPGRADING.md.
- Keep RULES.md succinct: it is read in full by every AI using it.
