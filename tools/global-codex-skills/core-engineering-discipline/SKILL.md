---
name: core-engineering-discipline
description: Generic fallback engineering discipline for code, architecture, refactoring, configuration, integration, or implementation changes when no more-specific project-local engineering skill covers the same work. Prevents unsupported assumptions, overengineering, scope creep, and accidental neighboring changes through repository evidence, focused diffs, and a verifiable goal.
---

# Core Engineering Discipline

Use this as a generic engineering guardrail **only when a more-specific project-local skill is not already covering the same discipline**. Do not stack this skill with a local equivalent merely to repeat the same rules. Repository instructions and local specializations take priority.

## Rules

1. **Do not guess when the project can answer.**
   - Read the relevant code, tests, schemas, configuration, documentation, and recent changes first.
   - If an important fact remains unknown, mark the assumption instead of silently treating it as true.

2. **Translate the request into an observable goal.**
   - Define what must be true when the task is complete.
   - Prefer concrete evidence: reproduced failure gone, test passing, build succeeding, expected output produced, data preserved, interface unchanged where required.

3. **Choose the simplest sufficient solution.**
   - Avoid new frameworks, services, abstractions, state layers, dependencies, or broad rewrites unless the existing design cannot safely support the requirement.
   - Simple does not mean fragile. Prefer the smallest architecturally correct change.

4. **Keep scope tight.**
   - Do not clean up unrelated code merely because it looks improvable.
   - Preserve unrelated behavior, interfaces, persisted data, configuration, and compatibility unless the task requires changing them.

5. **Make every changed file explainable.**
   - Each change must directly support the requested behavior, a necessary test, migration, documentation update, or required integration.
   - If a change cannot be justified, leave it out.

6. **Respect project specialization.**
   - If the repository provides `AGENTS.md`, local skills, architecture decisions, migration rules, or regression tests, treat them as authoritative for that project.
   - Prefer a project-local specialized skill over this generic one when both cover the same area.

7. **Prove the result.**
   - Use the project's local verification skill/procedure when present; otherwise use `core-verification`.

## Completion question

Before finishing, be able to answer: **What evidence proves that I solved exactly the requested problem without silently changing unrelated behavior?**
