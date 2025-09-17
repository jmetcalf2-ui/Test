from __future__ import annotations
from typing import Dict, List, Tuple, Optional
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# ---- Helper: safe list conversion ----
def _to_list(x) -> List[str]:
    if isinstance(x, list):
        return x
    if pd.isna(x) or x is None:
        return []
    if isinstance(x, str):
        # attempt to parse comma-separated tags
        return [t.strip() for t in x.split(",") if t.strip()]
    return []

# 1) Lead Score Decomposition
def lead_score_decomposition(leads: pd.DataFrame, evidence: pd.DataFrame, supplements: pd.DataFrame) -> pd.DataFrame:
    """Return sub-scores normalized to 0-100 and a total (does not overwrite your lead_score).
    Columns: recency, volume, source_mix, interest_depth, cadence_consistency, total
    """
    df = leads.copy()
    # recency: days since last_activity_at (lower better)
    recency_days = pd.to_datetime(df["last_activity_at"], errors="coerce")
    recency_days = (pd.Timestamp.utcnow() - recency_days).dt.days.replace({np.nan: 9999})
    recency = 100 * (1 - (recency_days / (recency_days.max() or 1)))
    # volume: evidence + supplements counts per lead
    ev_counts = evidence.groupby("lead_id").size().rename("ev_n")
    sup_counts = supplements.groupby("lead_id").size().rename("sup_n")
    vol = (ev_counts.reindex(df.lead_id).fillna(0) + sup_counts.reindex(df.lead_id).fillna(0))
    if vol.max() == 0: volume_norm = vol
    else: volume_norm = 100 * vol / vol.max()

    # source_mix: museums/press get more weight if present
    src_weights = {"museum": 1.0, "press": 0.9, "official": 0.8, "gallery": 0.7, "blog": 0.4}
    sup = supplements.copy()
    sup["w"] = sup["source_type"].str.lower().map(src_weights).fillna(0.5)
    mix = sup.groupby("lead_id")["w"].mean().rename("mix_w").reindex(df.lead_id).fillna(0)
    mix_norm = 100 * mix / (mix.max() or 1)

    # interest_depth: unique interests length
    interests_len = df["interests"].apply(_to_list).apply(len)
    depth_norm = 100 * interests_len / (interests_len.max() or 1)

    # cadence consistency: std of monthly supplements count (lower std => steadier => higher score)
    sup["_month"] = pd.to_datetime(sup["published_at"], errors="coerce").dt.to_period("M")
    cadence = sup.groupby(["lead_id", "_month"]).size().groupby("lead_id").std().rename("cad_std")
    cad_norm = 100 * (1 - (cadence.reindex(df.lead_id).fillna(0) / (cadence.max() or 1)))

    result = pd.DataFrame({
        "lead_id": df.lead_id,
        "recency": recency.round(1),
        "volume": volume_norm.round(1),
        "source_mix": mix_norm.round(1),
        "interest_depth": depth_norm.round(1),
        "cadence_consistency": cad_norm.round(1),
    })
    result["total"] = (result[["recency","volume","source_mix","interest_depth","cadence_consistency"]]
                       .mean(axis=1).round(1))
    return result

# 2) Engagement Velocity (30/90 day rate; z-score within peer group)
def engagement_velocity(supplements: pd.DataFrame, window_days: int = 30) -> pd.DataFrame:
    s = supplements.copy()
    s["published_at"] = pd.to_datetime(s["published_at"], errors="coerce")
    cutoff = pd.Timestamp.utcnow() - pd.Timedelta(days=window_days)
    s_recent = s[s["published_at"] >= cutoff]
    counts = s_recent.groupby("lead_id").size().rename("recent_n").astype(float)
    # z-score
    mu, sigma = counts.mean(), counts.std() if counts.std() not in (0, np.nan) else 1.0
    z = (counts - mu) / sigma
    return pd.DataFrame({"lead_id": counts.index, f"vel_{window_days}d": counts.values, f"z_{window_days}d": z.values})

# 3) Freshness Score
def freshness_score(supplements: pd.DataFrame) -> pd.DataFrame:
    df = supplements.copy()
    df["published_at"] = pd.to_datetime(df["published_at"], errors="coerce")
    df["age_days"] = (pd.Timestamp.utcnow() - df["published_at"]).dt.days
    # domain tiers (placeholder mapping—customize externally if you have a curated list)
    tier_map = {"moma.org": 1.0, "whitney.org": 1.0, "metmuseum.org": 1.0, "nytimes.com": 0.9}
    df["domain"] = df.get("domain") if "domain" in df.columns else df["url"].str.extract(r"https?://([^/]+)/")[0].str.lower()
    df["dom_w"] = df["domain"].map(tier_map).fillna(0.6)
    # decay
    df["decay"] = np.exp(-df["age_days"].fillna(999) / 365.0)
    df["fresh"] = 100 * df["dom_w"] * df["decay"]
    sc = df.groupby("lead_id")["fresh"].mean().rename("freshness_score").reset_index()
    return sc

# 4) Interest Vector & Similarity
def interest_vectors(leads: pd.DataFrame) -> Tuple[pd.DataFrame, np.ndarray]:
    tags = [" ".join(_to_list(x)) for x in leads["interests"]]
    vec = CountVectorizer(binary=True)
    X = vec.fit_transform(tags)
    return leads[["lead_id","full_name"]].reset_index(drop=True), X.toarray()

def similar_collectors(leads: pd.DataFrame, top_k: int = 5) -> Dict[str, List[Tuple[str, float]]]:
    meta, X = interest_vectors(leads)
    sim = cosine_similarity(X)
    out: Dict[str, List[Tuple[str, float]]] = {}
    for i, row in meta.iterrows():
        scores = list(enumerate(sim[i]))
        scores = sorted(((j, s) for j, s in scores if j != i), key=lambda x: x[1], reverse=True)[:top_k]
        out[row["lead_id"]] = [(meta.iloc[j]["lead_id"], float(score)) for j, score in scores]
    return out

# 5) Interest Momentum & Drift
def interest_momentum(supplements: pd.DataFrame, leads: pd.DataFrame) -> pd.DataFrame:
    # naive proxy: count of mentions per interest by quarter (if supplements has 'interests' or tags in notes)
    # If not available, we just mark growth in number of interests for a lead over time.
    l = leads.copy()
    l["_n_interests"] = l["interests"].apply(lambda x: len(_to_list(x)))
    # Placeholder: change vs. median count
    med = l["_n_interests"].median() if not np.isnan(l["_n_interests"].median()) else 0
    l["interest_momentum"] = (100 * (l["_n_interests"] - med) / (med or 1)).clip(-100, 100)
    return l[["lead_id","interest_momentum"]]

# 6) Influence Proxy
def influence_proxy(supplements: pd.DataFrame) -> pd.DataFrame:
    w = {"museum": 1.0, "press": 0.9, "official": 0.8, "gallery": 0.7, "blog": 0.5}
    df = supplements.copy()
    df["w"] = df["source_type"].str.lower().map(w).fillna(0.6)
    score = 100 * df.groupby("lead_id")["w"].mean()
    return score.rename("influence_proxy").reset_index()

# 7) Diversity Index (Shannon-like) across source_type and interests
def diversity_index(supplements: pd.DataFrame, leads: pd.DataFrame) -> pd.DataFrame:
    # source diversity
    src_counts = supplements.groupby(["lead_id","source_type"]).size().rename("n").reset_index()
    src_div = src_counts.groupby("lead_id").apply(
        lambda g: -np.sum((g["n"]/g["n"].sum()) * np.log2(g["n"]/g["n"].sum()))
    ).rename("src_diversity")
    # interest diversity
    L = leads.copy()
    L["n_interests"] = L["interests"].apply(_to_list).apply(len).replace(0, 1)
    max_n = L["n_interests"].max() or 1
    int_div = (L.set_index("lead_id")["n_interests"] / max_n).rename("int_diversity")
    out = pd.concat([src_div, int_div], axis=1).fillna(0.0).reset_index()
    out["diversity_index"] = (50*out["src_diversity"] + 50*out["int_diversity"]).round(1)
    return out[["lead_id","diversity_index","src_diversity","int_diversity"]]

# 8) QA Health
def qa_health(supplements: pd.DataFrame) -> pd.DataFrame:
    df = supplements.copy()
    # expects 'qa_flag' possibly null
    counts = df.groupby(["lead_id","qa_flag"]).size().rename("n").reset_index()
    pivot = counts.pivot_table(index="lead_id", columns="qa_flag", values="n", fill_value=0)
    pivot.columns = [f"qa_{str(c).lower()}" for c in pivot.columns]
    pivot = pivot.reset_index()
    pivot["qa_total"] = pivot.drop(columns=["lead_id"]).sum(axis=1)
    return pivot

# Utility: join multiple analytics into one frame
def build_analytics(leads: pd.DataFrame, evidence: pd.DataFrame, supplements: pd.DataFrame) -> pd.DataFrame:
    a = lead_score_decomposition(leads, evidence, supplements)
    v30 = engagement_velocity(supplements, 30)
    v90 = engagement_velocity(supplements, 90)
    fresh = freshness_score(supplements)
    infl = influence_proxy(supplements)
    div = diversity_index(supplements, leads)
    qa = qa_health(supplements)
    out = (leads[["lead_id","full_name","tier","city","country","lead_score"]]
           .merge(a, on="lead_id", how="left")
           .merge(v30, on="lead_id", how="left")
           .merge(v90, on="lead_id", how="left")
           .merge(fresh, on="lead_id", how="left")
           .merge(infl, on="lead_id", how="left")
           .merge(div, on="lead_id", how="left")
           .merge(qa, on="lead_id", how="left")
           )
    return out.fillna(0.0)
