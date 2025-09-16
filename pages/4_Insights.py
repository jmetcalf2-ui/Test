from __future__ import annotations
import streamlit as st
import pandas as pd
from services.supabase_client import get_client
from services.queries import fetch_leads, fetch_evidence, fetch_supplements
from services.analytics import build_analytics

st.set_page_config(page_title="Insights · ACI", layout="wide", initial_sidebar_state="expanded")
with open("theme/base.css", "r") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

sb = get_client()
st.title("Insights")
st.caption("Deeper analytics, rankings, trendlines, comparatives. Export charts as PNG.")

leads = fetch_leads(sb, limit=1000)
evidence = fetch_evidence(sb)
supplements = fetch_supplements(sb)
ana = build_analytics(leads, evidence, supplements)

tab1, tab2, tab3 = st.tabs(["Rankings","Trends","Comparatives"])
with tab1:
    top = ana.sort_values("total", ascending=False).head(50)
    st.dataframe(top[["full_name","tier","lead_score","total","freshness_score","influence_proxy","diversity_index"]], use_container_width=True)
    st.download_button("Export CSV", data=top.to_csv(index=False), file_name="rankings.csv", mime="text/csv")
with tab2:
    st.line_chart(ana[["freshness_score","influence_proxy","diversity_index"]])
with tab3:
    t1, t2 = st.columns(2)
    with t1:
        st.bar_chart(ana.groupby("tier")["lead_score"].mean())
    with t2:
        st.bar_chart(ana.groupby("country")["freshness_score"].mean().sort_values(ascending=False).head(12))
