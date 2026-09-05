<!-- SERGE_GLOBAL_SKILL_POLICY_BEGIN -->
# Global working policy — skill self-organization

These are the owner's default rules for all Codex projects. More-specific repository instructions (`AGENTS.md`, nested overrides, project-local skills, tests, and explicit owner decisions) take priority for their scope.

## Skill organization

The owner should not have to manually remember, copy, or install the same skills for every new project.

For every substantial new project, workstream, or recurring workflow:

1. Consider the user-level skill `skill-orchestrator` and follow it when relevant.
2. Reuse the user-level core skills automatically when they match the task:
   - `core-engineering-discipline`
   - `core-systematic-debugging`
   - `core-tdd-review`
   - `core-verification`
3. Do **not** copy these global core skills into each repository. They already apply user-wide.
4. Inspect project-local `.agents/skills/` and prefer a project-local specialization over a generic global skill when both cover the same work.
5. When a non-trivial project develops a stable project-specific workflow, repeated failure mode, important domain invariant, or specialized recurring procedure, create a concise text-only project skill under `.agents/skills/<name>/SKILL.md` automatically when the benefit is clear.
6. Do not create skills for trivial one-off tasks or duplicate existing instructions.
7. Keep `AGENTS.md` concise. If a long instruction applies only to one class of tasks, prefer a focused project-local skill.
8. Mention newly created project-local skills in the work summary so the owner knows what was organized, but do not require the owner to request the skill manually.

## External skill safety

Do not blindly install external skill bundles or `--skill '*'` collections.

Before adopting an external skill, audit its `SKILL.md` and all referenced scripts, hooks, MCP/API configuration, network calls, permissions, and data access. Prefer a small audited text-only adaptation when that is enough.

A safe instruction-only project skill may be created automatically. Explicit owner approval is required before installing or enabling an external skill that executes code, adds hooks, contacts external services, uses credentials, changes persistent global configuration, installs packages, or grants new permissions.

## New-project bootstrap

When the owner begins a genuinely new non-trivial project, treat agent organization as part of the project setup:

- inspect the repository and existing instructions;
- use global skills without copying them;
- create a concise repository `AGENTS.md` if durable project rules are needed and no adequate one exists;
- create only the project-specific skills already justified by the work;
- add or refine project skills later as repeated workflows and failure patterns become clear;
- keep the skill set small, non-overlapping, and useful.

The normal experience for the owner should be: describe the project goal, not administer the skill system.
<!-- SERGE_GLOBAL_SKILL_POLICY_END -->