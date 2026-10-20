# Build the native report

This is a manual Power BI Desktop build guide, not a claim of a completed native
report. The code files are intended for the following setup and remain untested
in Desktop. First reproduce the supplied example before replacing its data.

## 1. Import and transform

1. Clone/download this repository. Find the absolute local path to
   `data/synthetic_sales.csv` (not a GitHub webpage URL).
2. Open Power BI Desktop > Get data > Blank query > Transform data.
3. Rename that query `pSalesCsvPath`. In Advanced Editor, paste the contents of
   `power-query/pSalesCsvPath.pq`. Replace the example path with your actual path.
   In M strings, backslash is literal: use `C:\Portfolio\...` with one backslash
   between components, not Python-style double escaping.
4. Add a second blank query named `Sales`. Paste `power-query/Sales.pq` in Advanced
   Editor. Check 720 rows and 12 columns; Date must be Date, Units whole number,
   monetary columns fixed decimal, Discount decimal (fraction, not whole percent).
   Monetary columns are recalculated, not trusted from the CSV.
5. Close & Apply. If the CSV path changes, edit the parameter and refresh.

## 2. Model and measures

1. Modeling > New table: paste the complete expression in `dax/Calendar.dax`.
2. Mark Calendar as a date table using Calendar[Date].
3. Create a single-direction one-to-many active relationship:
   `Calendar[Date] (1) → Sales[Date] (*)`. Do not add bidirectional relationships.
4. Sort Calendar[Month] by Calendar[MonthNo]. Use Calendar[YearMonth] on the chart
   to avoid accidentally combining different years if the dataset expands.
5. Add each of the nine expressions in `dax/measures.dax` separately with New
   measure. The first line is its name. Format Net Sales, Total Cost, Gross Profit,
   Average Order Value and Previous Month Sales as INR currency with two decimals;
   Gross Margin % and MoM Sales % as percent with one decimal; counts as integers.
6. Turn off Auto date/time for this file to avoid competing implicit date tables.

## 3. Build one report page

- Canvas: 16:9. Title: **Retail Pulse / 2025**.
- Subtitle: **Synthetic demonstration data · INR · 720 orders**.
- Top slicers: Sales[Region], Sales[Category], Calendar[YearMonth]. Allow clearing
  selections; all charts/cards must respond to the same slicer context.
- Top row: cards for Net Sales, Gross Profit, Gross Margin % and Orders.
- Middle left: clustered column chart, Calendar[YearMonth] on X, Net Sales and
  Gross Profit on Y. Sort YearMonth ascending.
- Middle right: horizontal bar chart, Sales[Category] on Y and Net Sales on X.
- Bottom: matrix with Sales[Region] rows, Net Sales, Gross Profit, Gross Margin %,
  Orders and Average Order Value values. Add conditional colour to margin.
- Add MoM Sales % to the monthly chart tooltip (do not aggregate the percentage).
- View > Themes > Browse for themes: select `theme/retail-pulse.json`.
- Add footer: **Gross profit excludes taxes, returns, shipping and overhead**.

## 4. Check before saving

1. Clear all slicers. In DAX query view run `dax/validation-query.dax` after creating
   the measures. Compare results with `data/expected_metrics.json` → `all`.
2. Filter North and compare every card with `regions.North` in that JSON.
3. Confirm monthly/category sums reconcile to the all-data sales amount.
4. Confirm January 2025 MoM is blank because December 2024 is outside the dataset.
5. Clear all filters, save as `RetailPulse.pbix`, reopen and refresh. Only after
   this succeeds call it a completed Power BI report. Capture real screenshots
   and record your Desktop version and validation results.

The HTML reference preview demonstrates layout/filtering with independently
implemented JavaScript. It is neither a substitute for these Desktop checks nor
a native Power BI output.
