# Prompt Engineering Design — OLAP BI Assistant

## 1. Purpose of the Prompt System

The OLAP BI Assistant allows users to query a dataset using natural language instead of writing Python or SQL.

**Example:**

"Show revenue per country for 2024"

The Large Language Model (LLM) translates this request into executable pandas code, which is then executed inside the Streamlit application.

The prompt system ensures that the model:

✅ Understands the dataset structure
✅ Uses valid OLAP operations
✅ Produces executable Python code only
✅ Returns results consistently

## 2. Architecture Overview

The prompt workflow follows this pipeline:

```
User Question
      ↓
System Prompt (rules + dataset schema)
      ↓
LLM (Claude Haiku)
      ↓
Generated Python Code
      ↓
Safe Execution (exec)
      ↓
Displayed Result in Streamlit
```

## 3. Prompt Components

| Component     | File                | Purpose                    |
| ------------- | ------------------- | -------------------------- |
| System Prompt | app.py / prompts.py | Defines rules and behavior |
| Templates     | prompts.py          | Guides OLAP interpretation |

## 4. System Prompt Logic

**Current System Prompt:**

```python
SYSTEM_PROMPT = """
You are a Business Intelligence Assistant.
Given a pandas DataFrame named 'df', generate Python code that performs the requested OLAP operation.
Respond ONLY with valid Python code and assign the final output to a variable named 'result'.
Available operations: slice, dice, summarize, drill-down, compare.
Dataset columns: order_date, year, quarter, month, region, country, category, subcategory, customer_segment, quantity, revenue, profit.
"""
```

### Why This Works

The prompt enforces three critical constraints:

1️⃣ **Role Definition**
You are a Business Intelligence Assistant
This narrows the model’s behavior to analytics tasks instead of general conversation.

Without this, the model might:

* explain concepts
* add commentary
* produce non-executable text

2️⃣ **Dataset Awareness**
Dataset columns: ...
The model cannot see your CSV directly. You must explicitly provide:

* column names
* schema context

This prevents hallucinated columns like:
❌ sales_amount
❌ customer_age

3️⃣ **Output Constraint (MOST IMPORTANT)**
Respond ONLY with valid Python code

This prevents:

* explanations
* markdown
* bullet points
* notes

Your app executes the response using:

```python
exec(code, {}, local_vars)
```

Therefore any extra text breaks execution.

## 5. Template Logic (prompts.py)

```python
TEMPLATES = {
    "slice": "Filter {column} for value {value}",
    "dice": "Filter multiple columns: {filters}",
    "summarize": "Group by {group_by} and aggregate {agg_column} with {agg_func}",
    "drill_down": "Group by hierarchy columns {columns} and summarize",
    "compare": "Compare {metric_col} between periods {period1} and {period2}"
}
```

**Purpose:**

Templates help standardize how OLAP concepts are interpreted. They act as semantic hints for the LLM.

### Mapping Natural Language → OLAP

| User Request           | Operation  |
| ---------------------- | ---------- |
| Show 2024 data         | Slice      |
| Electronics in Europe  | Dice       |
| Revenue by country     | Summarize  |
| Year → Quarter → Month | Drill-down |
| Compare 2023 vs 2024   | Compare    |

## 6. Code Generation Process

When a user submits a query:

```python
query = st.text_input(...)
```

The app sends:

```
SYSTEM_PROMPT + user_query
```

to Claude:

```python
response = client.messages.create(...)
```

**Example transformation:**

**User Input:**

```
Show revenue per country for 2024
```

**LLM Output:**

```python
filtered = df[df["year"] == 2024]
result = filtered.groupby("country")["revenue"].sum().reset_index()
```

## 7. Output Cleaning Layer

Claude sometimes adds formatting:

```python
result = ...
```

Your app removes this using:

````python
code = "\n".join(
    line for line in code.splitlines()
    if not line.strip().startswith("Note:")
    and not line.strip().startswith("-")
    and not line.strip().startswith("```")
)
````

This guarantees executable code.

## 8. Safe Execution Design

Generated code runs in a restricted environment:

```python
local_vars = {
    "df": df,
    "pd": pd,
    "slice_data": slice_data,
    ...
}
```

**Benefits:**

✅ Prevents undefined function errors
✅ Limits execution scope
✅ Enables reusable OLAP helpers

## 9. Why Claude Haiku Was Selected

**Model used:** claude-haiku-4-5

**Reasons:**

* Low cost
* Fast responses
* Reliable structured code output
* Suitable for deterministic analytics tasks

This model balances performance and cost for interactive BI applications.

## 10. Prompt Engineering Challenges & Solutions

| Problem                 | Solution                   |
| ----------------------- | -------------------------- |
| Model adds explanations | Enforce "ONLY Python code" |
| Invalid syntax          | Output cleaning filter     |
| Wrong columns           | Provide schema             |
| Missing result variable | Explicit instruction       |
| Function not found      | Inject helpers into exec() |

## 11. Limitations

* Model does not truly understand data values.
* Queries must reference existing columns.
* Complex multi-step analytics may require prompt refinement.

## 12. Future Improvements

* Structured JSON output instead of raw code
* Query classification before LLM call
* Validation layer before execution
* Auto chart generation
* Guardrails for unsafe code
