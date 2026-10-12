# Python Project Rules for AI Assistants

Rules for AI assistants writing Python applications for romkey. Follow every
rule unless the human says otherwise. Templates live in
[`templates/`](templates/); copy them and fill them in rather than inventing
new ones.

Canonical URL: https://github.com/romkey/python-ai-rules/blob/main/RULES.md

## 0. How to work

- **Never invent APIs.** Library functions, options, environment variables
  and protocol details come from the library's docs or source; link the
  source in a comment when it isn't obvious. If you can't find it, ask.
- **Ask before adding** a framework, a service (database, queue, cache) or
  a dependency the stdlib or an existing dependency already covers.
- **Prove it before claiming it.** Run the tests and lint (§13) before
  saying something works. Say plainly what you did not test, e.g. "tests
  pass; not tried against the real API".
- **Never trust your memory for versions.** Look up current releases of
  Python, packages, images and actions (see §8).
- **When first applying these rules to a repo**, new or existing, ask the
  owner which license to use (§11) before adding or changing `LICENSE`.
- **Never expose secrets.** Don't put real secret values in code, tests,
  docs, commit messages, PR text, issues or chat, and don't print `.env`.
  Configuration comes from the environment (§2). If you find a real secret
  in the repo or its history, stop and tell the owner to rotate it;
  rewriting history doesn't make it secret again.
- Small, focused commits with messages that say why. `main` is protected:
  work on a branch and open a pull request; never push to `main`. Don't
  push, merge, tag or release without being asked.

## 1. Repository layout

```
src/<package>/     the application (src layout); py.typed
tests/             pytest tests, test_<module>.py
docs/              configuration.md, overview.md
scripts/           changelog-section.sh, bump-version.sh, check-env-example.py,
                   check-env-secrets.py, setup-github.sh
.github/           workflows/ci.yaml, lint.yaml, release.yaml
pyproject.toml  uv.lock  .python-version  Dockerfile  .dockerignore
docker-compose.yaml  docker-compose.test.yaml  docker-compose.lint.yaml
docker-compose.prod.yaml  .env.example  renovate.json  .pre-commit-config.yaml
.yamllint.yaml  .gitleaks.toml  .gitignore  README.md  CHANGELOG.md  LICENSE
SECURITY.md  AGENTS.md
```

- The repo name is lowercase with hyphens and is also the distribution,
  command and image name (`my-app`); the package is the same in snake_case
  (`my_app`).
- These rules are for applications: things that run as a service, worker
  or command. If the human wants a library published to PyPI, ask how it
  should differ.

## 2. Python

- **Version:** the newest Python with an official `python:X.Y-slim-trixie`
  image. `.python-version`, `requires-python = ">=X.Y"` and the
  Dockerfile's image always name the same version; change all three
  together. Use the language features it offers.
- **uv** is how you develop, test and release: `uv add`/`uv remove` for
  dependencies, `uv.lock` committed, `uv run` to run things. No
  `requirements.txt` or setup.py. The build backend is `uv_build`.
- **pip must work too**, for people who don't use uv: everything is in
  standard `pyproject.toml` (PEP 621 metadata, PEP 735 dependency groups),
  so `pip install -e . --group dev` sets up development and
  `pip install .` (or from a release's wheel, or PyPI) installs the app.
  The README documents both. CI proves the wheel installs with pip. pip
  ignores `uv.lock`, so say that uv gives the tested versions.
- **Types everywhere.** mypy `--strict` passes on `src/`, `tests/` and
  `scripts/`. No `Any` without a comment saying why; no `# type: ignore`
  without an error code and a reason.
- **ruff** formats and lints, with the rule set in the template's
  `pyproject.toml`. Fix findings rather than adding `noqa`; when a `noqa`
  is right, give the code and the reason.
- **Configuration comes from environment variables**, read once at startup
  into a typed, frozen settings object (template: `config.py`) that
  validates every value and fails with a message naming the variable.
  Secrets have no defaults. Each variable is described in
  `docs/configuration.md`.
- **Generate and maintain `.env.example`.** It lists every environment
  variable the project uses: everything the app reads, what compose
  services need (e.g. `POSTGRES_PASSWORD`), and credentials for tooling
  (e.g. `UV_PUBLISH_TOKEN` for PyPI), each with a comment and a dummy
  value, never a real one. Optional ones are commented out (`# HOST=...`).
  Update it in the same change that adds, renames or removes a variable.
  The `env-example` hook fails if the app reads a variable it doesn't
  list.
- **Logging**, not `print()`: `logging.getLogger(__name__)` per module,
  configured once in `main()`, to stdout. Lazy `%s` formatting. Never log
  secrets or full request bodies.
- The entry point is a `[project.scripts]` command whose `main()` returns
  an exit code, supports `--version`, and handles SIGTERM by shutting down
  cleanly (`docker stop` sends it).
- Keep I/O at the edges and logic in plain functions that are easy to
  test. Catch specific exceptions; never a bare `except:` or a silent
  `except Exception: pass`.
- Timezone-aware datetimes (`datetime.now(UTC)`), `pathlib` for paths,
  timeouts on every network call.

## 3. Dependencies

- Prefer the standard library. Add a dependency only when it removes real
  work, is maintained, and is widely used; say why in the PR.
- `dependencies` in `pyproject.toml` take lower bounds (`>=X.Y`); `uv.lock`
  pins exact versions. Dev tools go in `[dependency-groups] dev`.
- Lint tools that run from pre-commit (ruff, yamllint...) are pinned there,
  not in `dev`. mypy is in `dev` because it needs the project's
  dependencies.

## 4. Tests

- pytest in `tests/`, with coverage of `src/` (`pytest-cov`); the suite
  fails under 80%. New code comes with tests; a bug fix comes with a test
  that failed before it.
- Tests are fast and deterministic: no real network, no sleeping, no
  dependence on order. Fake external services at their boundary; use
  `monkeypatch`, `tmp_path`, and port 0 for servers.
- Tests that need a database run against a real PostgreSQL (§5), in Docker
  locally and as a service container in CI, never SQLite standing in.

## 5. Databases

- Don't add one unless the app needs persistent, shared or queryable
  state; ask first.
- **PostgreSQL** is the default: current major `postgres:N-trixie` image,
  psycopg 3, connection from `DATABASE_URL`. Add SQLAlchemy 2 and Alembic
  only when the app has models. Schema changes are migrations committed
  with the code, applied by an explicit `migrate` command, never by hand.
- **SQLite** only when the owner agrees it fits: one process, small data,
  nothing else reads it. The file lives in a named volume, with WAL mode
  and foreign keys on, and the schema is still versioned.
- [`templates/optional/postgres/`](templates/optional/postgres/README.md)
  has the compose, CI, migration and test setup to copy.

## 6. Docker

Everything runs in Docker with nothing else installed. Use the template's
[`Dockerfile`](templates/Dockerfile) and four compose files unchanged except
for names, ports, image pins and added services (e.g. a database):

| File | Use | Services |
|------|-----|----------|
| `docker-compose.yaml` | development: `docker compose up` | `app`, working tree mounted |
| `docker-compose.test.yaml` | tests, as CI runs them | `test` |
| `docker-compose.lint.yaml` | lint, as CI runs it | `lint`, `secrets` |
| `docker-compose.prod.yaml` | production | `app` from the released image |

Name them exactly so (`.yaml`, never `compose.yaml` or `.yml`); run the
non-dev ones with `docker compose -f <file>`.

- The Dockerfile has a `dev` stage (uv and all dependency groups; the venv
  at `/venv` so the mounted working tree doesn't hide it) and a
  `production` stage: runtime dependencies only, non-editable install, no
  uv, non-root user, `CMD` the app's command. Dependencies install in a
  layer before the source is copied, with uv's cache mounted.
- Production config comes from `.env` via `env_file`; nothing secret is
  baked into an image (`.dockerignore` excludes `.env*`). The production
  compose file adds a health check, `restart: unless-stopped`,
  `read_only`, `cap_drop: [ALL]` and `no-new-privileges`.
- Services listening on a port expose `GET /healthz` (no auth, no
  dependencies beyond the process) for the health check.

## 7. Git and pre-commit

- Use [`templates/.gitignore`](templates/.gitignore): ignores `.venv/`,
  caches, build output, and `.env`/`.env.*` except `.env.example`.
- **Secrets never reach the repo.** The pre-commit hooks enforce it:
  - `env-secrets` (`scripts/check-env-secrets.py`) fails if a value from
    your local `.env` files appears in any committed file. It names the
    file, line and variable, never the value. `not-a-secret` on a line
    allows it.
  - `gitleaks` checks staged changes for tokens and keys; the Lint job and
    the lint compose file's `secrets` service scan the whole history.
    [`.gitleaks.toml`](templates/.gitleaks.toml) exempts only
    `.env.example`; accept a false positive by adding its fingerprint to
    `.gitleaksignore`.
- [`.pre-commit-config.yaml`](templates/.pre-commit-config.yaml) holds every
  lint, format and type check (ruff, mypy, `uv lock` up to date, yamllint,
  actionlint, shellcheck, hadolint, whitespace, large files, private keys,
  secrets, `.env.example` complete). The same hooks run via the lint compose file, as a git hook
  (`uvx pre-commit install`), and in CI.

## 8. GitHub workflows

Start from [`templates/.github/`](templates/.github/) and
[`templates/renovate.json`](templates/renovate.json).

**Versions.** Your training data is months old and the actions you remember
are probably deprecated. Before writing or editing any workflow, look up the
latest release of every action and tool you use, e.g.
`gh api repos/actions/checkout/releases/latest --jq .tag_name`. Use the
major tag (`@v7`) only if it exists
(`gh api repos/actions/checkout/git/ref/tags/v7`); some actions, like
`astral-sh/setup-uv`, publish only full versions (`@v10.3.0`). Do the same
for Python, base images, pre-commit hook revs and packages. A Node.js
deprecation warning in a run log means an action is out of date: fix it.
Afterwards [Renovate](https://docs.renovatebot.com/) keeps everything
current, including `uv.lock`. Versions on 2026-10-12, for sanity checking
only: Python 3.14 (3.15 has no slim image yet), uv 0.13.0,
`actions/checkout@v7`, `actions/cache@v6`, `astral-sh/setup-uv@v10.3.0`,
`docker/build-push-action@v7`, `docker/setup-buildx-action@v4`,
`docker/login-action@v4`, `docker/metadata-action@v6`.

**Protected main.** Every change reaches `main` through a pull request,
squash-merged, and only when the required checks **CI passed** and
**Lint** pass on an up-to-date branch. `scripts/setup-github.sh` applies
this as a ruleset, plus secret scanning with push protection (and generic
patterns and validity checks where GitHub Secret Protection is available),
Dependabot alerts, private vulnerability reporting, CodeQL default setup,
read-only workflow tokens and branch deletion on merge. Run it once when
the GitHub repo is created (re-running is safe). Keep the required checks
reporting:

- Never use `paths`/`paths-ignore` on a workflow that provides a required
  check; a workflow that doesn't run blocks the PR forever. Skip expensive
  jobs inside it instead.
- Required check names must be stable, so jobs feed one summary job
  (`CI passed`) instead of being required themselves.
- GitHub holds the workflow runs of a PR opened by `GITHUB_TOKEN` as
  `action_required`. The workflow that opened it must approve them
  (`POST /repos/{owner}/{repo}/actions/runs/{id}/approve`); runs started
  separately with `gh workflow run` do not satisfy the PR's required
  checks.

**lint.yaml**: runs pre-commit on all files and gitleaks over the whole
git history (job **Lint**).

**ci.yaml**: runs pytest with coverage against the locked dependencies,
builds the sdist and wheel and runs `<app> --version` from the wheel
installed with pip, and builds the production image and runs
`<app> --version` in it; all skipped when a change touches only docs. Ends with **CI passed**.

**release.yaml**: run it from the Actions tab (**Run workflow**) with a
`bump` choice of `patch` (default), `minor` or `major`. It checks CI
passed (waiting for it right after a merge), runs
`scripts/bump-version.sh` on a `release/vX.Y.Z` branch, opens a
"Release vX.Y.Z" PR and approves its CI and Lint runs. Merging that PR
tags the merge commit, pushes the production image, optionally publishes
to PyPI, and creates the GitHub Release (§9). Pushing a `vX.Y.Z` tag by hand also works.

**Speed:**

- Install with `astral-sh/setup-uv` (`enable-cache: true`), not pip or
  setup-python; uv installs the Python in `.python-version`.
- Build images with Buildx and the GitHub Actions layer cache
  (`cache-from: type=gha`, `cache-to: type=gha,mode=max`). Cache
  pre-commit hook environments.
- `concurrency` with `cancel-in-progress: true` (except releases).
- `timeout-minutes` on every job; least-privilege `permissions`:
  `contents: read` unless a job needs more.

## 9. Releases

Full explanation: [docs/releasing.md](docs/releasing.md).

- [Semantic versioning](https://semver.org/), tags `vX.Y.Z`; the first
  release is 0.1.0. Breaking (major): removing or renaming a command,
  option, environment variable, HTTP endpoint or response field; changing
  a default that changes behavior; a database change without a migration
  path; raising the minimum of anything users must provide. Minor: new
  features, options, endpoints. Patch: fixes and dependency updates.
  Before 1.0.0, breaking changes bump the minor.
- `main` is always releasable. To release, run the Release workflow from
  the Actions tab, pick the bump, then merge the release PR it opens.
  `scripts/bump-version.sh <patch|minor|major>` makes the edits (moves
  `## [Unreleased]` entries under `## [X.Y.Z] - YYYY-MM-DD`, sets the
  version in `pyproject.toml` and `uv.lock` with `uv version`); a human can
  run it on a branch and open the PR themselves.
- `release.yaml` refuses to publish if the changelog section is missing or
  `pyproject.toml`'s version doesn't match the tag. It then pushes the
  production image for `linux/amd64` and `linux/arm64` to
  `ghcr.io/<owner>/<repo>`, tagged `X.Y.Z`, `X.Y`, `X` (from 1.0.0) and
  `latest` (pre-releases get only `X.Y.Z-rc.N`), with provenance and an
  SBOM, and creates the GitHub Release with the changelog section and the
  image reference as notes, and the sdist and wheel attached.
- **PyPI is optional**; ask the owner. To publish, check the name is free
  on PyPI, add a trusted publisher there for `release.yaml` (preferred: no
  secret), or else store a project-scoped token as the `PYPI_API_TOKEN`
  repository secret, then set the repository variable `PYPI_PUBLISH` to
  `true`. Each release then runs `uv publish`. Never put a token in the
  repo; `UV_PUBLISH_TOKEN` in `.env` is only for publishing by hand.

## 10. Documentation

**README.md**, in this order:

1. Title and badges (below)
2. One-paragraph introduction
3. AI disclosure (verbatim, below)
4. Project breakdown: what each part of the code does
5. Technical details: how it works, its API or command line, what it talks to
6. Running it (production compose, `.env`; `pip install`), then development
   with Docker, uv and pip, and the test and lint commands
7. License

Badges, in this order, exactly this style. Only CI/Lint status may show red,
and only because a build failed:

```markdown
[![CI](https://github.com/romkey/REPO/actions/workflows/ci.yaml/badge.svg)](https://github.com/romkey/REPO/actions/workflows/ci.yaml)
[![Lint](https://github.com/romkey/REPO/actions/workflows/lint.yaml/badge.svg)](https://github.com/romkey/REPO/actions/workflows/lint.yaml)
[![Python 3.14](https://img.shields.io/badge/python-3.14-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
```

The Python badge names the version in `.python-version`. For another
license, use its SPDX id in the license badge (`License-Apache--2.0-yellow`;
shields.io needs `--` for a literal `-`). Add a release badge once tagged:
`https://img.shields.io/github/v/release/romkey/REPO?color=blue`. Any other
badge uses `blue` (info) or `lightgrey` (neutral).

AI disclosure:

```markdown
> **AI disclosure:** This project was written by AI under human oversight,
> following [these rules](https://github.com/romkey/python-ai-rules/blob/main/RULES.md).
```

**CHANGELOG.md**: [Keep a Changelog](https://keepachangelog.com/) format,
newest first, `## [Unreleased]` at the top. Update it with every change.

**docs/configuration.md**: every environment variable: default (or
required), allowed values and meaning.

**docs/overview.md**: under ~60 lines, for AIs and humans. What the project
is, how it runs, the file map, each module in one line, conventions. No
prose padding.

**AGENTS.md** (copy to CLAUDE.md or symlink): tells AI tools to follow
these rules and records the rules version the repo follows
("Follows python-ai-rules vX.Y.Z"), so anyone can see which UPGRADING.md
entries it still needs. Update that line whenever the repo is brought up
to a newer version. Plus anything project-specific.

## 11. License

- Default: MIT, in `LICENSE`, `Copyright (c) <year> John Romkey`, and
  `license = "MIT"` in `pyproject.toml`.
- The first time these rules are applied to a repo, ask the owner: "MIT,
  or a different license?" If different, use that license's official text
  (`gh api licenses/<spdx-id-lowercase> --jq .body`, filling in its year
  and name placeholders) and never copy the MIT `LICENSE`. Match the
  README badge, License section and `pyproject.toml` to it.
- Never change an existing repo's license without the owner's explicit
  confirmation; if it already has one, ask whether to keep it.

## 12. Keeping repos current

These rules change. When you re-scan a repo that already follows them,
read [UPGRADING.md](UPGRADING.md) and apply every entry newer than the
version in the repo's `AGENTS.md` ("Follows python-ai-rules vX.Y.Z"), then
update that line. When you change these rules in a way existing repos must
follow, add an entry to UPGRADING.md in the same PR, headed
`## Unreleased: ...`; the release labels it with its version.

## 13. Before finishing

- `docker compose -f docker-compose.test.yaml run --rm test` passes.
- `docker compose -f docker-compose.lint.yaml run --rm lint` passes.
- For Dockerfile or dependency changes,
  `docker compose -f docker-compose.prod.yaml build` succeeds and the image
  runs.
- `.env.example`, README, docs and CHANGELOG reflect the change.
- Changes are on a branch with a PR open, not on `main`.
- You've told the human what you did not test.
