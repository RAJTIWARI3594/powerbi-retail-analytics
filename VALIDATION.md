# Validation and native-report boundary

Validation run: 2026-10-20. Debian 12 Linux; Python 3.10.21. These are local checks, not a certification or an independent security audit. AI-assisted implementation and verification with Wabi.

## Passed

- `python -m unittest -v`: **10 tests**, all passed. These cover synthetic data
  grain/dates/completeness, revenue and profit arithmetic, region reconciliation,
  weighted margin, CSV schema, JSON theme parsing and generated HTML content.
- Chromium 155: opened the actual HTML reference, checked All and each of the
  four region filters against expected revenue/profit/margin and order counts,
  and expanded its 12-row monthly detail table.
- Desktop and mobile layouts reviewed; no horizontal mobile overflow and no
  JavaScript page errors in this check.
- [Desktop reference screenshot](docs/html-reference-demo.png) and
  [mobile reference screenshot](docs/html-reference-mobile.png) were captured
  from the working HTML page. [Browser receipt](docs/browser-checks.json).

All-data sales: **INR 3,630,970**; gross profit: **INR 1,496,400**;
orders: **720**. All records are synthetic.

## Not tested / not completed

Power BI Desktop is unavailable on this Linux machine. Power Query M and DAX
have been written for the documented model, but have **not** been executed in
Desktop. Theme import, relationships, slicer behaviour, native visual rendering,
refresh and PBIX save/reopen remain untested. No PBIX/PBIP file is included.

The HTML reference and Python tests do not prove that a native Power BI model
works. Follow [BUILD_REPORT.md](BUILD_REPORT.md), run the supplied DAX validation
query in Desktop and compare `data/expected_metrics.json` before describing a
native report as complete. Do not represent the HTML screenshots as Power BI
screenshots.
