# Changelog

All notable changes to this project are documented here. The format follows
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/) and the project uses
[Semantic Versioning](https://semver.org/).

## [Unreleased]

## [0.1.0] - 2026-10-12

### Added

- RULES.md for Python applications: AI conduct, layout, Python and uv,
  dependencies, tests, databases (PostgreSQL by default), Docker, git and
  pre-commit, GitHub workflows, releases, documentation, license.
- A working template app: settings from the environment, an HTTP server
  with `/healthz`, tests at 100% coverage, strict mypy, ruff.
- Dockerfile with `dev` and non-root `production` stages, and compose
  files for development, tests, lint and production.
- CI running the tests and building the production image; lint via
  pre-commit (ruff, mypy, uv-lock, yamllint, actionlint, shellcheck,
  hadolint, gitleaks, a check for `.env` values in committed files) plus a
  gitleaks scan of the whole history.
- Release workflow: a release PR from the Actions tab; merging it tags,
  pushes a multi-arch image to ghcr.io and creates the GitHub Release.
- pip support alongside uv: README instructions for installing with pip
  and for a pip-based development setup; CI builds the package and
  installs the wheel with pip; every GitHub Release carries the sdist and
  wheel.
- Optional PyPI publishing on release, by trusted publishing or a
  `PYPI_API_TOKEN` secret, switched on with the `PYPI_PUBLISH` variable;
  `.env.example` lists `UV_PUBLISH_TOKEN` for publishing by hand.
- Rule to generate and maintain `.env.example` with every variable the
  project uses, enforced by a pre-commit hook (`check-env-example.py`).
- Optional PostgreSQL kit, Renovate config with lockfile maintenance, and
  `scripts/setup-github.sh` for branch protection and security features.
- The repo is an Agent Skill (`SKILL.md`), usable from claude.ai, the
  API, Claude Code's skills folder and other tools that read Agent
  Skills; each release attaches `python-ai-rules-skill.zip`.
- Claude Code plugin `python-rules` with `new`, `check`, `release` and
  `rules` skills, and its marketplace `romkey-python`.
