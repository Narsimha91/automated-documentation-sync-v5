# Proposed Architecture: README Auto-Sync

**Status:** Proposed for HITM approval. This document covers SDLC Step 2 only.

## Overview

Use a small Python feature module and pytest tests, orchestrated by one GitHub Actions workflow. After tests pass, a focused sync script renders the runtime feature names into the README marker region. The workflow publishes the README change on `docs/auto-update-readme` and creates or updates one pull request targeting `main`.

## Chosen Stack

- Python for the feature list and README synchronization logic.
- `pytest` for the feature-list contract tests.
- GitHub Actions for push filtering, ordered validation/synchronization, and publishing.
- A maintained pull-request action (pinned to a reviewed version or commit) to push the feature branch and create/update its pull request without duplicates.

No application framework, database, or additional service is needed.

## Components and Responsibilities

- `src/features.py`: defines `features()` and returns the current feature names as a list of strings. The runtime values, not example names, are authoritative.
- `tests/`: contains focused pytest tests for the return shape and string-valued feature names without hard-coding example names. Sync tests verify marker validation, newline rendering, preservation outside the markers, and no write on invalid input.
- `scripts/sync_readme.py`: calls `features()`, validates exactly one start and one end marker in the required order, formats names as ordered Markdown bullets, replacing embedded line breaks with spaces, and replaces only the content between the markers. It must validate the full marker set before writing anything.
- `.github/workflows/readme-auto-sync.yml`: runs only on pushes to `main` that include `src/features.py`; sets up Python 3.12, installs pytest, runs the complete test suite, then invokes the sync script, and publishes the resulting README change through the feature branch and pull request.
- `README.md`: remains the human-maintained document outside the marker-delimited region. Automation owns only the text between the markers.

## Workflow and Data Flow

1. A push to `main` that changes `src/features.py` starts the workflow; other events and paths do not.
2. The job checks out the pushed revision and prepares Python 3.12 and pytest.
3. `pytest` runs before any README-writing step. Any test failure stops the job, so the README and pull request are not updated.
4. The sync script imports and calls `features()`. Before writing, it checks that the README contains exactly one of each marker and that the start marker precedes the end marker. It renders each returned name as one `- feature name` bullet in returned order, replacing embedded line breaks with spaces, and replaces only the strict interior region.
5. Invalid markers or synchronization errors fail the job before publication. If the rendered README has no changes, publication is a no-op.
6. For a change, the workflow uses a pinned PR action configured to update the same-repository `docs/auto-update-readme` head branch and its pull request with base `main`; it must not create an empty commit or a duplicate open PR.

## Failure Behavior

- Test failure: fail immediately; do not invoke the README sync or PR publication steps.
- Missing, duplicated, or reversed markers: fail before writing `README.md` or publishing a branch update.
- Feature import, rendering, or file errors: fail the job; do not publish a PR update.
- No README diff: do not create an empty commit or duplicate PR.
- GitHub publication permission or API errors: fail the workflow and report the failed publishing step; leave the change for a later rerun rather than attempting a direct write to `main`.

## Security and Permissions

- Limit workflow permissions to `contents: write` and `pull-requests: write`, scoped to the job that publishes changes; grant no broader repository or organization permissions.
- Use the repository-provided `GITHUB_TOKEN`; do not introduce personal access tokens or external secrets for this flow.
- Before relying on pull-request creation, verify repository or organization settings allow `GITHUB_TOKEN` to create pull requests. If policy disables it, stop and agree on an approved credential path before implementation; do not silently broaden permissions or use a personal access token.
- Pin third-party actions to a reviewed immutable commit where practical, and pass only the required token and branch/base settings.
- Keep the automation trigger restricted to the required `main` push path, and publish exclusively through the named feature branch and PR.

## Approved Decisions

- Confirmed: use Python 3.12.
- Confirmed: target the pull request to `main` and update the open pull request for head branch `docs/auto-update-readme`. The repository currently has no workflow or pull-request template to follow, so use a conventional concise title and body with a feature-sync summary and test result.
- Confirmed: empty feature lists and blank feature names are valid; validation should not impose additional content restrictions.
- Confirmed: keep the trigger limited to pushes to `main` that modify `src/features.py`. Changes to the workflow or sync script alone will not trigger this workflow.
