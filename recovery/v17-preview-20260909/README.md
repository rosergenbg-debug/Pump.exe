# V17 working preview checkpoint — 2026-09-09

This is a working PREVIEW, not the complete requested V17 release. Do not delete
or replace V16. README_PREVIEW_RU.md states the user-facing limitations.

## Provenance and protected data

Original V16 and datasets remain unchanged at `F:\PUMP Research Lab`.
The bridge verifies all 34 recovered Python 3.13 compiled modules against
`../recovery_v16/manifest.json`. This is preserved compiled code, not a claim of
fully reconstructed editable V16 source. Synthetic legacy parity passes.
GitHub preservation branch: `recovery/v16-20260909` in `rosergenbg-debug/Pump.exe`.

## Implemented in the running preview

- Native PySide6 desktop with graphite/amber theme, research and database tabs.
- Inventory of existing F: datasets; selected PUMP/BTC/SOL files must align.
- Actual V16 causal replay in two separate Windows CPU worker processes.
- V17 removes daily entry quota and mandatory entry cooldown.
- Optuna 4.5 TPE plus exploratory proposals; effective-parameter deduplication.
- Family-level heuristic stagnation and exploration recheck; automatic stop.
  This is not an exhaustive search or a proof of global optimality.
- Per-candidate immutable JSON, persistent campaign/study and live report.
- Cooperative pause drains current work; normal resume does not repeat saved work.
- Leader/curve restricted to the active run, version and dataset identity.
- V12–V16 read-only archive, version/NET filters, global numeric sorting,
  500-row display pages and parameter details. Display paging is not a search cap.

## Verification actually performed

37 automated tests passed, including actual Windows spawn replay, pause/resume,
synthetic legacy parity, input alignment, durable records and presentation rules.
Two separate runs of the packaged EXE self-test passed: each completed one
synthetic candidate and verified that repeat execution did not recalculate it.
See packaged-final-1/smoke.json and packaged-final-2/smoke.json in the local build.
These are execution tests, NOT profitability evidence or a clean-machine test.

## Remaining before calling this a completed V17

- Automatic download/merge of full available annual history.
- Independent chronological validation/final TEST in the new execution pipeline;
  present NET is explicitly DEVELOPMENT_ONLY_NOT_INDEPENDENT_TEST.
- Connect verified incremental replay to patient candidate-level pruning.
  Currently every proposed candidate is fully evaluated. Configured Optuna pruner
  is not used by CampaignRunner; do not describe it as active early pruning.
- Full abrupt-crash/orphan reconciliation and large-campaign storage optimization.
- Hardware-adaptive CPU settings and telemetry. GPU is not used in this preview.
- Complete source reconstruction and broader real-history regression validation.
- Old V11 library integration; current archive reads experiment stores V12–V16.

No real-order capability or guarantee of positive returns is present.
Do not reintroduce trade-frequency targets or silently substitute an older leader.

## Reproduction

Use Python 3.13 and retain sibling `v17` / `recovery_v16` directories.
Runtime dependencies: PySide6 6.9.3, Optuna 4.5.0, NumPy, DuckDB, psutil;
build dependency: PyInstaller 6.16.0. Run from `v17`:

```
python -m unittest discover -q
python -m PyInstaller --noconfirm --distpath ./dist --workpath ./build PumpResearchLab-V17-preview.spec
```

Run the entire onedir package, not the EXE separated from `_internal`.
`--self-test OUTPUT_DIRECTORY` performs an offline synthetic packaged check.
Never use the user's real research directory as the self-test output.

