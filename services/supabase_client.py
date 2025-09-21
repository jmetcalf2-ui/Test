import os

# Placeholder for your Supabase client setup.
# This file will not error if env vars are missing; it simply provides
# a function you can complete when ready.

def get_supabase():
    url = os.getenv("SUPABASE_URL", "")
    key = os.getenv("SUPABASE_SERVICE_ROLE_KEY", "") or os.getenv("SUPABASE_ANON_KEY", "")
    if not url or not key:
        # Return None to keep the app running without configured backend.
        return None
    try:
        from supabase import create_client, Client
        return create_client(url, key)
    except Exception:
        return None