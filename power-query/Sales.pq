let
    Source = Csv.Document(File.Contents(pSalesCsvPath), [Delimiter=",", Columns=12, Encoding=65001, QuoteStyle=QuoteStyle.Csv]),
    Headers = Table.PromoteHeaders(Source, [PromoteAllScalars=true]),
    Types = Table.TransformColumnTypes(Headers, {
        {"OrderID", type text}, {"Date", type date}, {"Region", type text},
        {"Category", type text}, {"Product", type text}, {"Units", Int64.Type},
        {"UnitPrice", Currency.Type}, {"UnitCost", Currency.Type}, {"Discount", type number}
    }, "en-US"),
    // Recalculate monetary values instead of trusting the demonstration CSV totals.
    RemoveImportedTotals = Table.RemoveColumns(Types, {"Revenue", "Cost", "Profit"}),
    Revenue = Table.AddColumn(RemoveImportedTotals, "Revenue", each Number.Round([Units] * [UnitPrice] * (1 - [Discount]), 2), Currency.Type),
    Cost = Table.AddColumn(Revenue, "Cost", each [Units] * [UnitCost], Currency.Type),
    Profit = Table.AddColumn(Cost, "Profit", each [Revenue] - [Cost], Currency.Type)
in
    Profit
