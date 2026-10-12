# Upgrading repos that follow these rules

These rules change, and repos set up under an older version don't pick up
fixes on their own. Each entry below is a change that **existing repos
must apply**, newest first.

**AI assistants re-scanning a repo** (for example with
`/python-rules:check`): read the version in the repo's `AGENTS.md`
("Follows python-ai-rules vX.Y.Z"; treat a missing one as v0.0.0), apply
every entry newer than it (and any `Unreleased` ones, if you're working
from `main`), then update that line to the current release. Check each
entry against what's actually there; a repo may have diverged
deliberately, so ask before overwriting customizations.

**Anyone changing these rules**: when a change means existing repos must
update something, add an entry here in the same PR, headed
`## Unreleased: <what changed>`, with a **Check:** (how to tell a repo
needs it) and a **Fix:**. Don't guess the version: cutting a release
(`scripts/bump-version.sh`) renames `Unreleased` to it. An entry is only
needed for something a release shipped; a bug fixed before its release
needs none.

No entries yet.
