# ACI · Streamlit Refresh (Professional / GitHub-adjacent)

This package refines the UI (sans-serif system stack, neutral panels, subtle borders, icons), fixes Streamlit caching errors, and keeps your Supabase schema intact.

## Python
Pinned via `runtime.txt` → **python-3.11**

## Secrets (TOML)
Set in Streamlit Cloud (or `.streamlit/secrets.toml` locally):
```
SUPABASE_URL="https://...supabase.co"
SUPABASE_ANON_KEY="..."
```

## Run
```
pip install -r requirements.txt
streamlit run streamlit_app.py
```

## Changes vs previous package
- **Caching fix**: cached functions create the Supabase client internally.
- **Design**: GitHub-adjacent top bar, icons, system UI font stack, cleaner tables.
- **.gitignore** + **runtime.txt** added.
