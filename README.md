# ACI · Streamlit Refresh (Supabase/ChatGPT-inspired)

Sleek, minimal, professional refresh for your existing Streamlit app. Schema unchanged.

## Quick Start

1. **Env**: create `.env` or set secrets with:
```
SUPABASE_URL=...
SUPABASE_ANON_KEY=...
```
2. **Install**
```
pip install -r requirements.txt
```
3. **Run**
```
streamlit run streamlit_app.py
```

## Structure

- `theme/` — tokens in `config.toml`, CSS in `base.css` (rounded corners, soft shadows, subtle motion).
- `components/` — small, composable UI helpers (KPI cards, pills, drawer simulation).
- `services/` — `supabase_client.py`, `queries.py` (cached reads; respects RLS), `analytics.py` (pure functions).
- `pages/` — `Overview`, `Collectors`, `Interests`, `Insights`, `Quality & Freshness`.
- `tests/` — unit tests for analytics.

## Notes

- No schema changes; all reads respect RLS via Supabase policies.
- Light/Dark mode: top bar toggle writes `data-theme` attribute for CSS variables.
- CSV export buttons on key tables; PNG export can be done via browser or Streamlit screenshot add-ons.
