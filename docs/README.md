# OLAP BI Assistant — README

## Overview

The OLAP BI Assistant is a Streamlit application that allows users to query a dataset using natural language. Users can type questions like "Show revenue per country for 2024" and the system automatically generates executable Python pandas code to perform OLAP operations.

The system uses Claude Haiku to convert natural language queries into OLAP operations (slice, dice, summarize, drill-down, compare) on a pandas DataFrame.

## Features

* Natural language queries for analytics
* OLAP operations: slice, dice, summarize, drill-down, compare
* Safe execution environment for generated Python code
* Interactive visualization with Streamlit

## Prerequisites

* Python 3.10 or higher
* Streamlit
* pandas
* `anthropic` Python package for Claude API access

## Setup Instructions

1. **Clone the repository**

```bash
git clone https://github.com/adasulejmani/olap-streamlit-app
cd olap-streamlit-app
```

2. **Create a virtual environment**

```bash
python -m venv venv
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows
```

3. **Install dependencies**

```bash
pip install -r requirements.txt
```

Dependencies include:

* streamlit
* pandas
* anthropic

4. **Set up environment variables**

Create a `.streamlit/secrets.toml` file with your Claude API key:

```toml
ANTHROPIC_API_KEY = "your_api_key_here"
```

5. **Prepare your dataset**

Place your CSV dataset in the `data/` folder. Make sure the CSV has the following columns:

```
order_date, year, quarter, month, region, country, category, subcategory, customer_segment, quantity, revenue, profit
```

6. **Run the Streamlit application**

```bash
streamlit run app.py
```

7. **Use the OLAP BI Assistant**

* Enter your query in the text input box.
* The app sends the query to Claude, which returns executable Python code.
* The code is safely executed and results are displayed in Streamlit.

## Folder Structure

```
/olap-streamlit-app
│
├─ app.py               # Main Streamlit app
├─ data_utils.py        # Data loading and OLAP helper functions
├─ prompts.py           # System prompt and OLAP templates
├─ data/                # Folder for datasets
├─ requirements.txt     # Python dependencies
├─ README.md            # This file
```

## Notes

* Ensure your queries reference existing dataset columns.
* Complex analytics may require multi-step queries.
* Output cleaning ensures executable Python code.
* Use `.streamlit/secrets.toml` to store API keys securely.

## Future Improvements

* Structured JSON output for results
* Query validation before execution
* Auto chart generation
* Enhanced security and execution guardrails
