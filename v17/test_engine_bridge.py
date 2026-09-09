from dataclasses import replace
import importlib
import unittest
from engine_bridge import EngineBridge, load_engine


class BridgeTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.engine = load_engine()
        demo = importlib.import_module("pump_research_lab.demo")
        cls.rows = demo.demo_candles()
        cls.btc = [replace(row, symbol="BTCUSDT") for row in cls.rows]
        cls.sol = [replace(row, symbol="SOLUSDT") for row in cls.rows]
        cls.bridge = EngineBridge(cls.rows, cls.btc, cls.sol)

    def test_unmodified_v16_parity(self):
        config = self.engine.EconomyConfig()
        expected = self.engine.replay_adaptive(self.rows, self.bridge.features, config,
                                               1, len(self.rows), 1000, causal_order_gate=True)
        actual = self.bridge.replay({}, legacy=True)
        self.assertEqual(actual.to_dict(), expected.to_dict())

    def test_explicit_no_daily_quota(self):
        actual = self.bridge.replay({"max_entries_per_utc_day": 1, "min_hours_between_entries": 48})
        expected = self.engine.replay_adaptive(self.rows, self.bridge.features,
            self.engine.EconomyConfig(max_entries_per_utc_day=0, min_hours_between_entries=0),
            1, len(self.rows), 1000, causal_order_gate=True)
        self.assertEqual(actual.to_dict(), expected.to_dict())

    def test_missing_context_fails(self):
        with self.assertRaises(ValueError):
            EngineBridge(self.rows, [], self.sol)

    def test_gap_fails(self):
        with self.assertRaises(ValueError):
            EngineBridge(self.rows[:5] + self.rows[6:], self.btc, self.sol)

    def test_same_shape_wrong_dates_fails(self):
        shifted = [replace(r, open_time_ms=r.open_time_ms+60000, close_time_ms=r.close_time_ms+60000) for r in self.btc]
        with self.assertRaises(ValueError):
            EngineBridge(self.rows, shifted, self.sol)


if __name__ == "__main__":
    unittest.main()

