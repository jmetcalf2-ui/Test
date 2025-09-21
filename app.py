import os
import streamlit as st

st.set_page_config(
    page_title="Dashboard",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Inject CSS
with open(os.path.join("assets", "style.css"), "r", encoding="utf-8") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Lightweight landing content (kept minimal by request)
st.switch_page("pages/1_Dashboard.py")