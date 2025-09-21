import os
import streamlit as st

st.set_page_config(page_title="Dashboard", layout="wide")

# Ensure CSS is loaded on each page
with open(os.path.join("assets", "style.css"), "r", encoding="utf-8") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

st.header("Dashboard")
st.caption("White background • Helvetica • Safe top padding")

c1, c2 = st.columns([2, 1])

with c1:
    st.subheader("Activity Overview")
    st.write("Add charts here (Plotly/Altair) to visualize activity trends.")

with c2:
    st.subheader("Highlights")
    st.write("- New links added this week")
    st.write("- Collectors with rising interest momentum")
    st.write("- Items needing QA review")