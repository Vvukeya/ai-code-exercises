# Function Decomposition Challenge

**Language:** Python
**Function:** `generate_sales_report()`
**File:** `sales_report.py`

## Step 1 — Responsibilities I Found Before Using AI

Before using AI, I read through `generate_sales_report()` and noticed that it is doing many different jobs.

The responsibilities I identified are:

1. Validate the sales data input.
2. Validate the report type.
3. Validate the output format.
4. Validate and process the date range.
5. Filter sales by date.
6. Apply additional custom filters.
7. Handle cases where no data remains after filtering.
8. Calculate summary metrics such as total, average, minimum and maximum sales.
9. Group sales by product, category, customer or region.
10. Calculate totals, counts and averages for groups.
11. Build the main report structure.
12. Add detailed transaction calculations such as pre-tax amount, profit and margin.
13. Calculate monthly sales and forecast future sales.
14. Build chart data.
15. Send the final report to the correct output format.

The biggest problem is that one function is responsible for data validation, business calculations, forecasting, presentation data and output generation.

This makes the function long and harder to understand, test, reuse and maintain.

## Step 2 — AI Analysis and Comparison

AI confirmed that `generate_sales_report()` is doing too many jobs in one function.

My own analysis identified validation, filtering, calculations, grouping, forecasting, chart creation and output generation. The AI suggested separating these responsibilities into smaller helper functions.

## Step 3 — Final Decomposition Plan

I would extract these helper functions:

- `validate_report_inputs()` — validates sales data, report type and output format.
- `filter_by_date_range()` — filters transactions using start and end dates.
- `apply_sales_filters()` — applies category, product, customer or region filters.
- `calculate_sales_metrics()` — calculates total, average, minimum and maximum sales.
- `group_sales_data()` — groups sales and calculates group totals and averages.
- `build_base_report()` — creates the common report structure.
- `build_detailed_transactions()` — calculates pre-tax values, profit and margin.
- `calculate_monthly_sales()` — groups sales totals by month.
- `calculate_growth_rates()` — calculates month-to-month growth.
- `project_future_sales()` — estimates future monthly sales.
- `build_forecast_data()` — coordinates forecast calculations.
- `build_chart_data()` — creates chart information.
- `generate_report_output()` — selects JSON, HTML, Excel or PDF output.

## Step 4 — Example Helper Extraction

One useful helper would be:

```python
def calculate_sales_metrics(sales_data):
    total_sales = sum(sale['amount'] for sale in sales_data)

    return {
        'total_sales': total_sales,
        'transaction_count': len(sales_data),
        'average_sale': total_sales / len(sales_data),
        'max_sale': max(sales_data, key=lambda sale: sale['amount']),
        'min_sale': min(sales_data, key=lambda sale: sale['amount'])
    }
```

The main function could simply call:

```python
metrics = calculate_sales_metrics(sales_data)
```

This helper would be easier to understand, reuse and test independently.

## Step 5 — Refactored Main Function Sketch

The main function could become a short coordinator:

```python
def generate_sales_report(...):
    validate_report_inputs(...)
    sales_data = filter_by_date_range(...)
    sales_data = apply_sales_filters(...)

    metrics = calculate_sales_metrics(sales_data)
    grouped_data = group_sales_data(...)

    report_data = build_base_report(...)

    if report_type == 'detailed':
        report_data['transactions'] = build_detailed_transactions(...)

    if report_type == 'forecast':
        report_data['forecast'] = build_forecast_data(...)

    if include_charts:
        report_data['charts'] = build_chart_data(...)

    return generate_report_output(...)
```

The main function would coordinate the report instead of performing every calculation itself.

## Reflection

The original function contains many responsibilities, which makes it difficult to read and maintain.

The most reusable helper would be `calculate_sales_metrics()` because many report types could reuse the same calculations.

The forecasting logic would probably be the hardest part to separate because monthly sales, growth rates and future projections depend on one another.

Splitting the function would improve readability, testing, reuse and maintenance.

Before applying this refactoring to production code, I would make sure automated tests exist so that behaviour can be checked before and after the changes.
