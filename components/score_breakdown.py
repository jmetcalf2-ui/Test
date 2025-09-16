from __future__ import annotations
import streamlit as st
import pandas as pd

def breakdown_row(row: pd.Series):
    bars = []
    for k in ["recency","volume","source_mix","interest_depth","cadence_consistency"]:
        bars.append(f"""
        <div style='display:flex;align-items:center;gap:8px;margin:6px 0;'>
          <div style='width:140px;color:var(--muted);font-size:0.85rem'>{k.replace('_',' ').title()}</div>
          <div style='flex:1;background:#1f2937;border-radius:10px;overflow:hidden;height:8px'>
            <div style='width:{row.get(k,0)}%;height:8px;background:var(--accent)'></div>
          </div>
          <div style='width:42px;text-align:right'>{row.get(k,0):.0f}</div>
        </div>
        """)
    st.markdown("""<div class='ac-card'>"""+"".join(bars)+"""</div>""", unsafe_allow_html=True)
