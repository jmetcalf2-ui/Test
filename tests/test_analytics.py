import pandas as pd
from services.analytics import lead_score_decomposition

def test_lead_score_decomposition_smoke():
    leads = pd.DataFrame([
        {"lead_id":"1","full_name":"A","last_activity_at":"2024-01-01","interests":["X","Y"]},
        {"lead_id":"2","full_name":"B","last_activity_at":"2024-06-01","interests":["X"]},
    ])
    evidence = pd.DataFrame([{"lead_id":"1"},{"lead_id":"1"},{"lead_id":"2"}])
    supplements = pd.DataFrame([
        {"lead_id":"1","source_type":"museum","published_at":"2024-08-01","url":"https://moma.org/a"},
        {"lead_id":"2","source_type":"blog","published_at":"2024-04-01","url":"https://blog.com/b"}
    ])
    out = lead_score_decomposition(leads,evidence,supplements)
    assert set(out.columns) >= {"lead_id","recency","volume","source_mix","interest_depth","cadence_consistency","total"}
    assert len(out)==2
