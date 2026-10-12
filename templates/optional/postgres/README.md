# Adding PostgreSQL

Only for apps that need a database (RULES.md §5). Apply these changes to
the project, then delete `optional/`. Look up current versions first; the
ones here were current on 2026-10-12.

## Dependencies

```bash
uv add "psycopg[binary]"
# Only if the app needs an ORM and migrations:
uv add sqlalchemy alembic
```

Use psycopg 3 directly for a few queries; SQLAlchemy 2 (typed, `select()`
style) when there are models. Either way, schema changes are Alembic
migrations committed with the code (`alembic init migrations`, set
`sqlalchemy.url` from `DATABASE_URL` in `migrations/env.py`). Never change
the schema by hand or with `create_all()` outside tests.

## Configuration

The app reads one variable, `DATABASE_URL`
(`postgresql://user:password@host:5432/dbname`), required, with no default.
Add it to `config.py`, `docs/configuration.md` and `.env.example` (with a
dummy password). Add a `migrate` subcommand that runs
`alembic upgrade head`.

## docker-compose.yaml (dev)

```yaml
services:
  app:
    # ...existing settings...
    environment:
      DATABASE_URL: postgresql://app:app@db:5432/app  # not-a-secret
    depends_on:
      db:
        condition: service_healthy

  db:
    image: postgres:18-trixie
    environment:
      POSTGRES_USER: app
      POSTGRES_PASSWORD: app  # not-a-secret: local dev only
      POSTGRES_DB: app
    ports:
      - "5432:5432"
    volumes:
      - db-data:/var/lib/postgresql
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U app -d app"]
      interval: 2s
      timeout: 5s
      retries: 15

volumes:
  db-data:
```

## docker-compose.test.yaml

The same `db` service, without `ports` or the volume (add
`tmpfs: [/var/lib/postgresql]` so every run starts empty and fast), and the
`test` service gets the same `environment` and `depends_on`.

## docker-compose.prod.yaml

```yaml
services:
  migrate:
    image: ghcr.io/romkey/example-app:${APP_VERSION:-latest}
    command: ["example-app", "migrate"]
    env_file:
      - path: .env
        required: false
    depends_on:
      db:
        condition: service_healthy

  app:
    # ...existing settings...
    depends_on:
      migrate:
        condition: service_completed_successfully

  db:
    image: postgres:18-trixie
    restart: unless-stopped
    env_file:
      - path: .env
        required: false
    volumes:
      - db-data:/var/lib/postgresql
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U \"$$POSTGRES_USER\" -d \"$$POSTGRES_DB\""]
      interval: 10s
      timeout: 5s
      retries: 5

volumes:
  db-data:
```

No `ports:` on `db`: only the app reaches it. `.env` sets
`POSTGRES_USER`, `POSTGRES_PASSWORD`, `POSTGRES_DB` and the matching
`DATABASE_URL` (host `db`). Back up the `db-data` volume
(`docker compose -f docker-compose.prod.yaml exec db pg_dump ...`).

## CI (`.github/workflows/ci.yaml`)

Tests run against a real PostgreSQL, never SQLite standing in for it. Add
to the `tests` job:

```yaml
    services:
      db:
        image: postgres:18-trixie
        env:
          POSTGRES_USER: app
          POSTGRES_PASSWORD: app  # not-a-secret: CI only
          POSTGRES_DB: app
        ports:
          - 5432:5432
        options: >-
          --health-cmd "pg_isready -U app -d app"
          --health-interval 2s --health-timeout 5s --health-retries 15
    env:
      DATABASE_URL: postgresql://app:app@localhost:5432/app  # not-a-secret
```

## Tests

A session fixture runs the migrations once; each test runs in a
transaction that is rolled back, so tests don't see each other's data.

## SQLite instead

Only if the owner agrees (RULES.md §5): one process, small data, nothing
else needs to read it. Then use the standard library's `sqlite3`, keep the
file in a named volume mounted at `/data` (`DATABASE_PATH=/data/app.db`),
turn on WAL (`PRAGMA journal_mode=WAL`) and foreign keys
(`PRAGMA foreign_keys=ON`), and still version the schema with migrations.
