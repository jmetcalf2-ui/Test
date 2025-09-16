from __future__ import annotations
import streamlit as st
import numpy as np

def sparkline(data):
    # minimal sparkline using st.line_chart for now
    if len(data) < 2:
        data = np.array([0, *data, 0])
    st.line_chart(data, height=60)
