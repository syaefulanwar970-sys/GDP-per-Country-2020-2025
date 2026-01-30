import streamlit as st
import pandas as pd

def render_kpis(df: pd.DataFrame):
    st.subheader("📌 Executive Summary")

    latest_year = df["Year"].max()
    latest_df = df[df["Year"] == latest_year]

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Total Countries", df["Country"].nunique())
    col2.metric("Year Coverage", f"{df['Year'].min()}–{df['Year'].max()}")
    col3.metric("Highest GDP (Latest Year)", f"${latest_df['GDP'].max():,.0f}")
    col4.metric("Countries Reported", latest_df["Country"].nunique())
