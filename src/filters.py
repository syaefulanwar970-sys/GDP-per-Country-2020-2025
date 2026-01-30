import streamlit as st
import pandas as pd

def sidebar_filters(df: pd.DataFrame):
    st.sidebar.header("🔎 Filter")

    countries = st.sidebar.multiselect(
        "Select Country",
        options=sorted(df["Country"].unique()),
        default=sorted(df["Country"].unique())[:5]
    )

    year_range = st.sidebar.slider(
        "Year Range",
        min_value=int(df["Year"].min()),
        max_value=int(df["Year"].max()),
        value=(2020, 2025)
    )

    filtered_df = df.query(
        "Country in @countries and Year >= @year_range[0] and Year <= @year_range[1]"
    )

    selected_year = st.sidebar.selectbox(
        "Comparison Year",
        sorted(df["Year"].unique()),
        index=len(sorted(df["Year"].unique())) - 1
    )

    return filtered_df, selected_year
