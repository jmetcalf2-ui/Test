import os
import streamlit as st
from supabase import create_client, Client
import pandas as pd
from sentence_transformers import SentenceTransformer

st.set_page_config(page_title="Art Collector Intelligence", layout="wide")

SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_ANON_KEY = os.environ.get("SUPABASE_ANON_KEY")
assert SUPABASE_URL and SUPABASE_ANON_KEY, "Set SUPABASE_URL and SUPABASE_ANON_KEY in secrets"

sb: Client = create_client(SUPABASE_URL, SUPABASE_ANON_KEY)
embedder = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

st.title("🎯 Art Collector Intelligence")

# Sidebar filters
with st.sidebar:
    st.header("Filters")
    min_score = st.slider("Min Collector Confidence", 0, 100, 0)
    tier_sel = st.multiselect("Tier", ["A","B","C"], [])
    country = st.text_input("Country contains", "")
    city = st.text_input("City contains", "")
    q = st.text_input("Keyword filter (name/role)", "")

# Fetch leads (basic filter)
query = sb.table("leads").select("lead_id,full_name,primary_role,collector_confidence,tier,city,country,instagram,website,last_activity_at,source_count").gte("collector_confidence", min_score)
if tier_sel:
    query = query.in_("tier", tier_sel)
if country:
    query = query.ilike("country", f"%{country}%")
if city:
    query = query.ilike("city", f"%{city}%")
if q:
    query = query.or_(f"full_name.ilike.%{q}%,primary_role.ilike.%{q}%")

res = query.order("collector_confidence", desc=True).limit(500).execute()
leads_df = pd.DataFrame(res.data or [])

col1, col2 = st.columns([2,3])
with col1:
    st.subheader("Leads")
    if not leads_df.empty:
        st.dataframe(leads_df[["full_name","collector_confidence","tier","city","country","source_count"]], use_container_width=True, height=480)
    else:
        st.info("No leads found.")

with col2:
    st.subheader("Details")
    if not leads_df.empty:
        selected_name = st.selectbox("Select lead", leads_df["full_name"].tolist())
        if selected_name:
            lead_row = leads_df[leads_df.full_name == selected_name].iloc[0]
            st.markdown(f"**Name:** {lead_row.full_name}")
            st.markdown(f"**Role:** {lead_row.primary_role or '—'} | **Score:** {lead_row.collector_confidence} | **Tier:** {lead_row.tier or '—'}")
            st.markdown(f"**Location:** {lead_row.city or '—'}, {lead_row.country or '—'}")
            if lead_row.instagram:
                st.markdown(f"**Instagram:** {lead_row.instagram}")
            if lead_row.website:
                st.markdown(f"**Website:** {lead_row.website}")

st.divider()

st.subheader("🔎 Semantic Search (pgvector)")
sem_q = st.text_input("Describe the lead you're looking for (e.g., 'Twombly collectors in New York')")
if st.button("Search") and sem_q.strip():
    q_emb = embedder.encode([sem_q], normalize_embeddings=True)[0].tolist()
    res = sb.rpc("rpc_semantic_search_leads", {"query_embedding": q_emb, "match_count": 50, "min_score": 0.2}).execute()
    sem_df = pd.DataFrame(res.data or [])
    if not sem_df.empty:
        sem_df["score"] = (sem_df["score"] * 100).round(1)
        st.dataframe(sem_df[["full_name","score","tier","city","country","collector_confidence"]], use_container_width=True)
    else:
        st.warning("No semantic matches above threshold.")
