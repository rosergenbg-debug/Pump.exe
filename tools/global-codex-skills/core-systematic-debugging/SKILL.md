---
name: core-systematic-debugging
description: Use whenever any project crashes, behaves incorrectly, regresses, becomes flaky, produces suspicious data, or loses expected behavior. Requires reproduction, evidence, root-cause isolation, a minimal cause-level fix, regression protection when feasible, and verification of nearby invariants.
---

# Core Systematic Debugging

Use for bugs, crashes, wrong calculations, broken UI behavior, flaky tests, corrupted state, unexpected network behavior, performance regressions, and inconsistent outputs.

Project-local instructions and specialized debugging skills take priority.

## Sequence

### 1. Reproduce before editing

- Establish the exact failing behavior.
- Capture the smallest reliable reproduction: input, state, sequence, log, stack trace, failing test, trace, or deterministic dataset.
- If exact reproduction is impossible, identify the strongest evidence and mark what remains uncertain.

### 2. Find the first divergence

Trace the path from input to observed failure and locate where actual behavior first diverges from expected behavior.

Check as relevant:
- state ownership and lifecycle;
- parsing and serialization;
- persistence and migrations;
- threading, async work, races, or cancellation;
- API/network assumptions;
- units, currencies, timestamps, time zones, precision, or conversions;
- UI state and visibility;
- stale caches or duplicated state;
- configuration and environment differences;
- compatibility between old and new data or versions.

Do not change code until there is at least one evidence-backed root-cause hypothesis.

### 3. Test the hypothesis

Use a narrow experiment, assertion, temporary diagnostic, test, trace, or controlled replay that can distinguish the hypothesis from alternatives.

A plausible story is not evidence.

### 4. Fix the cause

- Make the smallest architecturally correct change that removes the cause.
- Do not merely swallow exceptions, hide failures, reset user state, widen timeouts, bypass safety checks, or disable validation unless that is genuinely the correct design.
- Avoid replacing a large working subsystem to repair one local bug.

### 5. Add regression protection

When practical, add or strengthen a test that would fail without the fix.

If a normal unit test cannot capture the issue, use an integration test, deterministic fixture, replay, invariant assertion, or documented verification procedure.

### 6. Check nearby invariants

Verify that the fix did not break the project's documented interfaces, persisted state, migrations, compatibility, security assumptions, build, or neighboring behavior.

### 7. Escalate repeated repairs

If the same area needs repeated fixes or the new fix repairs consequences of a previous fix, stop layering patches. Re-examine the original assumption, state ownership, architecture boundary, duplicated logic, and whether a small refactor is now safer.

## Completion

Before finishing, be able to state:
- reproduction;
- root cause;
- evidence;
- exact fix;
- regression protection;
- verification performed;
- remaining uncertainty.

Then apply `core-verification`.