from __future__ import annotations

import datetime as dt
import importlib.util
import sys
import unittest
from pathlib import Path


SCRIPT = Path(__file__).parents[1] / "scripts" / "proven_cash_yield.py"
SPEC = importlib.util.spec_from_file_location("proven_cash_yield", SCRIPT)
assert SPEC and SPEC.loader
MODULE = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = MODULE
SPEC.loader.exec_module(MODULE)


def annual_fact(start: str, end: str, value: float, filed: str = "2025-01-01") -> dict:
    return {
        "start": start,
        "end": end,
        "val": value,
        "filed": filed,
        "form": "10-K",
        "fp": "FY",
    }


def instant_fact(end: str, value: float) -> dict:
    return {
        "end": end,
        "val": value,
        "filed": "2025-01-01",
        "form": "10-K",
    }


class ProvenCashYieldTests(unittest.TestCase):
    AS_OF = dt.date(2025, 6, 1)

    def companyfacts(self) -> dict:
        periods = (
            ("2022-01-01", "2022-12-31"),
            ("2023-01-01", "2023-12-31"),
            ("2024-01-01", "2024-12-31"),
        )
        facts = {}
        for tag, values in {
            "NetCashProvidedByUsedInOperatingActivities": (100, 120, 140),
            "PaymentsToAcquirePropertyPlantAndEquipment": (20, 25, 30),
            "ShareBasedCompensation": (5, 6, 7),
        }.items():
            facts[tag] = {
                "units": {
                    "USD": [
                        annual_fact(start, end, value)
                        for (start, end), value in zip(periods, values)
                    ]
                }
            }
        return {"facts": {"us-gaap": facts}}

    def test_owner_cash_uses_three_periods(self) -> None:
        history, error = MODULE.owner_cash_history(self.companyfacts(), self.AS_OF)
        self.assertIsNone(error)
        self.assertEqual([row["owner_cash"] for row in history], [103.0, 89.0, 75.0])

    def test_latest_restatement_wins(self) -> None:
        facts = self.companyfacts()
        rows = facts["facts"]["us-gaap"]["ShareBasedCompensation"]["units"]["USD"]
        rows.append(annual_fact("2024-01-01", "2024-12-31", 9, "2025-02-01"))
        history, _ = MODULE.owner_cash_history(facts, self.AS_OF)
        self.assertEqual(history[0]["stock_compensation"], 9.0)

    def test_missing_stock_comp_is_not_zero(self) -> None:
        facts = self.companyfacts()
        del facts["facts"]["us-gaap"]["ShareBasedCompensation"]
        history, error = MODULE.owner_cash_history(facts, self.AS_OF)
        self.assertEqual(history, [])
        self.assertIn("fewer than three", error)

    def test_negative_capex_is_rejected(self) -> None:
        facts = self.companyfacts()
        facts["facts"]["us-gaap"]["PaymentsToAcquirePropertyPlantAndEquipment"]["units"]["USD"][0]["val"] = -20
        history, error = MODULE.owner_cash_history(facts, self.AS_OF)
        self.assertEqual(history, [])
        self.assertIn("ambiguous sign", error)

    def test_stale_financials_are_rejected(self) -> None:
        history, error = MODULE.owner_cash_history(
            self.companyfacts(),
            dt.date(2026, 7, 29),
        )
        self.assertEqual(history, [])
        self.assertIn("stale annual financials", error)

    def test_nonconsecutive_financials_are_rejected(self) -> None:
        facts = self.companyfacts()
        for concept in facts["facts"]["us-gaap"].values():
            concept["units"]["USD"][0]["start"] = "2020-01-01"
            concept["units"]["USD"][0]["end"] = "2020-12-31"
        history, error = MODULE.owner_cash_history(facts, self.AS_OF)
        self.assertEqual(history, [])
        self.assertIn("nonconsecutive annual periods", error)

    def test_owner_cash_quality_requires_current_and_repeatable_cash(self) -> None:
        history = [
            {"owner_cash": -1},
            {"owner_cash": 10},
            {"owner_cash": 20},
        ]
        quality, error = MODULE.owner_cash_quality(history)
        self.assertEqual(error, "nonpositive latest owner cash")
        self.assertEqual(quality["owner_cash_positive_years"], 2)

        history = [
            {"owner_cash": 1},
            {"owner_cash": -10},
            {"owner_cash": -20},
        ]
        _, error = MODULE.owner_cash_quality(history)
        self.assertEqual(error, "fewer than two positive owner-cash years")

    def test_owner_cash_concentration_is_flagged(self) -> None:
        quality, error = MODULE.owner_cash_quality(
            [{"owner_cash": 100}, {"owner_cash": 10}, {"owner_cash": 10}]
        )
        self.assertIsNone(error)
        self.assertTrue(quality["owner_cash_concentration_warning"])

    def test_ff12_boundaries_and_financials(self) -> None:
        self.assertEqual(MODULE.ff12_sector("3571"), "BusEq")
        self.assertEqual(MODULE.ff12_sector(6020), "Money")
        self.assertEqual(MODULE.ff12_sector(9999), "Other")

    def test_positive_median_excludes_losses(self) -> None:
        self.assertEqual(MODULE.median_positive([-0.2, 0.02, 0.04]), 0.03)
        self.assertIsNone(MODULE.median_positive([-0.2, 0]))

    def test_daily_bar_price(self) -> None:
        price, timestamp = MODULE.price_from_daily_bar({"c": 11, "t": 4})
        self.assertEqual(price, 11)
        self.assertEqual(timestamp, "4")

    def test_market_cap_must_reconcile(self) -> None:
        values, error = MODULE.reconciled_market_cap(
            10,
            {
                "weighted_shares_outstanding": 100,
                "market_cap": 950,
            },
        )
        self.assertIsNone(error)
        self.assertEqual(values["market_cap"], 1000)

        values, error = MODULE.reconciled_market_cap(
            10,
            {
                "weighted_shares_outstanding": 100,
                "market_cap": 800,
            },
        )
        self.assertEqual(values, {})
        self.assertIn("differs", error)

    def test_total_debt_prevents_component_double_counting(self) -> None:
        facts = {
            "facts": {
                "us-gaap": {
                    "LongTermDebt": {"units": {"USD": [instant_fact("2024-12-31", 100)]}},
                    "LongTermDebtCurrent": {
                        "units": {"USD": [instant_fact("2024-12-31", 20)]}
                    },
                    "LongTermDebtNoncurrent": {
                        "units": {"USD": [instant_fact("2024-12-31", 80)]}
                    },
                }
            }
        }
        self.assertEqual(MODULE.latest_debt(facts, self.AS_OF), 100)

    def test_debt_components_are_summed_without_total(self) -> None:
        facts = {
            "facts": {
                "us-gaap": {
                    "LongTermDebtCurrent": {
                        "units": {"USD": [instant_fact("2024-12-31", 20)]}
                    },
                    "LongTermDebtNoncurrent": {
                        "units": {"USD": [instant_fact("2024-12-31", 80)]}
                    },
                }
            }
        }
        self.assertEqual(MODULE.latest_debt(facts, self.AS_OF), 100)


if __name__ == "__main__":
    unittest.main()
