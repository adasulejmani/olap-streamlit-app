# data_utils.py
import pandas as pd
import streamlit as st

# Load data with caching
@st.cache_data
def load_data(csv_path):
    df = pd.read_csv(csv_path)
    return df

# Slice (filter on single dimension)
def slice_data(df, filters: dict):
    filtered = df.copy()
    for col, val in filters.items():
        filtered = filtered[filtered[col] == val]
    return filtered

# Dice (filter on multiple dimensions)
def dice_data(df, filters: dict):
    filtered = df.copy()
    for col, val in filters.items():
        filtered = filtered[filtered[col] == val]
    return filtered

# Group & Summarize
def summarize_data(df, group_by, agg_column, agg_func='sum'):
    return df.groupby(group_by)[agg_column].agg(agg_func).reset_index()

# Drill-Down (assumes hierarchical columns)
def drill_down(df, hierarchy_cols):
    return df.groupby(hierarchy_cols).sum().reset_index()

# Compare two datasets or periods
def compare_data(df1, df2, metric_col):
    comparison = pd.DataFrame({
        'Metric': [metric_col],
        'Period1': [df1[metric_col].sum()],
        'Period2': [df2[metric_col].sum()],
        'Difference': [df2[metric_col].sum() - df1[metric_col].sum()]
    })
    return comparison