from __future__ import annotations
import streamlit as st
import pandas as pd
from services.supabase_client import get_client
from services.queries import fetch_leads, fetch_supplements
from services.analytics import similar_collectors

st.set_page_config(page_title="Interests · ACI", layout="wide", initial_sidebar_state="expanded")
with open("theme/base.css", "r") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

sb = get_client()
st.title("Interests")
st.caption("Explore interest tags; see associated collectors and similarity.")

leads = fetch_leads(sb, limit=1000)
supplements = fetch_supplements(sb)

# Facet by interest tags
all_tags = sorted({t for row in leads["interests"].dropna().tolist() for t in (row if isinstance(row, list) else [])})
tags = st.multiselect("Filter by interests", all_tags, [])
df = leads.copy()
if tags:
    df = df[df["interests"].apply(lambda L: L and all(t in L for t in tags))]

st.dataframe(df[["full_name","tier","lead_score","city","country","interests"]], use_container_width=True)
st.download_button("Export CSV", data=df.to_csv(index=False), file_name="interests_view.csv", mime="text/csv")

st.divider()
st.subheader("Similar collectors (by interests)")
sim = similar_collectors(leads, top_k=5)
sel = st.selectbox("Select a collector", leads["full_name"].tolist())
if sel:
    sel_id = leads.loc[leads["full_name"]==sel,"lead_id"].iloc[0]
    sims = sim.get(sel_id, [])
    if sims:
        ids = [sid for sid, s in sims]
        names = leads.set_index("lead_id").loc[ids, "full_name"].tolist()
        st.write(list(zip(names, [round(s,3) for _, s in sims])))
    else:
        st.info("No similar collectors found.")
