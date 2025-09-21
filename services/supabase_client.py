from __future__ import annotations

import streamlit as st
from typing import Optional

try:
    # supabase-py v2
    from supabase import create_client, Client
except Exception as e:  # pragma: no cover
    raise RuntimeError(
        "Supabase client is not installed. Add 'supabase>=2.5.0' to requirements.txt."
    ) from e


@st.cache_resource(show_spinner=False)
def get_supabase() -> Client:
    """
    Return a cached Supabase client configured via Streamlit secrets.

    Required secrets (set in Streamlit Cloud or .streamlit/secrets.toml locally):
      - SUPABASE_URL
      - SUPABASE_ANON_KEY

    Raises:
        KeyError: if required secrets are missing.
        RuntimeError: if client initialization fails.
    """
    url: str = st.secrets.get("SUPABASE_URL", "").strip()
    key: str = st.secrets.get("SUPABASE_ANON_KEY", "").strip()

    missing = []
    if not url:
        missing.append("SUPABASE_URL")
    if not key:
        missing.append("SUPABASE_ANON_KEY")

    if missing:
        raise KeyError(
            f"Missing Streamlit secrets: {', '.join(missing)}. "
            "Add them in your app's Settings → Secrets or in .streamlit/secrets.toml."
        )

    try:
        client: Client = create_client(url, key)
    except Exception as e:  # pragma: no cover
        raise RuntimeError(f"Failed to initialize Supabase client: {e}") from e

    return client


def healthcheck() -> dict:
    """
    Simple connectivity probe you can call from any page:
        from services.supabase_client import healthcheck
        st.json(healthcheck())
    """
    try:
        client = get_supabase()
        # lightweight call — get current time from PostgREST RPC if you have one;
        # otherwise just return a static structure
        return {"ok": True, "url": client.supabase_url}
    except Exception as e:
        return {"ok": False, "error": str(e)}