# app.py

import streamlit as st
import pandas as pd
import anthropic

# ✅ Import prompts from prompts.py
from prompts import SYSTEM_PROMPT, TEMPLATES

# Import OLAP utilities
from data_utils import (
    load_data,
    slice_data,
    dice_data,
    summarize_data,
    drill_down,
    compare_data,
)

# --- Create Anthropic client ---
client = anthropic.Anthropic(
    api_key=st.secrets["ANTHROPIC_API_KEY"]
)

# --- Load dataset ---
df = load_data("data/global_retail_sales.csv")

# --- App UI ---
st.title("OLAP BI Assistant")

# Dataset Overview
if st.checkbox("Show Dataset Overview"):
    st.write(df.head())
    st.write(df.describe())

# --- User Query Input ---
query = st.text_input("Ask a question about the dataset:", "")


# --- Function: Generate OLAP Python code using Claude ---
def get_olap_code(user_query):
    response = client.messages.create(
        model="claude-haiku-4-5",
        max_tokens=500,
        temperature=0,
        messages=[
            {
                "role": "user",
                "content": f"""
{SYSTEM_PROMPT}

OLAP Templates:
{TEMPLATES}

User request: {user_query}
"""
            }
        ],
    )

    code = response.content[0].text

    # Clean output → keep only Python code
    code = "\n".join(
        line
        for line in code.splitlines()
        if not line.strip().startswith("Note:")
        and not line.strip().startswith("-")
        and not line.strip().startswith("```")
    ).strip()

    return code


# --- Execute Query ---
if st.button("Run Query") and query:
    try:
        # Get generated pandas code
        code = get_olap_code(query)

        st.subheader("Generated Python Code")
        st.code(code, language="python")

        # Safe execution environment
        local_vars = {
            "df": df,
            "pd": pd,
            "slice_data": slice_data,
            "dice_data": dice_data,
            "summarize_data": summarize_data,
            "drill_down": drill_down,
            "compare_data": compare_data,
        }

        # Execute generated code
        exec(code, {}, local_vars)

        result = local_vars.get("result", None)

        if result is not None:
            st.subheader("Result")
            st.write(result)
        else:
            st.warning(
                "No result returned. Make sure the code defines 'result'."
            )

    except Exception as e:
        st.error(f"Error: {e}")
