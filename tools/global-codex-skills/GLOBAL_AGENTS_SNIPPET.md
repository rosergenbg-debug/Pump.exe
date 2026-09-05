<!-- SERGE_GLOBAL_SKILL_POLICY_BEGIN -->
# Global working policy — skill self-organization

These are the owner's default rules for all Codex projects. More-specific repository instructions (`AGENTS.md`, nested overrides, project-local skills, tests, and explicit owner decisions) take priority for their scope.

## Skill organization

The owner should not have to manually remember, copy, or install the same skills for every new project.

For substantial **new** projects/workstreams or when skill organization itself needs maintenance:

1. Use `skill-orchestrator` when reusable workflow organization is relevant.
2. In an established project that already has a project-local coordinator/skill policy, do **not** load `skill-orchestrator` for every ordinary task; defer to the local system unless skills themselves need work.
3. Reuse the user-level core skills only when they match the task **and no project-local equivalent already covers the same work**:
   - `core-engineering-discipline`
   - `core-systematic-debugging`
   - `core-tdd-review`
   - `core-verification`
4. Do **not** copy these global skills into repositories; they already apply user-wide.
5. Prefer a project-local specialization when it covers the same area more specifically.
6. Create concise text-only project skills automatically only for stable project-specific workflows, repeated failure modes, domain invariants, or recurring specialized procedures.
7. Do not create skills for trivial one-off tasks or duplicate an existing skill under another name.
8. Keep `AGENTS.md` concise; move long conditional procedures into focused local skills.
9. Mention newly created local skills in the work summary, but do not make the owner administer them manually.

## Cost and loop control

- Perform one orchestration decision pass per task unless scope materially changes.
- Never recursively invoke `skill-orchestrator` from itself.
- Do not rerun the same skill/tool on unchanged inputs.
- Default to one agent; do not create subagents merely to select/evaluate skills.
- Prefer deterministic local checks over live model benchmarks.
- Reuse test/build/scan evidence instead of repeating expensive verification without cause.

## Official OpenAI Plugin Eval

When the official OpenAI `plugin-eval` CLI is available:

- for a new or materially changed non-trivial skill/plugin, run at most one `plugin-eval analyze <path> --format markdown` per changed target per task;
- use `explain-budget` only when token/context size matters;
- do not automatically run `plugin-eval start`, `init-benchmark`, or `benchmark` for routine checks;
- live benchmarks require an explicit owner request because they may consume Codex credits;
- do not automatically evaluate the orchestrator merely because it executed;
- never create an evaluate -> rewrite -> evaluate loop.

If Plugin Eval is unavailable, use normal static review and continue; do not substitute an unknown plugin silently.

## Official OpenAI Codex Security

When Codex Security is installed, use it only for explicit security work or security-sensitive changes such as auth, secrets, untrusted input, network/API boundaries, persistent storage, permissions, dependency/security updates, signing/update chains, executable downloads, or justified release gates.

- Prefer one final-diff security scan for ordinary security-sensitive work.
- Do not scan cosmetic or unrelated small edits.
- Allow one verification re-scan only if the first scan produced an actionable finding and the code changed to fix it.
- Do not create scan -> fix -> scan loops.
- Full/deep scans are for explicit audits, major security work, or justified major-release checks.

## External skill safety

Do not blindly install external bundles or `--skill '*'` collections. Audit `SKILL.md`, referenced scripts/hooks, MCP/API configuration, network calls, permissions, and data access. Prefer a small audited text-only adaptation when enough.

A safe instruction-only project skill may be created automatically. External tools that execute code, add hooks, contact services, use credentials, install packages, change persistent global configuration, or grant permissions require explicit owner approval unless that exact integration has already been explicitly approved.

## New-project bootstrap

When the owner begins a genuinely new non-trivial project:

- inspect repository and existing instructions;
- use global skills without copying them;
- create concise repository `AGENTS.md` only when durable project rules are needed;
- create only already-justified project-specific skills;
- add/refine local skills as repeated workflows and failure patterns emerge;
- keep the total skill set small, non-overlapping, and useful.

The normal owner experience should be: describe the project goal, not administer the skill system.
<!-- SERGE_GLOBAL_SKILL_POLICY_END -->