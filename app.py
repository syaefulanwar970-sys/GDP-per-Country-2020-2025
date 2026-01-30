import streamlit as st
import pandas as pd
import plotly.express as px

# =========================================================
# PAGE CONFIG
# =========================================================
st.set_page_config(
    page_title="Global GDP Dashboard",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =========================================================
# HEADER
# =========================================================
st.title("🌍 Global GDP Dashboard (2020–2025)")
st.caption("Executive Economic Intelligence | Country-Level GDP Analysis")

st.markdown("---")

# =========================================================
# LOAD & TRANSFORM DATA
# =========================================================
@st.cache_data
def load_and_prepare_data():
    # Load wide-format data
    df_raw = pd.read_csv("data/gdp_country_2020_2025.csv")

    # Transform wide → long
    df = df_raw.melt(
        id_vars="Country",
        var_name="Year",
        value_name="GDP"
    )

    # Data cleaning
    df["Year"] = df["Year"].astype(int)
    df["GDP"] = pd.to_numeric(df["GDP"], errors="coerce")

    # Drop missing GDP (corporate-safe)
    df = df.dropna(subset=["GDP"])

    return df

df = load_and_prepare_data()

# =========================================================
# SIDEBAR FILTER (CORPORATE SAFE)
# =========================================================
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

filtered_df = df[
    (df["Country"].isin(countries)) &
    (df["Year"].between(year_range[0], year_range[1]))
]

# =========================================================
# EXECUTIVE KPI SECTION
# =========================================================
st.subheader("📌 Executive Summary")

latest_year = df["Year"].max()
latest_df = df[df["Year"] == latest_year]

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Total Countries",
    df["Country"].nunique()
)

col2.metric(
    "Year Coverage",
    f"{df['Year'].min()}–{df['Year'].max()}"
)

col3.metric(
    "Highest GDP (Latest Year)",
    f"${latest_df['GDP'].max():,.0f}"
)

col4.metric(
    "Countries Reported (Latest Year)",
    latest_df["Country"].nunique()
)

st.markdown("---")

# =========================================================
# GDP TREND (TIME SERIES)
# =========================================================
st.subheader("📈 GDP Trend by Country")

if filtered_df.empty:
    st.warning("No data available for selected filters.")
else:
    fig_trend = px.line(
        filtered_df,
        x="Year",
        y="GDP",
        color="Country",
        markers=True,
        title="GDP Trend (2020–2025)",
        template="plotly_white"
    )

    fig_trend.update_layout(
        xaxis_title="Year",
        yaxis_title="GDP (USD)",
        legend_title="Country"
    )

    st.plotly_chart(fig_trend, use_container_width=True)

# =========================================================
# GDP COMPARISON (SINGLE YEAR)
# =========================================================
st.subheader("📊 GDP Comparison by Country")

selected_year = st.selectbox(
    "Select Year for Comparison",
    sorted(df["Year"].unique()),
    index=len(sorted(df["Year"].unique())) - 1
)

year_df = df[df["Year"] == selected_year]

fig_bar = px.bar(
    year_df.sort_values("GDP", ascending=False),
    x="GDP",
    y="Country",
    orientation="h",
    title=f"GDP by Country – {selected_year}",
    template="plotly_white"
)

fig_bar.update_layout(
    xaxis_title="GDP (USD)",
    yaxis_title="Country"
)

st.plotly_chart(fig_bar, use_container_width=True)

# =========================================================
# INSIGHT SECTION (EXECUTIVE FRIENDLY)
# =========================================================
st.subheader("🧠 Key Insights")

top_country = year_df.sort_values("GDP", ascending=False).iloc[0]

st.info(
    f"In {selected_year}, **{top_country['Country']}** recorded the highest GDP "
    f"at **${top_country['GDP']:,.0f}**, indicating its dominant economic position."
)

# =========================================================
# DATA TABLE (OPTIONAL – FOR ANALYST)
# =========================================================
with st.expander("📄 View Data Table"):
    st.dataframe(filtered_df)

# =========================================================
# FOOTER
# =========================================================
st.markdown("---")
st.caption(
    "Source: Internal / World Bank-style GDP Data | "
    "For strategic and analytical purposes only"
)
