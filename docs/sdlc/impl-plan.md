# README Auto-Sync Implementation Plan

**Status:** Approved after HITM; implementation is in progress. This document records SDLC Step 4 and its approved execution plan.

## Prioritized Tasks

1. **Check GitHub PR-token policy (pre-implementation gate).** The user confirmed that workflows have read/write permissions and that the setting allowing `GITHUB_TOKEN` to create pull requests is enabled. If this policy changes, block PR publication and obtain an explicitly approved credential/policy decision before proceeding. Do not silently use a PAT or broaden workflow permissions. *Traceability: approved architecture Security and Permissions; design review Accepted Recommendation 1; requirement 7.*

2. **Add the minimal feature contract and tests.** Create `src/features.py` with `FEATURES = ["Create", "Update"]` and `features()` returning that configured list as a copy. Add a focused pytest test asserting both the configured names and function result. *Traceability: requirements 2-3; architecture Components and Responsibilities; user clarification during implementation.*

3. **Implement README synchronization and focused tests.** Add `scripts/sync_readme.py` to call `features()`, validate exactly one start marker and one end marker in start-before-end order before writing, render ordered `- name` items, and replace embedded line breaks in names with spaces. Permit empty lists and blank names. Test valid rendering, marker cardinality/order failures, no write on invalid input, and unchanged README content outside the marker-delimited region, including representative newline formatting. *Traceability: requirements 4-6 and Resolved Decisions; architecture Components, Workflow and Data Flow, and Failure Behavior; design review Accepted Recommendations 2-3.*

4. **Add the GitHub Actions workflow and PR publication configuration.** Create `.github/workflows/readme-auto-sync.yml` for pushes to `main` filtered to `src/features.py` only. Use Python 3.12, install pytest, run the complete suite before invoking the sync script, and prevent sync/publication after test or sync failure. Configure the publishing job with only `contents: write` and `pull-requests: write`, using `GITHUB_TOKEN`. Pin checkout v7.0.1, setup-python v7.0.0, and peter-evans/create-pull-request v8.1.1 to their reviewed immutable revisions. Configure same-repository head `docs/auto-update-readme` and base `main`; update the existing open PR rather than opening duplicates, and avoid empty commits or PR updates when there is no README diff. Use a concise conventional PR title/body summarizing the feature sync and test result. *Traceability: requirement 1, requirement 2, requirement 7, and Constraints; architecture Workflow and Data Flow, Failure Behavior, Security and Permissions, and Approved Decisions; design review Accepted Recommendation 4.*

5. **Perform implementation verification (after tasks 2-4).** Run pytest and verify the sync behavior for valid markers, preservation outside the markers, invalid-marker fail-before-write behavior, and no-diff behavior. Inspect the workflow configuration for the exact trigger/path filter, step ordering, token permissions, branch/base settings, action pin, and no-duplicate-PR behavior. Resolve failures before requesting code review or opening/merging any PR. *Traceability: requirements 1-7; architecture Workflow and Data Flow and Failure Behavior; design review Requirements Coverage and Accepted Recommendations 3-4.*

## Dependencies and Blockers

- Task 1 was satisfied by user confirmation before implementation. If the repository policy changes, block PR publication until an approved alternative is documented; do not substitute credentials or permissions by assumption.
- Task 3 depends on the `features()` contract in Task 2.
- Task 4 depends on Tasks 2 and 3 so the workflow can test and then invoke the implemented components.
- Task 5 depends on Tasks 2-4. It is a future implementation-stage activity and has not been run as part of this planning step.

## Approval Needed

- The plan and PR-creation policy were approved before implementation. The action selection is now resolved and pinned. Implementation changes are presented for HITM review before the code-review phase.
