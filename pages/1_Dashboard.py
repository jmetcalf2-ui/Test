from __future__ import annotations

import os
import time
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
    c1, c2, c3 = st.columns([2,1,1])
    with c1:
        q = st.text_input("Search by name, city, or country", placeholder="e.g., Bruce Nauman, New York, USA")
    with c2:
        tier = st.multiselect("Tier", options=["A","B","C"], placeholder="Any")
    with c3:
        limit = st.number_input("Max rows", min_value=10, max_value=2000, value=200, step=10)

# Query Supabase
supabase = get_supabase()

query = supabase.table("leads_rows").select("*")

# Apply basic filters
if q:
    # Use ilike on several columns (if they exist). Missing columns will be ignored by server,
    # but to be safe, we keep a single ilike on full_name and city/country when available.
    # supabase-py v2 supports 'or' in filter string
    like = f"%{q}%"
    query = query.or_(f"full_name.ilike.{like},city.ilike.{like},country.ilike.{like}")

if tier:
    # Use in_ filter
    query = query.in_("tier", tier)

query = query.limit(int(limit))

try:
    resp = query.execute()
    rows = resp.data or []
except Exception as e:
    st.error(f"Query failed: {e}")
    st.stop()

if not rows:
    st.info("No rows found. Adjust filters or add data to the 'leads_rows' table.")
else:
    df = pd.DataFrame(rows)
    # Reorder a few likely columns if present
    preferred = [c for c in ["full_name","city","country","tier","lead_score","lead_id","updated_at"] if c in df.columns]
    remaining = [c for c in df.columns if c not in preferred]
    df = df[preferred + remaining] if preferred else df
    st.dataframe(df, use_container_width=True, hide_index=True)