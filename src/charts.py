import streamlit as st
import plotly.express as px
import pandas as pd

def render_trend_chart(filtered_df: pd.DataFrame):
    st.subheader("📈 GDP Trend by Country")

    if filtered_df.empty:
        st.warning("No data available for selected filters.")
        return

    fig = px.line(
        filtered_df,
        x="Year",
        y="GDP",
        color="Country",
        markers=True,
        template="plotly_white"
    )

    st.plotly_chart(fig, use_container_width=True)


def render_bar_chart(df: pd.DataFrame, selected_year: int):
    st.subheader("📊 GDP Comparison by Country")

    year_df = df[df["Year"] == selected_year]

    if year_df.empty:
        st.warning("No data available for selected year.")
        return

    fig = px.bar(
        year_df.sort_values("GDP", ascending=False),
        x="GDP",
        y="Country",
        orientation="h",
        template="plotly_white"
    )

    st.plotly_chart(fig, use_container_width=True)

    top = year_df.sort_values("GDP", ascending=False).iloc[0]

    st.info(
        f"In {selected_year}, **{top['Country']}** recorded the highest GDP "
        f"at **${top['GDP']:,.0f}**."
    )
