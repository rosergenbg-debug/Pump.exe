# V17 development checkpoint — 2026-09-09

Not a release. No V17 EXE has been built. V16 originals remain untouched.

Implemented and tested: finite lazy candidate space, exact totals (including
spaces larger than 64-bit integers), block/total separation, SQLite durable
checkpoint, single committed result per candidate, persistent pause, interrupted
task recovery, terminal errors, current-run/version/data-only leader selection.
11 unit tests pass using Python 3.13. No trading/profitability claim follows.

Latest owner requirements supersede old endless-generation behavior: one pass
through a frozen space, adaptive ordering without infinite expansion, automatic
completion when every member is resolved. Errors are reported separately.
Crash recovery may rerun an uncommitted task, never a committed result.

Remaining: source reconstruction/parity for V16, integration with its evaluator
and process pool, removal of frequency quotas in V17 evaluator/search, full-history
data preparation and causal validation, modern non-blue GUI, version filtering
and header sorting, live plot restricted to current run, display-only 20% filter,
integration tests, two reviews, EXE packaging and launch.

Local V16 recovery is in ../recovery_v16. GitHub preservation branch:
recovery/v16-20260909. Do not label compiled recovery as editable source.

Run tests from this directory: python -m unittest -v test_run_control

