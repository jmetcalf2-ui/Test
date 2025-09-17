from __future__ import annotations
import streamlit as st
import pandas as pd
from services.queries import fetch_leads, fetch_evidence, fetch_supplements
from services.analytics import build_analytics
from components.score_breakdown import breakdown_row

st.set_page_config(page_title="Collectors · ACI", layout="wide", initial_sidebar_state="expanded")

with open("theme/base.css","r") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

st.markdown('''
<div class="ac-topbar">
  <div class="title">Collectors</div>
  <div class="controls"><span class="ac-icon">🔎</span><span style="color:var(--text-muted)">Search & filter your roster</span></div>
</div>
''', unsafe_allow_html=True)

st.caption("Search, filter, and inspect collectors; drawer shows details and suggested actions.")

# Filters
c0,c1,c2,c3,c4 = st.columns([2,1,1,1,2])
with c0: q = st.text_input("Global search (name/role/email/city/country)", "")
with c1: min_score = st.slider("Min score", 0, 100, 0)
with c2: tier = st.multiselect("Tier", ["A","B","C"], [])
with c3: city = st.text_input("City contains","")
with c4: country = st.text_input("Country contains","")

leads = fetch_leads(min_score=min_score, tiers=tier, country=country, city=city, q=q, limit=1000)
evidence = fetch_evidence()
supplements = fetch_supplements()
ana = build_analytics(leads, evidence, supplements)

left, right = st.columns([2.1,1.4], gap="large")

with left:
    if leads.empty:
        st.info("No leads match current filters.")
    else:
        table = ana[["full_name","tier","lead_score","freshness_score","vel_30d","z_30d","influence_proxy","diversity_index"]].copy()
        st.dataframe(table, use_container_width=True, height=520)
        st.download_button("Export table CSV", data=table.to_csv(index=False), file_name="collectors_table.csv", mime="text/csv")

with right:
    st.markdown("<div class='ac-drawer'>", unsafe_allow_html=True)
    sel = st.selectbox("Choose a collector", leads["full_name"].tolist())
    if sel:
        row = ana[ana["full_name"]==sel].iloc[0]
        st.subheader(sel)
        st.markdown(f"**Tier:** {row['tier']}  •  **Lead Score:** {row['lead_score']:.1f}")
        st.markdown(f"**Freshness:** {row['freshness_score']:.1f}  •  **Velocity (30d):** {row['vel_30d']:.0f} (z={row['z_30d']:.2f})")
        st.markdown(f"**Influence Proxy:** {row['influence_proxy']:.1f}  •  **Diversity:** {row['diversity_index']:.1f}")
        st.markdown("**Score Breakdown**")
        breakdown_row(row)
        st.markdown("**Suggested actions**")
        actions = []
        if row['freshness_score'] < 30: actions.append("Review stale links; add 1–2 recent museum/press sources.")
        if row['z_30d'] > 1.0: actions.append("Engagement spike: consider outreach or note in CRM.")
        if row['diversity_index'] < 30: actions.append("Low diversity: seek more varied sources & interests.")
        if not actions: actions = ["No immediate actions detected."]
        for a in actions: st.markdown(f"- {a}")
    st.markdown("</div>", unsafe_allow_html=True)
