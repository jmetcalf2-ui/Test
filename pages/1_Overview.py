from __future__ import annotations
import streamlit as st
import pandas as pd
from services.supabase_client import get_client
from services.queries import fetch_leads, fetch_evidence, fetch_supplements
from services.analytics import build_analytics
from components.kpi_card import kpi

st.set_page_config(page_title="Overview · ACI", layout="wide", initial_sidebar_state="collapsed")

# Inject CSS
with open("theme/base.css", "r") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

sb = get_client()

st.title("Overview")
st.caption("At-a-glance insights and recent changes")

leads = fetch_leads(sb, min_score=0, tiers=None, limit=1000)
evidence = fetch_evidence(sb)
supplements = fetch_supplements(sb)

ana = build_analytics(leads, evidence, supplements)

# KPI Row
c1, c2, c3, c4 = st.columns(4)
with c1: kpi("Total Collectors", f"{len(leads):,}")
with c2: kpi("Avg Lead Score", f"{ana['lead_score'].mean():.1f}")
with c3: kpi("Freshness (avg)", f"{ana['freshness_score'].mean():.1f}")
with c4: kpi("QA Flags (sum)", f"{int(ana.filter(like='qa_').sum(numeric_only=True).sum())}")

st.divider()

# Table of "What Changed" (placeholder heuristic: top delta in 30d velocity or freshness)
st.subheader("What Changed")
if "vel_30d" in ana.columns:
    top = ana.sort_values(["z_30d","freshness_score"], ascending=[False, False]).head(15)
    st.dataframe(top[["full_name","tier","lead_score","vel_30d","z_30d","freshness_score","influence_proxy","diversity_index"]],
                 use_container_width=True)
else:
    st.info("No recent activity detected.")

st.divider()
st.subheader("Segment Builder (session-only)")
tier = st.multiselect("Tier", ["A","B","C"], [])
region = st.text_input("Region (country contains)","")
score_range = st.slider("Lead Score range", 0, 100, (0,100))
q = st.text_input("Keyword (name/role/email)","")
btn = st.button("Build Segment")
if btn:
    seg = leads.copy()
    if tier: seg = seg[seg["tier"].isin(tier)]
    if region: seg = seg[seg["country"].str.contains(region, case=False, na=False)]
    seg = seg[(seg["lead_score"].fillna(0).between(score_range[0], score_range[1]))]
    if q:
        ql = q.lower()
        seg = seg[seg["full_name"].str.lower().str.contains(ql, na=False) | seg["email"].str.lower().str.contains(ql, na=False)]
    st.success(f"Segment size: {len(seg)}")
    st.dataframe(seg[["full_name","tier","lead_score","city","country"]], use_container_width=True)
    st.download_button("Export CSV", data=seg.to_csv(index=False), file_name="segment.csv", mime="text/csv")
