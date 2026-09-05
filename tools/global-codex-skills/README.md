# Global Codex Skills — Serge

This folder is the canonical source for Serge's user-wide Codex skill system.

## What is global

Installed once into `%USERPROFILE%\.agents\skills\`:

- `skill-orchestrator`
- `core-engineering-discipline`
- `core-systematic-debugging`
- `core-tdd-review`
- `core-verification`

The installer also merges the marked self-organization policy into `%USERPROFILE%\.codex\AGENTS.md` (or `$env:CODEX_HOME\AGENTS.md`). Existing unrelated global instructions are preserved.

## Official OpenAI tools

### Plugin Eval

The system intentionally installs **only the official OpenAI `plugin-eval` CLI**, not the whole Plugin Eval chat-plugin bundle. This avoids adding another set of automatically-triggered skills that could overlap with `skill-orchestrator`.

Source: `https://github.com/openai/plugins/tree/main/plugins/plugin-eval`.

The installer keeps a sparse official checkout under:

`%USERPROFILE%\.agents\vendor\openai-plugins\plugins\plugin-eval`

and uses `npm link` to expose the `plugin-eval` command. OpenAI requires Node.js >=20, npm, and Git. If those prerequisites are missing, the installer skips Plugin Eval without breaking the core skill system.

Default policy is deliberately cheap and bounded:

- new/materially changed skill/plugin -> at most one local `plugin-eval analyze` pass per changed target;
- `explain-budget` only when context/token size is relevant;
- no automatic `plugin-eval start`, benchmark initialization, or live `benchmark`;
- live Codex benchmarks require an explicit owner request;
- no evaluate -> rewrite -> evaluate loop.

### Codex Security

Codex Security is installed/enabled only through the **official OpenAI plugin directory**. It is intentionally not side-loaded by the PowerShell installer.

Default policy:

- use only for explicit security work or security-sensitive changes (auth, secrets, untrusted input, network/API boundaries, persistent storage, permissions, dependency/security updates, signing/update chain, executable downloads, or a justified release gate);
- prefer a final-diff scan for normal security-sensitive changes;
- no scan for cosmetic/unrelated small edits;
- one scan by default, with at most one verification re-scan if an actionable finding caused a code change;
- full/deep scans only for explicit audits, major security work, or justified major-release checks.

## Windows installation/update

From a local checkout:

```powershell
powershell -ExecutionPolicy Bypass -File .\tools\global-codex-skills\install-global-skills.ps1
```

The script is idempotent: rerunning it updates the five managed skills, refreshes only the marked global policy block, and updates/installs the official Plugin Eval CLI when prerequisites are available.

To update only the core system and skip Plugin Eval setup:

```powershell
powershell -ExecutionPolicy Bypass -File .\tools\global-codex-skills\install-global-skills.ps1 -SkipPluginEval
```

Start a new Codex session or restart Codex if the current session does not reload the new instructions.

## Design rules

Global skills are **not copied into every repository**. Repositories contain only project-specific skills, for example `.agents/skills/<project-specific-name>/SKILL.md`.

The global `skill-orchestrator` notices when a reusable project-specific workflow is justified and may create a concise safe text-only local skill automatically. It checks for overlap first and keeps the total set small.

External tools with executable code, hooks, MCP/network access, credentials, package installation, new permissions, or persistent global configuration changes require owner approval unless that exact integration was already explicitly approved.

## Anti-loop / credit guardrails

- one orchestration pass per task unless scope materially changes;
- no recursive orchestrator calls;
- no repeated tool/skill calls on unchanged inputs;
- single-agent by default for skill management;
- deterministic/local checks before model-consuming benchmarks;
- Plugin Eval live benchmarks never automatic;
- Codex Security scans bounded to one final scan + at most one verification re-scan after an actual security fix;
- existing test/build/scan evidence is reused rather than rerun without reason.

## PUMP

PUMP keeps its PUMP-specific local skills because they contain PUMP-specific invariants and project memory. Generic global skills do not replace those specialized local rules; project-local specialization wins for its scope.
