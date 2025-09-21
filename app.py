import os
import streamlit as st

st.set_page_config(
    page_title="Collector Intelligence — Overview",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Inject custom CSS (Helvetica, white background, safe top padding)
with open(os.path.join("assets", "style.css"), "r", encoding="utf-8") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

st.title("Collector Intelligence")
st.caption("All-white interface • Helvetica • Nothing clipped at the top")

st.write(
    "Welcome! Use the pages on the left (or the tabs below) to explore analytics "
    "and manage your insights without any text being clipped at the top."
)

# Simple overview tiles
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="metric-title">Total Collectors</div>', unsafe_allow_html=True)
    st.markdown('<div class="metric-value">1,000</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="metric-title">Active (90d)</div>', unsafe_allow_html=True)
    st.markdown('<div class="metric-value">412</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

with col3:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="metric-title">New Links (30d)</div>', unsafe_allow_html=True)
    st.markdown('<div class="metric-value">287</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

with col4:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="metric-title">QA Flags</div>', unsafe_allow_html=True)
    st.markdown('<div class="metric-value">9</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown("### Getting Started")
st.markdown("""
• Navigate to **Dashboard** for a quick pulse.  
• Open **Collectors** to search, filter, and view details.  
• Use **Insights** for advanced analytics around ranking and interests.
""")

st.info("This starter is configured to use a white background and Helvetica. If you still see clipping, increase the top padding in assets/style.css.")
