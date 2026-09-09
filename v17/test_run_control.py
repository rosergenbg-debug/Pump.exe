import tempfile
import unittest
from pathlib import Path
from run_control import RunStore, Space


class RunTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.path = Path(self.tmp.name) / "run.sqlite3"
        self.space = Space.create({"target": [0.02, 0.1], "stop": [-0.02, -0.04]})
        self.context = dict(version="17", run_id="test", dataset_sha256="fixture", engine="fixture", evaluation="development")
        self.store = RunStore(self.path, self.space, self.context)

    def tearDown(self):
        self.store.close()
        self.tmp.cleanup()

    def result(self, task, net=0.1):
        return dict(context=self.context, parameters=task["parameters"], net=net)

    def test_once_and_auto_completion(self):
        self.store.prioritize([3, 3, 1])
        seen = []
        while tasks := self.store.claim(2):
            for task in tasks:
                seen.append(task["index"])
                self.store.finish(task, self.result(task))
        self.assertEqual(sorted(seen), [0, 1, 2, 3])
        self.assertEqual(self.store.progress()["state"], "COMPLETED")
        self.assertEqual(self.store.claim(), [])

    def test_resume_keeps_done_and_rejects_old_worker(self):
        a, b = self.store.claim(2)
        self.store.finish(a, self.result(a))
        self.store.pause()
        self.store.close()
        self.store = RunStore(self.path, self.space, self.context)
        self.assertEqual(self.store.claim(), [])
        self.store.recover_interrupted()
        self.store.resume()
        tasks = self.store.claim()
        self.assertNotIn(a["index"], [t["index"] for t in tasks])
        with self.assertRaises(ValueError):
            self.store.finish(b, self.result(b))

    def test_duplicate_result_rejected(self):
        task = self.store.claim(1)[0]
        self.store.finish(task, self.result(task))
        with self.assertRaises(ValueError):
            self.store.finish(task, self.result(task, 9))

    def test_old_version_cannot_be_current_leader(self):
        self.assertIsNone(self.store.best())
        task = self.store.claim(1)[0]
        result = self.result(task)
        result["context"] = dict(self.context, version="11")
        with self.assertRaises(ValueError):
            self.store.finish(task, result)
        self.assertIsNone(self.store.best())

    def test_best_never_replaced_by_worse(self):
        a, b = self.store.claim(2)
        self.store.finish(a, self.result(a, 0.4))
        self.store.finish(b, self.result(b, 0.3))
        self.assertEqual(self.store.best()["net"], 0.4)

    def test_errors_are_terminal_not_successful(self):
        for task in self.store.claim():
            self.store.finish(task, error="fixture failure")
        p = self.store.progress()
        self.assertEqual((p["state"], p["completed"], p["errors"]), ("COMPLETED_WITH_ERRORS", 0, 4))

    def test_changed_data_rejected(self):
        with self.assertRaises(ValueError):
            RunStore(self.path, self.space, dict(self.context, dataset_sha256="other"))

    def test_finite_axes_deduplicate(self):
        self.assertEqual(Space.create({"x": [1, 1, 2]}).total, 2)
        with self.assertRaises(IndexError):
            self.store.prioritize([0, 4])
        self.assertEqual(self.store.progress()["queued"], 0)

    def test_large_space_is_lazy_and_has_no_ten_million_cap(self):
        space = Space.create({str(i): range(10) for i in range(20)})
        self.assertEqual(space.total, 10**20)
        self.assertEqual(set(space.candidate(space.total-1).values()), {9})

    def test_blocks_not_total(self):
        p = self.store.progress(3)
        self.assertEqual((p["total"], p["block_size"], p["nominal_blocks"]), (4, 3, 2))
        self.store.claim(3)
        self.assertEqual(self.store.progress()["completed"], 0)

    def test_invalid_net_rejected(self):
        task = self.store.claim(1)[0]
        with self.assertRaises(ValueError):
            self.store.finish(task, self.result(task, float("nan")))


if __name__ == "__main__":
    unittest.main()

