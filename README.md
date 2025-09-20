# Collector Intelligence Dashboard (Streamlit)

Minimal, all-white Streamlit app with black Helvetica (via CSS) and clearly visible headings. Includes a sidebar navigation and simple analytics.

## Quickstart (Local)

1. **Create and activate a virtual environment (optional but recommended):**
   ```bash
   python -m venv .venv
   source .venv/bin/activate   # macOS/Linux
   .venv\Scripts\activate    # Windows
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the app:**
   ```bash
   streamlit run streamlit_app.py
   ```

The app will open at http://localhost:8501 (or similar).

## Deploy to GitHub + Streamlit Cloud

1. Create a new GitHub repo (public or private).
2. Upload all files in this folder to the repo root.
3. In Streamlit Community Cloud: **New app** → Connect your GitHub repo → Select `streamlit_app.py` as the entrypoint.
4. Deploy.

## Customization

- Replace the demo DataFrame with your Supabase query/connector.
- The Helvetica/black-on-white style is set via a CSS block in `streamlit_app.py`. You can adjust font sizes for headings there.
- For larger apps, add more pages or modules and extend the sidebar navigation.

## Files
- `streamlit_app.py` — main app
- `requirements.txt` — Python dependencies
- `.streamlit/config.toml` — Streamlit theme configuration
- `README.md` — setup and deployment instructions
