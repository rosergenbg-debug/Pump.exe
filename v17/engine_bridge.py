"""Explicit frozen V16 execution bridge; no bytecode edits or monkey-patching.

V17 orchestration is source code. V16 remains a hashed, Python-3.13-only
compatibility dependency pending editable-source recovery.
"""
import hashlib
import importlib
import json
from pathlib import Path
import sys


def load_engine():
    if sys.version_info[:2] != (3, 13):
        raise RuntimeError("Recovered V16 engine requires Python 3.13")
    root = Path(__file__).resolve().parent.parent / "recovery_v16"
    compiled = root / "compiled"
    manifest = json.loads((root / "manifest.json").read_text(encoding="utf-8"))
    for record in manifest["modules"]:
        path = Path(*record["module"].split("."))
        path = path / "__init__.pyc" if record["package"] else path.with_suffix(".pyc")
        if hashlib.sha256((compiled / path).read_bytes()).hexdigest() != record["compiled_sha256"]:
            raise RuntimeError(f"V16 module integrity failure: {record['module']}")
    for name, module in tuple(sys.modules.items()):
        if name == "pump_research_lab" or name.startswith("pump_research_lab."):
            if not Path(module.__file__).resolve().is_relative_to(compiled.resolve()):
                raise RuntimeError("Another engine is already loaded; start an isolated process")
    if str(compiled) not in sys.path:
        sys.path.insert(0, str(compiled))
    return importlib.import_module("pump_research_lab.adaptive_optimizer")


def validate_rows(rows, label):
    if len(rows) < 2:
        raise ValueError(f"{label}: insufficient data")
    previous = None
    for row in rows:
        if previous is not None and row.open_time_ms - previous != 60_000:
            raise ValueError(f"{label}: discontinuity or duplicate candle")
        if row.close_time_ms != row.open_time_ms + 59_999:
            raise ValueError(f"{label}: not a closed one-minute candle interval")
        if not (0 < row.low <= min(row.open, row.close) <= max(row.open, row.close) <= row.high):
            raise ValueError(f"{label}: invalid OHLC")
        previous = row.open_time_ms


class EngineBridge:
    def __init__(self, rows, btc_rows, sol_rows):
        self.engine = load_engine()
        for data, label in [(rows, "PUMP"), (btc_rows, "BTC"), (sol_rows, "SOL")]:
            validate_rows(data, label)
        times = [r.open_time_ms for r in rows]
        if any([r.open_time_ms for r in data] != times for data in (btc_rows, sol_rows)):
            raise ValueError("PUMP/BTC/SOL periods must align exactly")
        self.rows = rows
        features = importlib.import_module("pump_research_lab.adaptive_features")
        self.features = features.build_feature_store(rows, btc_rows, sol_rows)

    def replay(self, parameters, capital=1000.0, legacy=False):
        if capital <= 0:
            raise ValueError("Capital must be positive")
        parameters = dict(parameters)
        if not legacy:
            # V16 has a verified explicit zero=unlimited branch, not a large cap.
            parameters["max_entries_per_utc_day"] = 0
            parameters["min_hours_between_entries"] = 0
        config = self.engine.EconomyConfig(**parameters)
        return self.engine.replay_adaptive(self.rows, self.features, config, 1,
                                           len(self.rows), capital, causal_order_gate=True)

