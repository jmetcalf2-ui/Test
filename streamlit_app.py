from __future__ import annotations
import streamlit as st

st.set_page_config(page_title="Art Collector Intelligence", layout="wide")

# Load CSS
with open("theme/base.css","r") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# GitHub-like top bar with icons
st.markdown('''
<div class="ac-topbar">
  <div class="title">Art Collector Intelligence</div>
  <div class="controls">
    <span class="ac-icon">🏠</span><span style="color:var(--text-muted)">Use sidebar Pages</span>
    <span class="ac-icon">🌗</span><span style="color:var(--text-muted)">Theme in sidebar</span>
  </div>
</div>
''', unsafe_allow_html=True)

st.info("Use the left 'Pages' navigation to explore: Overview, Collectors, Interests, Insights, Quality & Freshness.")
