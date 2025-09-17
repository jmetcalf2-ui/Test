from __future__ import annotations
from typing import List, Optional
import pandas as pd
import streamlit as st
from services.supabase_client import get_client

# NOTE: Do not pass the Supabase client into cached functions; create it inside each function.

@st.cache_data(ttl=300, show_spinner=False)
def fetch_leads(
    min_score: int = 0,
    tiers: Optional[List[str]] = None,
    country: str = "",
    city: str = "",
    q: str = "",
    limit: int = 1000,
) -> pd.DataFrame:
    sb = get_client()
    qy = sb.table("leads_rows").select(
        "lead_id,full_name,city,country,tier,lead_score,interests,"
        "last_activity_at,source_count,primary_role,email,instagram,website"
    ).gte("lead_score", min_score)
    if tiers: qy = qy.in_("tier", tiers)
    if country: qy = qy.ilike("country", f"%{country}%")
    if city: qy = qy.ilike("city", f"%{city}%")
    if q: qy = qy.or_(f"full_name.ilike.%{q}%,primary_role.ilike.%{q}%,email.ilike.%{q}%")
    res = qy.order("lead_score", desc=True).limit(limit).execute()
    return pd.DataFrame(res.data or [])

@st.cache_data(ttl=300, show_spinner=False)
def fetch_evidence(lead_id: Optional[str] = None, limit: int = 5000) -> pd.DataFrame:
    sb = get_client()
    qy = sb.table("evidence_rows").select("*").limit(limit)
    if lead_id: qy = qy.eq("lead_id", lead_id)
    return pd.DataFrame(qy.execute().data or [])

@st.cache_data(ttl=300, show_spinner=False)
def fetch_supplements(lead_id: Optional[str] = None, limit: int = 5000) -> pd.DataFrame:
    sb = get_client()
    qy = sb.table("supplements_rows").select("*").limit(limit)
    if lead_id: qy = qy.eq("lead_id", lead_id)
    return pd.DataFrame(qy.execute().data or [])
