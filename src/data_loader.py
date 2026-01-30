import pandas as pd
import streamlit as st
import os

DATA_PATH = os.path.join("data", "gdp_country_2020_2025.csv")

@st.cache_data(ttl=3600, show_spinner=False)
def load_data() -> pd.DataFrame:
    df_raw = pd.read_csv(DATA_PATH)

    year_columns = [col for col in df_raw.columns if col != "Country"]

    df = df_raw.melt(
        id_vars=["Country"],
        value_vars=year_columns,
        var_name="Year",
        value_name="GDP"
    )

    df["Year"] = df["Year"].astype(int)
    df["GDP"] = pd.to_numeric(df["GDP"], errors="coerce")

    return df.dropna(subset=["GDP"])
