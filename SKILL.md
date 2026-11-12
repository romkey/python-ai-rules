---
name: python-ai-rules
description: romkey's rules for Python applications, with a template project. Use when creating, writing, editing, reviewing, auditing or releasing a Python application (code, tests, uv and pip dependencies, Dockerfiles, compose files, GitHub Actions, PyPI, docs), and in any repo whose AGENTS.md or README says it follows python-ai-rules.
license: MIT
metadata:
  author: John Romkey
  version: "0.1.0"
  homepage: https://github.com/romkey/python-ai-rules
---

# Python AI rules

Read [RULES.md](RULES.md) in full and follow it. Paths below are relative
to this skill's directory.

- [templates/](templates/) is a complete, working project. Copy files from
  there rather than writing them from memory. What each one is for:
  [docs/configuration.md](docs/configuration.md).
- [templates/optional/postgres/](templates/optional/postgres/README.md):
  adding a database.
- [docs/releasing.md](docs/releasing.md): versions, releases, PyPI.
- [UPGRADING.md](UPGRADING.md): changes to apply to a repo that already
  follows an older version of these rules. This copy is version
  `metadata.version` above; a repo records the version it follows in its
  AGENTS.md.

## Tasks

For these, follow the matching instructions in [skills/](skills/), reading
`${CLAUDE_PLUGIN_ROOT}` there as this skill's directory and `$ARGUMENTS`
as whatever the human asked for:

- **Start a new project:** [skills/new/SKILL.md](skills/new/SKILL.md)
- **Audit a repo, or bring it up to date:** [skills/check/SKILL.md](skills/check/SKILL.md)
- **Cut a release:** [skills/release/SKILL.md](skills/release/SKILL.md)

Anything else (writing code, fixing a bug, adding a dependency): follow
RULES.md, and finish with its §13 checklist.
