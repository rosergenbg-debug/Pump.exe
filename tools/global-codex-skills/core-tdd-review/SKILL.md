---
name: core-tdd-review
description: Generic fallback TDD and focused-review protocol for non-trivial behavior changes, risky fixes, algorithms, persistence, migrations, public interfaces, calculations, or regressions when no more-specific project-local test/review skill covers the same work. Uses pragmatic tests as evidence without forcing ceremony on trivial edits.
---

# Core TDD and Focused Review

Use testing as evidence, not ritual. Apply this generic skill **only when no more-specific project-local test/review skill already covers the same change**. Do not stack it with a local equivalent merely to repeat the same checklist.

Project-local test conventions and specialized skills take priority.

## When to use

Apply when a change can silently break behavior, data, compatibility, calculations, state transitions, concurrency, public interfaces, or a previously fixed regression.

Do not force a new test suite onto a tiny one-off text/configuration edit when no meaningful executable behavior is involved.

## Test-first workflow

1. Identify the behavior or invariant that must change or remain protected.
2. Find the closest existing test level that can prove it: unit, integration, end-to-end, deterministic replay, fixture, contract test, or build-time assertion.
3. When practical, add or modify a test so it fails for the old/broken behavior for the correct reason.
4. Implement the smallest sufficient change.
5. Make the focused test pass.
6. Run the relevant surrounding suite to catch regressions.

Prefer behavioral assertions over tests coupled to implementation details.

## Test quality

A useful test should:
- prove a meaningful requirement or regression;
- be deterministic enough to trust;
- fail for a useful reason;
- avoid depending on irrelevant formatting or internal structure;
- preserve important compatibility and data invariants when applicable.

Do not create a fake sense of safety with assertions that cannot fail under the broken condition.

## Focused code review after implementation

Review the final diff as if it came from another engineer. Check specifically for:

- incorrect assumptions;
- unintended scope expansion;
- missing error paths;
- data loss or migration risk;
- compatibility or interface breaks;
- race conditions and lifecycle issues;
- security/privacy regressions;
- unit/precision/time-zone/conversion mistakes;
- unnecessary dependencies or abstractions;
- tests that pass without proving the requested behavior;
- stale comments/documentation contradicted by the code.

Fix substantive issues found by the review, then rerun only the affected verification.

## Completion

Use the project's local verification skill/procedure when present; otherwise use `core-verification`.
