# Design Review: README Auto-Sync

**Status:** Approved after HITM. The approved recommendations are reflected in `docs/sdlc/requirements.md` and `docs/sdlc/architecture.md`.

## Scope

Reviewed the proposed design in `docs/sdlc/architecture.md` against the approved requirements in `docs/sdlc/requirements.md`, focusing on requirements coverage, failure modes, security and permissions, maintainability, and unnecessary complexity. Implementation planning is handled as the next SDLC phase.

## Summary

The design is small and proportionate to the requested automation. It assigns clear responsibilities to the feature module, focused sync script, tests, and one workflow. The trigger, ordered validation-before-write behavior, managed README region, no-op handling, and PR-based publication cover the stated requirements. No blocking design gap was found, and the user-approved recommendations below are reflected in the requirements and architecture.

## Requirements Coverage

- The workflow is scoped to pushes on `main` that change only `src/features.py`, matching the approved trigger decision. Changes to workflow or sync code alone intentionally do not trigger it.
- Pytest runs before synchronization, so test failure prevents README and PR updates.
- `features()` supplies the runtime list; tests check its return shape and string values without fixing the example values.
- The sync script validates the complete marker set and order before writing, emits ordered Markdown bullets, and limits ownership to the marker-delimited content.
- The workflow publishes through `docs/auto-update-readme` with base `main`; the same head branch and PR action are intended to update rather than duplicate an open PR.
- No-diff publication is a no-op. Test, marker, synchronization, and publication failures are described without falling back to writing directly to `main`.
- Approved choices are represented: Python 3.12; concise conventional PR summary and test result because no repository templates exist; empty lists and blank feature names are permitted.

## Findings

### Blocking Issues

None identified in the proposed design.

### Accepted Recommendations

1. **Confirm GitHub Actions PR permission is enabled.** The `contents: write` and `pull-requests: write` job permissions are appropriately narrow, but repository or organization settings can separately disallow `GITHUB_TOKEN` from creating pull requests. Confirm that setting before relying on the automation. If policy forbids it, decide on an approved credential path before implementation; do not silently broaden permissions or use a personal access token.

2. **Make one-line rendering semantics explicit.** Embedded line breaks in a returned name are replaced with spaces so each name remains one Markdown list item. Empty lists and blank names remain valid.

3. **Test README preservation at the boundary.** Add focused sync tests that assert the bytes/text outside the marker-delimited interior are unchanged, including marker cardinality/order failures and representative newline formatting. This directly verifies the non-negotiable preservation and fail-before-write requirements without adding another framework.

4. **Specify branch update behavior in the chosen PR action configuration.** The architecture appropriately defers the exact maintained action, but implementation should verify it updates the same-repository `docs/auto-update-readme` head branch and the open PR targeting `main`, and does not create an empty commit when the rendered README is unchanged. Pin the action to a reviewed immutable revision as proposed.

## Maintainability and Complexity

The four-component split is justified: testable synchronization logic stays outside workflow YAML, and the workflow remains orchestration. No additional service, framework, or validation layer is warranted. Keep marker parsing and file writing in the focused script, with tests around its observable behavior; avoid adding generic templating or PR-management abstractions for this single use case.

## Decisions and HITM Approval

The user approved all four non-blocking recommendations. The implementation plan must include a preflight check that repository or organization policy permits `GITHUB_TOKEN` pull-request creation; one-bullet rendering with embedded line breaks replaced by spaces while allowing empty lists and blank names; tests for marker validity, no-write-on-failure, and unchanged README content outside markers; and PR-action configuration that reuses the same-repository `docs/auto-update-readme` branch and open PR to `main` without empty commits. The architecture and requirements now reflect these decisions. No additional architecture changes are pending.
