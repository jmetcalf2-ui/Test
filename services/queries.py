from __future__ import annotations
from typing import List, Dict, Any, Optional, Tuple
import pandas as pd
import streamlit as st
from supabase import Client

# ---- Read helpers (respect RLS; do not alter schema) ----
@st.cache_data(show_spinner=False, ttl=300)
def fetch_leads(sb: Client, min_score: int = 0, tiers: Optional[List[str]] = None,
                country: str = "", city: str = "", q: str = "", limit: int = 1000) -> pd.DataFrame:
    query = sb.table("leads_rows").select(
        "lead_id,full_name,city,country,tier,lead_score,interests,last_activity_at,source_count,primary_role,email,instagram,website"
    ).gte("lead_score", min_score)
    if tiers:
        query = query.in_("tier", tiers)
    if country:
        query = query.ilike("country", f"%{country}%")
    if city:
        query = query.ilike("city", f"%{city}%")
    if q:
        query = query.or_(f"full_name.ilike.%{q}%,primary_role.ilike.%{q}%,email.ilike.%{q}%")
    res = query.order("lead_score", desc=True).limit(limit).execute()
    return pd.DataFrame(res.data or [])

@st.cache_data(show_spinner=False, ttl=300)
def fetch_evidence(sb: Client, lead_id: Optional[str]=None, limit:int=5000) -> pd.DataFrame:
    query = sb.table("evidence_rows").select("*").limit(limit)
    if lead_id:
        query = query.eq("lead_id", lead_id)
    return pd.DataFrame(query.execute().data or [])

@st.cache_data(show_spinner=False, ttl=300)
def fetch_supplements(sb: Client, lead_id: Optional[str]=None, limit:int=5000) -> pd.DataFrame:
    # expected columns include: url, source_type, published_at, qa_flag, domain, evidence_id, lead_id
    query = sb.table("supplements_rows").select("*").limit(limit)
    if lead_id:
        query = query.eq("lead_id", lead_id)
    return pd.DataFrame(query.execute().data or [])
