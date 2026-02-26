# app.py
import streamlit as st
import pandas as pd
import anthropic

from data_utils import load_data, slice_data, dice_data, summarize_data, drill_down, compare_data

# --- Create Anthropic client ---
client = anthropic.Anthropic(api_key=st.secrets["ANTHROPIC_API_KEY"])

# Load dataset
df = load_data("data/global_retail_sales.csv")

st.title("OLAP BI Assistant")

# Dataset Overview
if st.checkbox("Show Dataset Overview"):
    st.write(df.head())
    st.write(df.describe())

# System prompt
SYSTEM_PROMPT = """
You are a Business Intelligence Assistant.
Given a pandas DataFrame named 'df', generate Python code that performs the requested OLAP operation.
Respond ONLY with valid Python code and assign the final output to a variable named 'result'.
Available operations: slice, dice, summarize, drill-down, compare.
Dataset columns: order_date, year, quarter, month, region, country, category, subcategory, customer_segment, quantity, revenue, profit.
"""

# User Query
query = st.text_input("Ask a question about the dataset:", "")

# Function to get OLAP Python code from Claude
def get_olap_code(user_query):
    response = client.messages.create(
        model="claude-haiku-4-5",
        max_tokens=500,
        temperature=0,
        messages=[
            {"role": "user", "content": f"{SYSTEM_PROMPT}\n\nUser request: {user_query}"}
        ]
    )
    code = response.content[0].text

    # Keep only Python code: remove notes, bullets, and ``` markers
    code = "\n".join(
        line for line in code.splitlines()
        if not line.strip().startswith("Note:") and
           not line.strip().startswith("-") and
           not line.strip().startswith("```")
    ).strip()

    return code

# Run query
if st.button("Run Query") and query:
    try:
        code = get_olap_code(query)
        st.code(code, language="python")

        # Safe execution
        local_vars = {"df": df, "pd": pd, 
                      "slice_data": slice_data, "dice_data": dice_data, 
                      "summarize_data": summarize_data, "drill_down": drill_down, 
                      "compare_data": compare_data}

        exec(code, {}, local_vars)
        result = local_vars.get("result", None)

        if result is not None:
            st.write(result)
        else:
            st.warning("No result returned. Make sure the code defines 'result'.")
    except Exception as e:
        st.error(f"Error: {e}")