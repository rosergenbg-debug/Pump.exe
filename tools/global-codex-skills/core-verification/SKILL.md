---
name: core-verification
description: Generic fallback verification-before-completion protocol when no more-specific project-local verification/release skill covers the same claim. Use before claiming code is fixed, complete, tested, ready, built, packaged, released, migrated, or otherwise successful; require direct evidence and distinguish verified, inspected, not-run, and uncertain states.
---

# Core Verification Before Completion

Use this generic verification skill **only when no more-specific project-local verification/release skill already covers the same completion claim**. Do not stack it with a local equivalent merely to repeat the same evidence checks.

Do not use confidence, code inspection, or a plausible explanation as a substitute for evidence. Project-local release/check procedures take priority.

## Match evidence to the claim

Before saying something is complete, identify the exact claim and obtain evidence that can actually prove it.

Examples:
- **bug fixed** -> reproduce the old failure path and show corrected behavior or a passing regression test;
- **tests pass** -> run the relevant tests and inspect the result;
- **build succeeds** -> run the actual build command and confirm success;
- **artifact ready** -> inspect the generated artifact, path/name/version/package/signature or other project-required properties;
- **migration safe** -> verify representative old data/state can be read or migrated without loss;
- **release ready** -> satisfy the repository's documented release checklist, not merely a debug build;
- **performance improved** -> compare a meaningful measurement against a baseline;
- **algorithm improved** -> compare required metrics on an appropriate controlled dataset, not one favorable example.

## Verification ladder

Use the strongest feasible relevant evidence, roughly:

1. direct reproduction/acceptance check;
2. focused automated test;
3. relevant broader regression suite;
4. static/lint/type checks;
5. actual build/package step;
6. artifact inspection;
7. manual inspection only when automation is not reasonably available.

Do not perform meaningless checks just to make the list longer, and do not rerun expensive checks when valid evidence from the same final state already exists.

## Never blur these states

Keep these statements distinct:

- **verified/passed** — actually executed and observed;
- **inspected** — reasoned from code or files but not executed;
- **not run** — unavailable, blocked, too expensive, or outside the environment;
- **uncertain** — evidence is incomplete or conflicting.

Never report an unrun check as passed.

## Final completion check

Before final status, confirm:

- the requested behavior is addressed;
- relevant tests/checks/builds actually ran when feasible;
- important project invariants remain intact;
- the final diff/artifact corresponds to what was verified;
- unresolved limitations are stated plainly.

Only then claim completion.
