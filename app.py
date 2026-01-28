import streamlit as st
import pandas as pd

st.set_page_config(page_title="Revenue Dashboard", layout="wide")

st.title("Interactive Revenue Dashboard")

@st.cache_data
def load_data():
    df = pd.read_csv("Code Playground - Analysis.csv")

    # Clean revenue column
    df["Revenue"] = (
        df["Revenue"]
        .replace({",": "", "\\$": ""}, regex=True)
        .astype(float)
    )

    return df

df = load_data()

# ─────────────────────────────
# Sidebar filters (optional)
# ─────────────────────────────
st.sidebar.header("Filters (leave blank for all)")

venues = st.sidebar.multiselect(
    "Venue",
    options=sorted(df["Venue"].unique())
)

time_of_day = st.sidebar.multiselect(
    "Time of Day (AM / PM)",
    options=sorted(df["AM/PM"].unique())
)

start_times = st.sidebar.multiselect(
    "Start Time",
    options=sorted(df["Start Time"].unique())
)

# ─────────────────────────────
# Apply filters only if selected
# ─────────────────────────────
filtered_df = df.copy()

if venues:
    filtered_df = filtered_df[filtered_df["Venue"].isin(venues)]

if time_of_day:
    filtered_df = filtered_df[filtered_df["AM/PM"].isin(time_of_day)]

if start_times:
    filtered_df = filtered_df[filtered_df["Start Time"].isin(start_times)]

# ─────────────────────────────
# Metrics
# ─────────────────────────────
total_revenue = filtered_df["Revenue"].sum()

st.metric("Accumulated Revenue", f"${total_revenue:,.2f}")

# ─────────────────────────────
# Data preview
# ─────────────────────────────
st.subheader("Filtered Data")
st.dataframe(filtered_df, use_container_width=True)
