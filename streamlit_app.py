from __future__ import annotations
import streamlit as st
import os

st.set_page_config(page_title="Art Collector Intelligence", layout="wide")

# Load our CSS (tokens + components)
with open("theme/base.css","r") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Top bar (simple)
col1, col2, col3 = st.columns([2,1,1])
with col1:
    st.markdown("### Art Collector Intelligence")
with col2:
    if "theme_mode" not in st.session_state:
        st.session_state.theme_mode = "dark"
    if st.toggle("Light mode", value=(st.session_state.theme_mode=="light")):
        st.session_state.theme_mode = "light"
        st.markdown("<script>document.documentElement.setAttribute('data-theme','light');</script>", unsafe_allow_html=True)
    else:
        st.session_state.theme_mode = "dark"
        st.markdown("<script>document.documentElement.setAttribute('data-theme','dark');</script>", unsafe_allow_html=True)
with col3:
    st.text_input("Global search", placeholder="Type to search in pages… (prototype)")

st.info("Use the left 'Pages' navigation to explore: Overview, Collectors, Interests, Insights, Quality & Freshness.")
