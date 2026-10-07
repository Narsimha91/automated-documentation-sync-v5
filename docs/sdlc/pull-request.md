# Pull Request Draft

**Status:** Submitted as [PR #1](https://github.com/Narsimha91/automated-documentation-sync-v5/pull/1) from `feature/readme-auto-sync` to `main`.

**Title:** `feat: automate README feature-list sync`

## Summary

Add a GitHub Actions workflow that tests and synchronizes the README feature list when `src/features.py` changes on `main`. The workflow updates the managed marker region through `docs/auto-update-readme` and opens or updates a pull request instead of writing directly to `main`.

## Changes Made

- `.github/workflows/readme-auto-sync.yml` — run the Python 3.12 test suite for the approved push/path trigger, synchronize the README after tests pass, and publish changes using the designated feature branch and PR action.
- `scripts/sync_readme.py` — render ordered feature bullets, validate marker uniqueness and order before writing, preserve content outside the managed region, and skip writes when unchanged.
- `src/features.py` — provide the configured `Create` and `Update` feature names through `features()`.
- `tests/test_features.py` — verify the configured feature values and function result.
- `tests/test_sync_readme.py` — cover rendering, marker failures, preservation, and no-write behavior.

`README.md` is intentionally excluded from this draft's claimed changes. The current checkout has a pre-existing user modification to that file; it was left untouched and is not represented as part of this work.

## Test Evidence

Recorded verification from [tests/results/test_results.md](../../tests/results/test_results.md):

```text
Command: python -m pytest
Runtime: Python 3.12.10 (isolated temporary virtual environment)
Result: 11 tests passed
```

The record also documents a disposable-file integration check using the actual `features()` output: the `Create` and `Update` bullets were generated, bytes outside the marker region were preserved, and a second sync reported no change. Workflow configuration was inspected against the approved trigger, ordering, permissions, and branch/base requirements.

## Known Limitations

- The GitHub Actions workflow was not executed on GitHub. Action execution, repository permissions at runtime, and live pull-request creation or update behavior remain unverified.
- The code review's low-severity recommendation to pin pytest was explicitly deferred; the workflow currently installs pytest without a version pin.

## Reviewer Checklist

- [ ] Confirm the workflow triggers only on pushes to `main` that modify `src/features.py`.
- [ ] Confirm pytest completes before README synchronization and publication.
- [ ] Confirm invalid markers fail before any README write and content outside the markers remains unchanged.
- [ ] Confirm workflow permissions, action pins, feature branch, and `main` PR base match the approved design.
- [ ] Confirm `README.md` contains no unrelated or pre-existing change in the submitted PR.
- [ ] Review the recorded Python 3.12.10 verification and account for the GitHub runtime limitations above.

## Approval Gate

Final HITM approval was received before submission. PR #1 is open and ready to merge.