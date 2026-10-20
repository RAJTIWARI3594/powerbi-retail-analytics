import csv, json, unittest
from datetime import date
from pathlib import Path
from build_data import build, dataset, ROOT


class DataTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.metrics = build()
        cls.rows = dataset()

    def test_grain(self):
        self.assertEqual(len({r["OrderID"] for r in self.rows}), 720)

    def test_dates(self):
        for r in self.rows:
            self.assertEqual(date.fromisoformat(r["Date"]).year, 2025)
        self.assertEqual(len({r["Date"][5:7] for r in self.rows}), 12)

    def test_no_blank_fields(self):
        for r in self.rows:
            self.assertTrue(all(v is not None and v != "" for v in r.values()))

    def test_recalculated_revenue(self):
        for r in self.rows:
            self.assertAlmostEqual(
                r["Revenue"],
                round(r["Units"] * r["UnitPrice"] * (1 - r["Discount"]), 2),
            )

    def test_profit(self):
        for r in self.rows:
            self.assertAlmostEqual(
                r["Revenue"] - r["Units"] * r["UnitCost"], r["Profit"]
            )

    def test_region_reconciliation(self):
        self.assertAlmostEqual(
            sum(x["net_sales"] for x in self.metrics["regions"].values()),
            self.metrics["all"]["net_sales"],
        )

    def test_margin_is_ratio_of_totals(self):
        self.assertAlmostEqual(
            self.metrics["all"]["margin"],
            self.metrics["all"]["gross_profit"] / self.metrics["all"]["net_sales"],
        )

    def test_csv_schema(self):
        with (ROOT / "data/synthetic_sales.csv").open() as f:
            rows = list(csv.DictReader(f))
        self.assertEqual(len(rows), 720)
        self.assertEqual(len(rows[0]), 12)

    def test_theme_json(self):
        self.assertEqual(
            len(
                json.loads((ROOT / "theme/retail-pulse.json").read_text())["dataColors"]
            ),
            6,
        )

    def test_preview_generation(self):
        s = (ROOT / "preview/index.html").read_text()
        self.assertNotIn("__DATA__", s)
        self.assertIn("SYN-0720", s)


if __name__ == "__main__":
    unittest.main()
