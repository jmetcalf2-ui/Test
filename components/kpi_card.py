from __future__ import annotations
import streamlit as st

def kpi(label: str, value: str, delta: str | None = None):
    st.markdown(
        f'''<div class="ac-card ac-kpi hover-raise">
            <div class="label">{label}</div>
            <div class="value">{value}</div>
            {f'<div class="delta">{delta}</div>' if delta else ''}
        </div>''',
        unsafe_allow_html=True,
    )
