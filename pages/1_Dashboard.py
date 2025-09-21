from __future__ import annotations

import os
import pandas as pd
import streamlit as st

from services.supabase_client import get_supabase, healthcheck

st.set_page_config(page_title="Dashboard", layout="wide")

# Inject CSS
with open(os.path.join("assets", "style.css"), "r", encoding="utf-8") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

st.header("Dashboard")
st.caption("Connected to Supabase • White background • Helvetica")

# Connectivity check
hc = healthcheck()
if not hc.get("ok"):
    st.error("Supabase is not configured yet. Add SUPABASE_URL and SUPABASE_ANON_KEY to Streamlit secrets.")
    st.stop()

# Controls
with st.container():
    c1, c2, c3 = st.columns([2, 1, 1])
    with c1:
        q = st.text_input("Search by name, city, or country", placeholder="e.g., Bruce Nauman, New York, USA")
    with c2:
        tier = st.multiselect("Tier", options=["A", "B", "C"], placeholder="Any")
    with c3:
        limit = st.number_input("Max rows", min_value=10, max_value=2000, value=200, step=10)

supabase = get_supabase()

def run_query(table_name: str):
    query = supabase.table(table_name).select("*")
    if q:
        like = f"%{q}%"
        # apply ilike to common columns
        query = query.or_(f"full_name.ilike.{like},city.ilike.{like},country.ilike.{like}")
    if tier:
        query = query.in_("tier", tier)
    query = query.limit(int(limit))
    return query.execute()

rows = []
active_table = None
error_msg = None

# Try leads_rows first, then leads
for t in ("leads_rows", "leads"):
    try:
        resp = run_query(t)
        rows = resp.data or []
        active_table = t
        break
    except Exception as e:
        error_msg = str(e)
        continue

if active_table is None:
    st.error(f"Query failed. Last error: {error_msg}")
    st.stop()

if not rows:
    st.info(f"No rows found in '{active_table}'. Adjust filters or add data.")
else:
    df = pd.DataFrame(rows)
    preferred = [c for c in ["full_name", "city", "country", "tier", "lead_score", "lead_id", "updated_at", "id"] if c in df.columns]
    remaining = [c for c in df.columns if c not in preferred]
    df = df[preferred + remaining] if preferred else df
    st.dataframe(df, use_container_width=True, hide_index=True)
    st.caption(f"Showing data from **{active_table}**")
