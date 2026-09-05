# Global Codex Skills — Serge

This folder is the canonical source for Serge's user-wide Codex skill system.

## What is global

These skills are intended to be installed once into:

`%USERPROFILE%\.agents\skills\`

- `skill-orchestrator`
- `core-engineering-discipline`
- `core-systematic-debugging`
- `core-tdd-review`
- `core-verification`

The installer also merges the self-organization policy into the user's global Codex instructions:

`%USERPROFILE%\.codex\AGENTS.md`

(or `$env:CODEX_HOME\AGENTS.md` when `CODEX_HOME` is set).

## One-time installation on Windows

From a local checkout of this repository:

```powershell
powershell -ExecutionPolicy Bypass -File .\tools\global-codex-skills\install-global-skills.ps1
```

The script installs/updates the five managed global skills and adds or refreshes only the marked `SERGE_GLOBAL_SKILL_POLICY` block in the global `AGENTS.md`; existing unrelated global instructions are preserved.

After installation, start a new Codex session if the current session does not show the new skills.

## Design rule

Global skills are **not copied into every repository**. They are available user-wide.

A repository should contain only project-specific skills, for example:

`.agents/skills/<project-specific-name>/SKILL.md`

The global `skill-orchestrator` is responsible for noticing when a reusable project-specific workflow is justified and creating a concise safe text-only local skill automatically. External skills with executable code, hooks, MCP/network access, credentials, package installation, new permissions, or persistent global configuration changes require owner approval before installation.

## PUMP

PUMP keeps its PUMP-specific local skills because they contain PUMP-specific invariants and project memory. The generic global skills do not replace those specialized local rules; project-local specialization wins for its scope.