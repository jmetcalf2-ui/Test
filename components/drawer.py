from __future__ import annotations
import streamlit as st

def drawer_header(title: str):
    st.markdown(f'<div class="ac-drawer"><h3>{title}</h3>', unsafe_allow_html=True)

def drawer_footer():
    st.markdown('</div>', unsafe_allow_html=True)
