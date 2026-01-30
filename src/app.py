import streamlit as st
from src.data_loader import load_data
from src.filters import sidebar_filters
from src.kpi import render_kpis
from src.charts import render_trend_chart, render_bar_chart

st.set_page_config(
    page_title="Global GDP Dashboard",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("🌍 Global GDP Dashboard (2020–2025)")
st.caption("Executive Economic Intelligence | Country-Level GDP Analysis")
st.markdown("---")

df = load_data()

if df.empty:
    st.error("Dataset is empty or failed to load.")
    st.stop()

filtered_df, selected_year = sidebar_filters(df)

render_kpis(df)

st.markdown("---")

render_trend_chart(filtered_df)
render_bar_chart(df, selected_year)

with st.expander("📄 View Data Table"):
    st.dataframe(filtered_df, use_container_width=True)

st.markdown("---")
st.caption(
    "Source: Internal / World Bank-style GDP Data | "
    "For strategic and analytical purposes only"
)
