from __future__ import annotations
import streamlit as st
import pandas as pd
from services.supabase_client import get_client
from services.queries import fetch_supplements, fetch_leads
from services.analytics import qa_health, freshness_score

st.set_page_config(page_title="Quality & Freshness · ACI", layout="wide", initial_sidebar_state="expanded")
with open("theme/base.css", "r") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

sb = get_client()
st.title("Quality & Freshness")
st.caption("QA flags, dedupe hints, recrawl suggestions, stale-link triage.")

supp = fetch_supplements(sb)
leads = fetch_leads(sb, limit=1000)

qa = qa_health(supp)
fresh = freshness_score(supp)

left, right = st.columns([1.5,1])
with left:
    st.subheader("QA by Lead")
    view = qa.merge(leads[["lead_id","full_name"]], on="lead_id", how="left").fillna(0)
    st.dataframe(view, use_container_width=True, height=520)
    st.download_button("Export QA CSV", data=view.to_csv(index=False), file_name="qa_by_lead.csv", mime="text/csv")
with right:
    st.subheader("Stale Links")
    # Simple rule: links older than 180d
    s = supp.copy()
    s["published_at"] = pd.to_datetime(s["published_at"], errors="coerce")
    stale_cut = pd.Timestamp.utcnow() - pd.Timedelta(days=180)
    stale = s[s["published_at"] < stale_cut]
    st.dataframe(stale[["lead_id","url","source_type","published_at","qa_flag"]].head(200), use_container_width=True, height=520)
