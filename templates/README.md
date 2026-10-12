# PROJECT

[![CI](https://github.com/romkey/example-app/actions/workflows/ci.yaml/badge.svg)](https://github.com/romkey/example-app/actions/workflows/ci.yaml)
[![Lint](https://github.com/romkey/example-app/actions/workflows/lint.yaml/badge.svg)](https://github.com/romkey/example-app/actions/workflows/lint.yaml)
[![Python 3.14](https://img.shields.io/badge/python-3.14-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

One paragraph: what this is and why you'd want it.

> **AI disclosure:** This project was written by AI under human oversight,
> following [these rules](https://github.com/romkey/python-ai-rules/blob/main/RULES.md).

## What's here

| Path | What it is |
|------|------------|
| `src/example_app/` | The app: `config.py` reads settings from the environment, `server.py` serves HTTP |
| `tests/` | pytest tests |
| `docs/configuration.md` | Every environment variable |

## Technical details

How it works, what it talks to, its HTTP API or command line.

## Running it

Requires Docker. Configuration comes from environment variables, kept in
`.env` (see [docs/configuration.md](docs/configuration.md)):

```bash
cp .env.example .env   # then edit it
docker compose -f docker-compose.prod.yaml up -d
```

That runs the latest release from `ghcr.io/romkey/example-app`; set
`APP_VERSION=X.Y.Z` to pin one. The app answers on http://localhost:8000.

### With pip

Needs Python 3.14 or newer. Install into a virtual environment, from a
release's wheel (or `pip install example-app` if it's published on PyPI):

```bash
python3 -m venv ~/.venvs/example-app
~/.venvs/example-app/bin/pip install https://github.com/romkey/example-app/releases/download/vX.Y.Z/example_app-X.Y.Z-py3-none-any.whl
~/.venvs/example-app/bin/example-app --version
```

Set its environment variables yourself (see
[docs/configuration.md](docs/configuration.md)); it doesn't read `.env`.

## Development

With Docker, nothing else to install:

```bash
docker compose up --build                                  # run from the working tree
docker compose -f docker-compose.test.yaml run --rm test   # tests with coverage
docker compose -f docker-compose.lint.yaml run --rm lint   # every lint check, as CI runs them
```

With [uv](https://docs.astral.sh/uv/), which installs the exact versions
CI tests (`uv.lock`):

```bash
uv sync
uv run pytest
uv run mypy
uv run example-app
```

With pip (25.1 or newer, for `--group`). pip doesn't read `uv.lock`, so it
may pick newer dependency versions than CI tested:

```bash
python3 -m venv .venv
. .venv/bin/activate
pip install -e . --group dev
pytest
mypy
example-app
```

Either way, `uvx pre-commit install` (or `pip install pre-commit &&
pre-commit install`) runs the lint checks on every commit.

## License

[MIT](LICENSE)
