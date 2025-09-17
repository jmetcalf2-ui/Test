from __future__ import annotations
import streamlit as st

def pill(text: str):
    st.markdown(f'<span class="ac-pill">{text}</span>', unsafe_allow_html=True)
