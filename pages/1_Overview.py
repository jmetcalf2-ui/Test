from __future__ import annotations
import streamlit as st
import pandas as pd
from services.queries import fetch_leads, fetch_evidence, fetch_supplements
from services.analytics import build_analytics
from components.kpi_card import kpi

st.set_page_config(page_title="Overview · ACI", layout="wide", initial_sidebar_state="collapsed")

with open("theme/base.css","r") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Top bar
st.markdown('''
<div class="ac-topbar">
  <div class="title">Art Collector Intelligence · Overview</div>
  <div class="controls">
    <div class="ac-icon">🌗</div><div style="color:var(--text-muted)">Toggle theme in sidebar</div>
  </div>
</div>
''', unsafe_allow_html=True)

leads = fetch_leads(min_score=0, tiers=None, limit=1000)
evidence = fetch_evidence()
supplements = fetch_supplements()
ana = build_analytics(leads, evidence, supplements)

# KPI row
c1,c2,c3,c4 = st.columns(4)
with c1: kpi("Total Collectors", f"{len(leads):,}", icon="👥")
with c2: kpi("Avg Lead Score", f"{ana['lead_score'].mean():.1f}", icon="⭐")
with c3: kpi("Freshness (avg)", f"{ana['freshness_score'].mean():.1f}", icon="🕒")
with c4: kpi("QA Flags (sum)", f"{int(ana.filter(like='qa_').sum(numeric_only=True).sum())}", icon="🧪")

st.markdown('<div class="ac-section">', unsafe_allow_html=True)
st.subheader("What Changed")
if "vel_30d" in ana.columns:
    top = ana.sort_values(["z_30d","freshness_score"], ascending=[False, False]).head(15)
    st.dataframe(top[["full_name","tier","lead_score","vel_30d","z_30d","freshness_score","influence_proxy","diversity_index"]],
                 use_container_width=True)
else:
    st.info("No recent activity detected.")
st.markdown('</div>', unsafe_allow_html=True)
