# services/queries.py
from __future__ import annotations
from typing import List, Optional
import pandas as pd
import streamlit as st
from services.supabase_client import get_client

def _safe_select(df: pd.DataFrame, want: List[str]) -> pd.DataFrame:
    """Keep only columns that exist; add missing as empty so pages don't crash."""
    have = [c for c in want if c in df.columns]
    missing = [c for c in want if c not in df.columns]
    out = df[have].copy() if have else df.copy()
    for m in missing:
        out[m] = None
    return out

@st.cache_data(ttl=300, show_spinner=False)
def fetch_leads(
    min_score: int = 0,  # kept for UI; ignored if your schema lacks lead_score
    tiers: Optional[List[str]] = None,  # ignored if no 'tier' column
    country: str = "",
    city: str = "",
    q: str = "",
    limit: int = 1000,
) -> pd.DataFrame:
    sb = get_client()
    # Use your REAL table name
    qy = sb.table("leads").select("*")

    # Apply filters only if those columns exist in your schema
    if min_score and "lead_score" in qy._filters.keys():  # defensive; PostgREST ignores unknown keys poorly
        qy = qy.gte("lead_score", min_score)
    if tiers:
        # only apply if 'tier' exists
        qy = qy.in_("tier", tiers) if "tier" in qy._filters.keys() else qy
    if country:
        qy = qy.ilike("country", f"%{country}%") if "country" in qy._filters.keys() else qy
    if city:
        qy = qy.ilike("city", f"%{city}%") if "city" in qy._filters.keys() else qy
    if q:
        # OR search across fields that commonly exist; PostgREST requires real columns
        or_parts = []
        for col in ["full_name", "primary_role", "email", "city", "country"]:
            or_parts.append(f"{col}.ilike.%{q}%") if col in ["full_name","primary_role","email","city","country"] else None
        if or_parts:
            qy = qy.or_(",".join(or_parts))

    res = qy.limit(limit).execute()
    df = pd.DataFrame(res.data or [])

    # Normalize columns the UI expects (nonexistent ones become empty)
    expected = [
        "lead_id","full_name","city","country","tier","lead_score",
        "interests","last_activity_at","source_count","primary_role",
        "email","instagram","website"
    ]
    return _safe_select(df, expected)

@st.cache_data(ttl=300, show_spinner=False)
def fetch_evidence(lead_id: Optional[str] = None, limit: int = 5000) -> pd.DataFrame:
    sb = get_client()
    qy = sb.table("evidence").select("*").limit(limit)  # your REAL table
    if lead_id:
        qy = qy.eq("lead_id", lead_id)
    return pd.DataFrame(qy.execute().data or [])

@st.cache_data(ttl=300, show_spinner=False)
def fetch_supplements(lead_id: Optional[str] = None, limit: int = 5000) -> pd.DataFrame:
    sb = get_client()
    qy = sb.table("supplements").select("*").limit(limit)  # your REAL table
    if lead_id:
        qy = qy.eq("lead_id", lead_id)
    return pd.DataFrame(qy.execute().data or [])
