"""Behavior checks for the notebook's reusable functions and real default run."""

import copy
import unittest
from unittest.mock import patch

from odds_comparability import (
    app,
    compare_records,
    record_table,
    synthetic_records,
    workload,
)


class ComparabilityTests(unittest.TestCase):
    def test_matching_contract_passes_declared_checks(self):
        left, right = synthetic_records("matching")
        self.assertEqual(compare_records(left, right, 5, 2), [])

    def test_each_contract_mismatch_has_a_specific_reason(self):
        for scenario, message in (
            ("event", "Event identity: the records differ"),
            ("market", "Market: the records differ"),
            ("outcome", "Named outcome: the records differ"),
            ("point", "Point/line differs"),
            ("period", "Period: the records differ"),
            ("settlement", "Settlement rules: the records differ"),
            ("unknown_rules", "Settlement rules are not fully supplied"),
        ):
            with self.subTest(scenario=scenario):
                self.assertTrue(
                    any(
                        message in r
                        for r in compare_records(*synthetic_records(scenario), 5, 2)
                    )
                )

    def test_missing_outcome_never_becomes_opponent_price(self):
        left, right = synthetic_records("missing")
        self.assertIn("missing", compare_records(left, right, 5, 2)[0])
        self.assertEqual(right, [])
        self.assertIn("Record B: missing", record_table(left, right))

    def test_duplicate_neither_selected_nor_mutated(self):
        left, right = synthetic_records("duplicate")
        original = copy.deepcopy(right)
        self.assertIn(
            "neither price is selected", compare_records(left, right, 5, 2)[0]
        )
        self.assertEqual(right, original)
        table = record_table(left, right)
        self.assertIn("-105", table)
        self.assertIn("-115", table)

    def test_fresh_retrieval_does_not_repair_old_source(self):
        reasons = compare_records(*synthetic_records("matching", 12), 5, 2)
        self.assertTrue(any("12 minutes old" in r for r in reasons))
        self.assertTrue(any("11 minutes apart" in r for r in reasons))

    def test_missing_time_is_unknown(self):
        reasons = compare_records(*synthetic_records("unknown_time"), 5, 2)
        self.assertTrue(any("Retrieval time cannot replace it" in r for r in reasons))

    def test_time_boundaries_are_inclusive(self):
        self.assertEqual(compare_records(*synthetic_records("matching", 5), 5, 4), [])
        self.assertTrue(compare_records(*synthetic_records("matching", 5), 4, 4))

    def test_future_source_and_inconsistent_retrieval_are_rejected(self):
        left, right = synthetic_records("future_time")
        reasons = compare_records(left, right, 5, 2)
        self.assertTrue(any("future source" in r for r in reasons))
        self.assertTrue(any("inconsistent" in r for r in reasons))

    def test_unknown_line_and_invalid_price_are_rejected(self):
        left, right = synthetic_records("matching")
        right[0].update(point=None, price=float("nan"))
        reasons = compare_records(left, right, 5, 2)
        self.assertTrue(any("required point/line" in r for r in reasons))
        self.assertTrue(any("valid American price" in r for r in reasons))

    def test_table_escapes_adapted_labels(self):
        left, right = synthetic_records("matching")
        right[0]["event"] = "<script>alert(1)</script>"
        self.assertNotIn("<script>", record_table(left, right))


class WorkloadTests(unittest.TestCase):
    def test_continuous_and_scheduled_examples(self):
        scheduled = workload(15, 8, 30, 3)
        continuous = workload(1, 24, 30, 3)
        self.assertEqual(scheduled["calls_monthly"], 960)
        self.assertEqual(scheduled["credits_monthly"], 2880)
        self.assertEqual(scheduled["unobserved_hours_daily"], 16)
        self.assertEqual(continuous["calls_monthly"], 43200)
        self.assertEqual(continuous["credits_monthly"], 129600)
        self.assertEqual(continuous["calls_monthly"] / scheduled["calls_monthly"], 45)

    def test_weight_changes_credits_not_request_count(self):
        one, three, zero = [workload(15, 8, 30, n) for n in (1, 3, 0)]
        self.assertEqual(one["calls_monthly"], three["calls_monthly"])
        self.assertEqual(one["credits_monthly"], 960)
        self.assertEqual(zero["credits_monthly"], 0)

    def test_window_end_is_excluded_and_partial_interval_counted(self):
        self.assertEqual(workload(60, 1, 1, 1)["calls_daily"], 1)
        self.assertEqual(workload(7, 1, 1, 1)["calls_daily"], 9)

    def test_invalid_parameters_fail_instead_of_silently_normalizing(self):
        for args in (
            (0, 8, 30, 3),
            (1, 0, 30, 3),
            (1, 25, 30, 3),
            (1, 8, 32, 3),
            (1, 8, 30, -1),
            (True, 8, 30, 3),
            (1.5, 8, 30, 3),
            (1, 8, float("nan"), 3),
        ):
            with self.subTest(args=args), self.assertRaises(ValueError):
                workload(*args)

    def test_notebook_runs_without_network_and_returns_real_default_results(self):
        self.assertFalse(app._unparsable)
        with patch(
            "socket.socket.connect",
            side_effect=AssertionError("Notebook tried network"),
        ):
            _, definitions = app.run()
        self.assertEqual(definitions["estimate"]["calls_monthly"], 960)
        self.assertEqual(definitions["ratio"], 45)
        self.assertTrue(
            any("Point/line differs" in reason for reason in definitions["reasons"])
        )


if __name__ == "__main__":
    unittest.main()
