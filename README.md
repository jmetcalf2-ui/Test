# Streamlit App — White Background (Helvetica), No Top Clipping

This template sets **white background**, **black text**, and **Helvetica** (via CSS) across the app, and adds **safe top padding** to ensure **no text is cut off at the top**.

## Quick Start

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Structure

```
.
├── .streamlit/
│   └── config.toml        # light theme, white bg, black text
├── assets/
│   └── style.css          # Helvetica, safe top padding, cards, tables
├── pages/
│   ├── 1_Dashboard.py
│   └── 2_Collectors.py
├── services/
│   └── supabase_client.py # optional stub; won’t crash if not configured
├── app.py                 # main entry
├── requirements.txt
└── README.md
```

## Theme & Styling

- Background = **#FFFFFF**
- Text = **#000000**
- Font = **Helvetica** (with fallbacks)
- Safe top padding on `.block-container` prevents clipped headings.

If you still see clipping on certain deployments, increase the top padding in `assets/style.css`:

```css
.block-container {
  padding-top: 2.25rem !important;
}
```

## Deploy to Streamlit Cloud

1. Push this folder to a GitHub repo.
2. In Streamlit Cloud, create a new app and point to `app.py`.
3. Add any required environment variables (e.g., `SUPABASE_URL`, `SUPABASE_ANON_KEY`) if you wire up the backend.

## Notes

- This template focuses on **look & layout**; analytics/data hooks can be added to `pages/` and `services/`.
- The UI avoids any clipping at the top and enforces a **clean white aesthetic** site‑wide.