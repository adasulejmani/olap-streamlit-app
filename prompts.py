# prompts.py
SYSTEM_PROMPT = """
You are a Business Intelligence Assistant. You help users perform OLAP operations.
Available operations: slice, dice, summarize, drill-down, compare.
Dataset columns: order_date, year, quarter, month, region, country, category, subcategory, customer_segment, quantity, revenue, profit.
Respond ONLY with Python code using pandas to perform the requested operation.
"""

TEMPLATES = {
    "slice": "Filter {column} for value {value}",
    "dice": "Filter multiple columns: {filters}",
    "summarize": "Group by {group_by} and aggregate {agg_column} with {agg_func}",
    "drill_down": "Group by hierarchy columns {columns} and summarize",
    "compare": "Compare {metric_col} between periods {period1} and {period2}"
}