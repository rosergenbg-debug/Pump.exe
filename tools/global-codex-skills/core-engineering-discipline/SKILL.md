---
name: core-engineering-discipline
description: Use for code, architecture, refactoring, configuration, integration, or implementation changes in any project. Prevents unsupported assumptions, overengineering, scope creep, and accidental neighboring changes by requiring repository evidence, a verifiable goal, the simplest sufficient design, and focused diffs.
---

# Core Engineering Discipline

Use this as a generic engineering guardrail. More-specific repository instructions and project-local skills take priority.

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
   - Use `core-verification` before claiming the task is finished.

## Completion question

Before finishing, be able to answer: **What evidence proves that I solved exactly the requested problem without silently changing unrelated behavior?**