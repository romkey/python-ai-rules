# PROJECT overview

<!-- Short, factual, for AIs and humans. Keep under ~60 lines. -->

**What:** one sentence.
**Runs as:** HTTP service on port 8000 | CLI | worker.
**Talks to:** nothing | PostgreSQL | other services.

## Files

- `src/example_app/__main__.py`: command line, logging, signal handling.
- `src/example_app/config.py`: `Settings` from environment variables.
- `src/example_app/server.py`: HTTP handler; `GET /healthz`.
- `tests/`: pytest; one file per module.
- `Dockerfile`: `dev` and `production` stages.
- `docker-compose.yaml` (dev), `.test`, `.lint`, `.prod`.

## Conventions

- All configuration from environment variables; see docs/configuration.md.
- Rules: https://github.com/romkey/python-ai-rules/blob/main/RULES.md
