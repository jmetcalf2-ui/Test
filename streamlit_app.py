
import streamlit as st
import pandas as pd

# -----------------------------
# Page config
# -----------------------------
st.set_page_config(page_title="Collector Intelligence Dashboard", layout="wide")

# -----------------------------
# Global styling (all-white, black text, Helvetica)
# -----------------------------
st.markdown(
    """
    <style>
    html, body, [class^="css"], .block-container {
        background-color: white !important;
        color: black !important;
        font-family: Helvetica, Arial, sans-serif !important;
    }
    /* Ensure all headings are clearly visible and larger */
    h1 { font-size: 2.2rem !important; line-height: 1.2; margin: 1.25rem 0 0.75rem 0; font-weight: 700; }
    h2 { font-size: 1.6rem !important; line-height: 1.3; margin: 1rem 0 0.5rem 0; font-weight: 650; }
    h3 { font-size: 1.25rem !important; line-height: 1.35; margin: 0.75rem 0 0.5rem 0; font-weight: 600; }
    h4, h5, h6 { color: black !important; font-weight: 600; }

    /* Streamlit widgets/text labels */
    .stMarkdown, .stText, .stCaption, label, .st-cp, .st-ag, .st-dx { color: black !important; }

    /* Dataframe header / cell text */
    .stDataFrame thead tr th { color: black !important; }
    .stDataFrame tbody tr td { color: black !important; }

    /* Remove excessive padding and keep layout airy */
    .block-container { padding-top: 2rem; padding-bottom: 2rem; }

    /* Links stay black (optional) */
    a, a:visited { color: black !important; text-decoration: underline; }
    </style>
    """ ,
    unsafe_allow_html=True,
)

# -----------------------------
# Demo data (replace with Supabase fetch)
# -----------------------------
@st.cache_data
def load_demo_data():
    return pd.DataFrame({
        "Collector": ["Alice", "Bob", "Charlie", "Dana"],
        "Location": ["New York", "London", "Paris", "Los Angeles"],
        "Tier": ["A", "B", "C", "A"],
        "Interest Score": [92, 75, 63, 88]
    })

data = load_demo_data()

# -----------------------------
# Sidebar Navigation
# -----------------------------
st.sidebar.header("Navigation")
page = st.sidebar.radio(
    "Go to",
    ["Overview", "Filters", "Detailed View", "Analytics"],
    index=0,
    help="Use this to move between sections"
)

# Optional: global quick filters in sidebar
with st.sidebar.expander("Quick Filters", expanded=False):
    tier_filter = st.multiselect("Tier", options=sorted(data["Tier"].unique().tolist()), default=[])
    location_filter = st.multiselect("Location", options=sorted(data["Location"].unique().tolist()), default=[])

filtered = data.copy()
if tier_filter:
    filtered = filtered[filtered["Tier"].isin(tier_filter)]
if location_filter:
    filtered = filtered[filtered["Location"].isin(location_filter)]

# -----------------------------
# Page Content
# -----------------------------
st.title("Collector Intelligence Dashboard")
st.write("A clean, minimalist interface to explore collector data.")

if page == "Overview":
    st.header("Overview")
    st.write("This section shows a summary of collectors and their interest scores.")
    st.dataframe(filtered, use_container_width=True)

elif page == "Filters":
    st.header("Filters")
    st.write("Filter the dataset by Tier using the selector below.")

    selected_tier = st.selectbox(
        "Filter by Tier",
        options=["All"] + sorted(data["Tier"].unique().tolist())
    )

    df = data.copy()
    if selected_tier != "All":
        df = df[df["Tier"] == selected_tier]

    st.subheader("Filtered Table")
    st.dataframe(df, use_container_width=True)

elif page == "Detailed View":
    st.header("Detailed View")
    st.write("Explore the selected subset of collectors from the sidebar’s quick filters.")

    st.subheader("Records")
    st.dataframe(filtered, use_container_width=True)

    if not filtered.empty:
        st.subheader("Row Inspector")
        row = st.selectbox("Choose a collector", options=filtered["Collector"].tolist())
        row_data = filtered[filtered["Collector"] == row].iloc[0]
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Collector", row_data["Collector"])
        col2.metric("Location", row_data["Location"])
        col3.metric("Tier", row_data["Tier"])
        col4.metric("Interest Score", int(row_data["Interest Score"]))
    else:
        st.info("No rows match the current filters.")

elif page == "Analytics":
    st.header("Analytics")
    st.write("Basic statistics and insights for the currently filtered dataset.")

    if not filtered.empty:
        avg_score = round(filtered["Interest Score"].mean(), 1)
        count = len(filtered)
        a_count = int((filtered["Tier"] == "A").sum())

        c1, c2, c3 = st.columns(3)
        c1.metric(label="Average Interest Score", value=avg_score)
        c2.metric(label="Number of Collectors", value=count)
        c3.metric(label="Tier A Count", value=a_count)

        st.subheader("Tier Breakdown")
        st.write(
            filtered.groupby("Tier").size().rename("Count").reset_index()
        )
    else:
        st.info("No data available under current filters.")
