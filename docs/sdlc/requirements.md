# README Auto-Sync Requirements

**Status:** Approved after HITM. This document covers SDLC Step 1 only.

## Source and Goal

Source: Confluence page **README Auto-Sync** (page `16842753`).

As a developer, I want a GitHub Actions workflow to update the feature list in `README.md` whenever `src/features.py` changes on `main`.

## Functional Requirements

1. The workflow shall trigger only for pushes to `main` that modify `src/features.py`.
2. The workflow shall run `pytest` to validate the feature list returned by `features()`. If any test fails, the workflow shall abort immediately and make no README update.
3. The repository shall provide a minimal `src/features.py` module defining `features()`, which returns the configured feature names as a list. The initial configured names are `Create` and `Update`; future feature changes are made through the source list.
4. After tests pass, the workflow shall call `features()` and replace only the text strictly between `<!-- docs-sync: start -->` and `<!-- docs-sync: end -->` in `README.md`.
5. If the required markers are missing or misplaced, the workflow shall fail immediately without updating the README.
6. All README content outside the marker-delimited region shall remain unchanged.
7. The workflow shall commit the updated README on the `docs/auto-update-readme` feature branch and open a pull request, or update the existing open pull request, without creating duplicate pull requests.

## Constraints and Non-Functional Requirements

- The automation is limited to the specified push trigger and feature-list update; it shall not modify README content outside the sync markers.
- Test failure and invalid marker placement are fail-fast conditions; neither may proceed to a README update or pull request update.
- Changes are proposed through the named feature branch and pull request rather than written directly to `main`.
- The README contains the expected sync markers. The source module and pytest tests were absent at the start of implementation and are included in scope.

## Assumptions

- `features()` is the source of the feature names, and the names to publish are whatever that function returns at runtime.
- Pytest tests are to validate the feature list returned by `features()`; no additional test or validation framework is required by this story.
- The branch name for the proposed README update is exactly `docs/auto-update-readme`.

## Resolved Decisions

- Render each feature returned by `features()` as one Markdown list item, matching the example in the user story (for example, `- feature name`). Preserve the returned order and replace embedded line breaks in a name with spaces so each name remains one list item. Empty lists and blank names are valid.
- The README is valid only when it contains exactly one start marker and exactly one end marker, with the start marker appearing before the end marker. Missing, duplicated, or reversed markers are invalid; the workflow shall fail before changing the README.
