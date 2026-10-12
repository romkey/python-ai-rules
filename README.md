# python-ai-rules

[![CI](https://github.com/romkey/python-ai-rules/actions/workflows/ci.yaml/badge.svg)](https://github.com/romkey/python-ai-rules/actions/workflows/ci.yaml)
[![Lint](https://github.com/romkey/python-ai-rules/actions/workflows/lint.yaml/badge.svg)](https://github.com/romkey/python-ai-rules/actions/workflows/lint.yaml)
[![Python 3.14](https://img.shields.io/badge/python-3.14-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

Rules for AI assistants writing my Python applications, a complete template
project they start from, and a Claude Code plugin that scaffolds, audits and
releases projects that follow them.

> **AI disclosure:** This project was written by AI under human oversight,
> following [these rules](https://github.com/romkey/python-ai-rules/blob/main/RULES.md).

## What's here

| Path | What it is |
|------|------------|
| [RULES.md](RULES.md) | The rules. Point an AI at this file. |
| [templates/](templates/) | A working example app: src layout, tests, Dockerfile, dev/test/lint/prod compose files, CI, release workflow, pre-commit, Renovate, docs skeletons |
| [templates/optional/postgres/](templates/optional/postgres/) | How to add PostgreSQL (or, if it must be, SQLite) |
| [SKILL.md](SKILL.md) | Makes this repo an Agent Skill |
| [skills/](skills/), [.claude-plugin/](.claude-plugin/) | The `python-rules` Claude Code plugin |
| [UPGRADING.md](UPGRADING.md) | Fixes repos set up under older rules must apply |
| [SECURITY.md](SECURITY.md) | How to report a vulnerability |
| [docs/](docs/) | [Release strategy](docs/releasing.md), [Claude Code usage](docs/claude-code.md), [configuration guide](docs/configuration.md), [overview](docs/overview.md) |

## What the rules cover

- **How the AI works:** no invented APIs, ask before adding frameworks,
  services or dependencies, run the tests and lint before claiming
  success, say what wasn't tested, look up current versions instead of
  trusting training data.
- **Python:** the newest Python, uv for development (pip still works),
  src layout, strict mypy, ruff, configuration from environment variables
  with a complete `.env.example`, logging, clean shutdown.
- **Tests:** pytest with an 80% coverage floor, fast and deterministic,
  real PostgreSQL when there's a database.
- **Databases:** none unless needed; PostgreSQL by default, SQLite only by
  agreement, migrations always.
- **Docker:** dev, test, lint and production compose files; a small,
  non-root, read-only production image.
- **Tooling:** pre-commit for lint, format, types and secrets; GitHub
  Actions with uv and layer caching; Renovate; protected `main`.
- **Releases:** semver, changelog-driven release notes, a multi-arch
  production image on ghcr.io and a GitHub Release with the wheel for
  every version; optionally PyPI.
- **Installing:** Docker, uv or plain pip, all documented.
- **Docs:** README layout, badges, AI disclosure, CHANGELOG, configuration
  reference, a short overview for AIs.

## Using it

**With Claude Code**, install the plugin
([details](docs/claude-code.md)):

```
/plugin marketplace add romkey/python-ai-rules
/plugin install python-rules@romkey-python
```

Then `/python-rules:new` starts a project, `/python-rules:check` audits
one, and `/python-rules:release` cuts a release.

**As an Agent Skill**, for Claude (claude.ai, the desktop app, the API)
or any other tool that reads [Agent Skills](https://agentskills.io): download
`python-ai-rules-skill.zip` from the
[latest release](https://github.com/romkey/python-ai-rules/releases/latest)
and upload it as a skill, or clone the repo into the tool's skills folder:

```bash
git clone https://github.com/romkey/python-ai-rules ~/.claude/skills/python-ai-rules
```

The skill covers the same tasks as the plugin's commands: describe them
("start a new Python app", "audit this repo", "cut a release").

**With any AI assistant**, tell it: "Follow
https://github.com/romkey/python-ai-rules/blob/main/RULES.md", or
copy [templates/AGENTS.md](templates/AGENTS.md) into the project.

**By hand**, copy `templates/` and follow the
[configuration guide](docs/configuration.md).

## Developing this repo

The templates are tested like a real project; this repo's CI runs the
template's tests and builds its production image.

```bash
docker compose -f docker-compose.lint.yaml run --rm lint
cd templates
docker compose -f docker-compose.test.yaml run --rm test
docker compose -f docker-compose.prod.yaml build
cd ..
claude plugin validate .
```

`main` is protected: changes go through pull requests, which merge once
**CI passed** and **Lint** pass. `.github/workflows/ci.yaml` is generated
from the template's: edit
`templates/.github/workflows/ci.yaml` and run `scripts/sync-ci.py`.

## License

[MIT](LICENSE)
