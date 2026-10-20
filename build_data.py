"""Generate a reproducible synthetic sales workbook. No Excel installation required."""

import calendar, csv, json, random
from collections import defaultdict
from datetime import date, datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent
CATALOG = [
    ("Technology", "Keyboard", 1800, 1000),
    ("Technology", "Headphones", 2400, 1400),
    ("Office", "Desk lamp", 1200, 680),
    ("Office", "Notebook pack", 450, 200),
    ("Home", "Storage box", 800, 430),
    ("Home", "Water bottle", 650, 320),
    ("Accessories", "Backpack", 2100, 1200),
    ("Accessories", "Laptop sleeve", 900, 400),
]
REGIONS = ["North", "South", "East", "West"]
FIELDS = [
    "OrderID",
    "Date",
    "Region",
    "Category",
    "Product",
    "Units",
    "UnitPrice",
    "UnitCost",
    "Discount",
    "Revenue",
    "Cost",
    "Profit",
]


def dataset():
    rng = random.Random(3594)
    rows = []
    for month in range(1, 13):
        for i in range(60):
            category, product, price, cost = rng.choice(CATALOG)
            units = rng.randint(1, 8)
            discount = rng.choice([0, 0.05, 0.1, 0.15])
            revenue = round(units * price * (1 - discount), 2)
            expense = units * cost
            rows.append(
                dict(
                    zip(
                        FIELDS,
                        [
                            f"SYN-{len(rows) + 1:04}",
                            date(
                                2025,
                                month,
                                rng.randint(1, calendar.monthrange(2025, month)[1]),
                            ).isoformat(),
                            rng.choice(REGIONS),
                            category,
                            product,
                            units,
                            price,
                            cost,
                            discount,
                            revenue,
                            expense,
                            round(revenue - expense, 2),
                        ],
                    )
                )
            )
    return rows


def build():
    data = ROOT / "data"
    data.mkdir(exist_ok=True)
    rows = dataset()
    with (data / "synthetic_sales.csv").open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=FIELDS)
        w.writeheader()
        w.writerows(rows)

    def summarize(group):
        sales = round(sum(r["Revenue"] for r in group), 2)
        cost = round(sum(r["Cost"] for r in group), 2)
        profit = round(sales - cost, 2)
        return {
            "net_sales": sales,
            "cost": cost,
            "gross_profit": profit,
            "margin": profit / sales if sales else 0,
            "orders": len(group),
            "units": sum(r["Units"] for r in group),
            "aov": sales / len(group) if group else 0,
        }

    metrics = {
        "all": summarize(rows),
        "regions": {
            region: summarize([r for r in rows if r["Region"] == region])
            for region in REGIONS
        },
    }
    (data / "expected_metrics.json").write_text(json.dumps(metrics, indent=2) + "\n")
    template = (ROOT / "preview/template.html").read_text()
    (ROOT / "preview/index.html").write_text(
        template.replace("__DATA__", json.dumps(rows))
    )
    return metrics


if __name__ == "__main__":
    print(json.dumps(build(), indent=2))
