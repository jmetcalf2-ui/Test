import os
import pandas as pd
import streamlit as st

st.set_page_config(page_title="Collectors", layout="wide")

# Load CSS
with open(os.path.join("assets", "style.css"), "r", encoding="utf-8") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

st.header("Collectors")
st.caption("Search & filter — showcase only")

# Demo search/filter UI
q = st.text_input("Search by name, city, or country", placeholder="e.g., Bruce Nauman, New York, USA")
tier = st.multiselect("Tier", options=["A", "B", "C"], default=[])
region = st.selectbox("Region", ["Any", "North America", "Europe", "Asia", "Other"], index=0)

# Simulated data frame for layout testing
data = pd.DataFrame({
    "full_name": ["Alice Li", "Bob Mendoza", "Carla Noor", "David Osei"],
    "city": ["New York", "Los Angeles", "London", "Berlin"],
    "country": ["USA", "USA", "UK", "Germany"],
    "tier": ["A", "B", "A", "C"],
    "lead_score": [87, 72, 91, 63]
})
st.dataframe(data, use_container_width=True)