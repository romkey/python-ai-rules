# Release strategy

How every repo that follows these rules is versioned and released. The
short version is in [RULES.md §9](../RULES.md#9-releases); this explains the
reasoning and walks through a release.

## Why release at all

People run these apps from images: `ghcr.io/romkey/<app>:1.4.2` in a
compose file. A tag is a promise that the image at that reference never
changes, so a deployment that works today still works after a restart next
year. Tracking `latest` is allowed but means accepting surprises; Renovate
turns new image tags into pull requests for deployments that pin, so
pinning costs nothing in freshness.

## Versions

[Semantic versioning](https://semver.org/), tags `vX.Y.Z`, starting at
0.1.0:

| Bump | When | Examples |
|------|------|----------|
| **Major** | Something that worked stops working | Removing/renaming a command, option, environment variable, endpoint or response field; a default that changes behavior; a database change with no migration |
| **Minor** | New things, nothing breaks | New feature, option, endpoint or variable with a default |
| **Patch** | Fixes only | Bug fixes, docs, CI, dependency bumps |

Environment variables, command-line options and HTTP responses count as
API: deployments, scripts and other services depend on them, so a rename
silently breaks someone's setup.

Before 1.0.0, breaking changes bump the minor (0.3.0 → 0.4.0) and everything
else bumps the patch. Go to 1.0.0 once the interfaces have settled.

Pre-releases (`v1.2.0-rc.1`) are published as GitHub pre-releases, with an
image tagged only `1.2.0-rc.1`, for trying a big change in a real
deployment before committing to it.

## The changelog is the source of truth

Every change adds a line under `## [Unreleased]` in CHANGELOG.md, in the
same commit. At release time those lines become the version's section and,
verbatim, the GitHub Release notes. The release workflow refuses to publish
a version with no changelog section, so a release can't go out undocumented.

## Branches

`main` is protected: every change arrives through a squash-merged PR whose
**CI passed** and **Lint** checks pass, so `main` is always releasable.
Releases are cut from `main`. The only other long-lived names are
`release/vX.Y.Z` branches, which exist just until their release PR merges.
If an old major ever needs a fix, branch from its tag then.

## Cutting a release

**From GitHub (easiest):** Actions tab → **Release** → **Run workflow**,
choose the bump and run. Patch is the default; minor resets patch to 0;
major resets minor and patch to 0 (1.4.2 → 1.4.3, 1.5.0 or 2.0.0). For the
first release, choose **minor**: 0.0.0 → 0.1.0. The workflow:

1. refuses to run from anything but `main`; waits up to 30 minutes for
   CI on that commit to finish (so you can run it right after merging),
   and stops if CI didn't pass;
2. runs `scripts/bump-version.sh` on a new `release/vX.Y.Z` branch: it
   finds the latest `vX.Y.Z` tag (none yet means 0.0.0), computes the next
   version, refuses if `## [Unreleased]` is empty, moves those entries
   under the new version with today's date, and sets the version in
   `pyproject.toml` and `uv.lock` (`uv version`);
3. opens a **Release vX.Y.Z** PR with the release notes, and approves the
   PR's CI and Lint runs (GitHub holds runs on PRs opened by a workflow
   until someone approves them). If it can't, the run shows a warning: open
   the PR and click **Approve and run workflows**.

Review the PR and merge it when the checks pass. Merging tags the merge
commit `vX.Y.Z` and runs the release steps below. To abandon a release,
close the PR; nothing is tagged.

**With Claude Code:** `/python-rules:release` proposes the bump from the
Unreleased entries, runs the workflow, and tells you when the PR is ready
to merge.

**By hand** (on a branch, through a PR like any other change):

1. Start from an up-to-date, green `main`.
2. Pick the bump from the Unreleased entries using the table above.
3. `scripts/bump-version.sh <patch|minor|major>` updates CHANGELOG.md,
   `pyproject.toml` and `uv.lock` and prints the new version.
4. Check: `scripts/changelog-section.sh X.Y.Z`, the tests and
   `docker compose -f docker-compose.prod.yaml build`.
5. Commit on a `release/vX.Y.Z` branch, push, and open a PR titled
   `Release vX.Y.Z`. Merging it tags and publishes, as above.

## What the release workflow does

`.github/workflows/release.yaml`, once the release PR merges (or on a tag
you pushed):

1. Checks the CHANGELOG section exists and `pyproject.toml`'s version
   equals the tag. Fails loudly otherwise; delete the tag, fix, re-tag.
2. Builds the Dockerfile's `production` stage for `linux/amd64` and
   `linux/arm64` and pushes it to `ghcr.io/<owner>/<repo>` as `X.Y.Z`,
   `X.Y`, `X` (from 1.0.0 on) and `latest`, with build provenance and an
   SBOM attached. A pre-release gets only its own tag.
3. Builds the sdist and wheel (`uv build`).
4. **If PyPI publishing is on** (below): `uv publish`. Files already on
   PyPI are skipped, so re-running a failed release is safe.
5. Creates the GitHub Release with the changelog section, the image
   reference (and PyPI link) as its notes and the sdist and wheel attached,
   so `pip install <wheel URL>` works whether or not the app is on PyPI.
   Marked pre-release if the tag has a `-suffix`.

The image and package are published before the Release is created, so a
Release always has them.

The first push creates the package on ghcr.io. For a public repo, check
the package's visibility under the repo's **Packages** → package
settings, and make it public if it isn't, so `docker pull` works without
logging in.

## Publishing to PyPI (optional)

Off by default: most apps are deployed as images, and a PyPI name is
public and permanent. Ask the owner first. To turn it on:

1. Check the name in `pyproject.toml` is free on https://pypi.org.
2. Authorize GitHub, one of:
   - **Trusted publishing (preferred, no secret):** on PyPI, add a
     publisher (for a new project, a "pending publisher") with this
     repo's owner and name, workflow `release.yaml`, no environment.
   - **API token:** create a project-scoped token on PyPI (for the very
     first upload it has to be account-scoped; replace it after) and store
     it as the repository secret `PYPI_API_TOKEN`
     (`gh secret set PYPI_API_TOKEN`).
3. Set the repository variable `PYPI_PUBLISH` to `true`
   (`gh variable set PYPI_PUBLISH --body true`).

The next release publishes. To publish by hand instead, put the token in
`UV_PUBLISH_TOKEN` (listed, commented out, in `.env.example`; keep it out
of `.env` on servers, which compose passes to the app), then `uv build`
and `uv publish`. Never commit a token.

## If a release goes wrong

- Release PR's checks fail: fix on a normal PR to `main`, close the release
  PR, delete its branch, and run the Release workflow again.
- Tagged, but the image, PyPI upload or Release wasn't created: fix the cause, then
  re-run the failed jobs of that Release run from the Actions tab.
- A bad release is already public: don't rewrite it or move its image
  tags. Release a patch (`X.Y.Z+1`) with the fix, and mark the bad one in
  its notes.
