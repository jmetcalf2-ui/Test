from __future__ import annotations
import os
from typing import Optional
from supabase import create_client, Client
import streamlit as st

def get_client() -> Client:
    """Create a Supabase client using Streamlit secrets or env vars. Raises AssertionError if missing."""
    url = st.secrets.get("SUPABASE_URL", os.environ.get("SUPABASE_URL"))
    key = st.secrets.get("SUPABASE_ANON_KEY", os.environ.get("SUPABASE_ANON_KEY"))
    assert url and key, "Set SUPABASE_URL and SUPABASE_ANON_KEY in secrets/.env"
    return create_client(url, key)
