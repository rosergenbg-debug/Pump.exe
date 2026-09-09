import unittest
from presentation import archive_rows, current_leader, PALETTE


class PresentationTests(unittest.TestCase):
    def test_version_filter_and_numeric_sort(self):
        rows = [dict(id="a", version="16", net=9, trades=100),
                dict(id="b", version="17", net=.3, trades=2),
                dict(id="c", version="17", net=.4, trades=10)]
        self.assertEqual([r["id"] for r in archive_rows(rows, "17", column="trades")], ["c", "b"])
        self.assertEqual([r["id"] for r in archive_rows(rows, "17", column="trades", descending=False)], ["b", "c"])

    def test_filter_never_deletes_below_threshold(self):
        rows = [dict(net=.19), dict(net=.2), dict(net=-.3)]
        self.assertEqual(len(archive_rows(rows)), 1)
        self.assertEqual(len(archive_rows(rows, minimum_net=None)), 3)
        self.assertEqual(len(rows), 3)

    def test_current_leader_not_archive_or_pending(self):
        context = dict(version="17", run_id="new", data="x")
        rows = [dict(context=dict(context, version="11"), status="DONE", net=10),
                dict(context=dict(context, run_id="old"), status="DONE", net=9),
                dict(context=context, status="RUNNING", net=8),
                dict(context=context, status="DONE", net=.1)]
        self.assertEqual(current_leader(rows, context)["net"], .1)
        self.assertIsNone(current_leader(rows[:-1], context))

    def test_no_blue_accent(self):
        self.assertEqual(PALETTE["accent"], "#F0B90B")

    def test_unknown_sort_rejected(self):
        with self.assertRaises(ValueError):
            archive_rows([], column="sql")


if __name__ == "__main__":
    unittest.main()

