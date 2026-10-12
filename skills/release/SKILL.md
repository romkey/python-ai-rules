---
name: release
description: Cut a release of the current Python project following the python-ai-rules release process.
argument-hint: "[patch|minor|major]"
disable-model-invocation: true
---

Prepare a release. Arguments: `$ARGUMENTS` (bump type; optional). The process is in `${CLAUDE_PLUGIN_ROOT}/docs/releasing.md`;
read it first.

1. Check: on `main`, up to date with `origin/main`, and CI passed for the
   latest commit (`gh run list --workflow ci.yaml --branch main --limit 3`).
   Stop and report if not.
2. Read `## [Unreleased]` in CHANGELOG.md. If it's empty, stop: nothing to
   release.
3. Choose the bump (`patch`, `minor` or `major`). If not given, propose
   one from the entries using RULES.md §9 (breaking → major, or minor
   before 1.0.0; new features → minor; fixes → patch; the first release
   is minor, to 0.1.0) and explain why. Confirm with the human.
4. If pinned versions of this app in README/docs need the new version,
   make that change through a normal PR first.
5. Run the Release workflow: `gh workflow run release.yaml -f bump=<bump>`,
   watch it (`gh run watch`), and give the human the release PR's URL. It
   approves the PR's CI and Lint runs; if its log has a warning that it
   couldn't, approve them (`gh api -X POST
   repos/{owner}/{repo}/actions/runs/<id>/approve` for each
   `action_required` run on the branch). Report when the checks pass.
6. Don't merge the release PR unless the human asks; merging publishes.
   After it merges, watch the Release run triggered by the merge and report
   the release URL, the image (`ghcr.io/<owner>/<repo>:X.Y.Z`) and, if
   `PYPI_PUBLISH` is on, the PyPI page. On the
   first release, remind the human to check the package's visibility.
