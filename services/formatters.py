from __future__ import annotations
from typing import Optional
import pandas as pd

def fmt_date(x: Optional[str]) -> str:
    try:
        return pd.to_datetime(x).strftime("%Y-%m-%d")
    except Exception:
        return "—"

def badge_for_tier(tier: str) -> str:
    if not tier:
        return '<span class="ac-pill">Tier —</span>'
    return f'<span class="ac-pill">Tier {tier}</span>'
