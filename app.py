import streamlit as st
import pandas as pd

st.set_page_config(page_title="Summer Camps Dashboard", layout="wide")

# Load data
@st.cache_data
def load_data():
    df = pd.read_csv("Summer Camps.csv")

    # Clean money columns
    df["Revenue"] = (
        df["Revenue"]
        .replace("[\$,]", "", regex=True)
        .astype(float)
    )

    df["Credit Awarded (S2/S3/S4)"] = (
        df["Credit Awarded (S2/S3/S4)"]
        .replace("[\$,]", "", regex=True)
        .astype(float)
    )

    # Clean utilization %
    df["Utilization %"] = (
        df["Utilization %"]
        .str.replace("%", "")
        .astype(float)
    )

    # Make sure numeric fields are numeric
    df["Quota"] = pd.to_numeric(df["Quota"], errors="coerce")
    df["Enrollments"] = pd.to_numeric(df["Enrollments"], errors="coerce")
    df["Waitlist"] = pd.to_numeric(df["Waitlist"], errors="coerce")

    return df

df = load_data()

# ------------------
# Sidebar Filters
# ------------------
st.sidebar.header("Filters")

venue_filter = st.sidebar.multiselect("Venue", sorted(df["Venue"].dropna().unique()), default=[])
day_filter = st.sidebar.multiselect("Day of Week (Week)", sorted(df["Week"].dropna().unique()), default=[])
ampm_filter = st.sidebar.multiselect("Time of Day (AM/PM)", sorted(df["AM/PM"].dropna().unique()), default=[])
start_time_filter = st.sidebar.multiselect("Start Time", sorted(df["Start Time"].dropna().unique()), default=[])

# 🔥 Waitlist toggle
show_waitlist_only = st.sidebar.toggle("Show only classes with waitlist > 0", value=False)

# ------------------
# Apply Filters
# ------------------
filtered_df = df.copy()

if venue_filter:
    filtered_df = filtered_df[filtered_df["Venue"].isin(venue_filter)]

if day_filter:
    filtered_df = filtered_df[filtered_df["Week"].isin(day_filter)]

if ampm_filter:
    filtered_df = filtered_df[filtered_df["AM/PM"].isin(ampm_filter)]

if start_time_filter:
    filtered_df = filtered_df[filtered_df["Start Time"].isin(start_time_filter)]

if show_waitlist_only:
    filtered_df = filtered_df[filtered_df["Waitlist"] > 0]

# ------------------
# KPI Row 1
# ------------------
total_revenue = filtered_df["Revenue"].sum()
total_credit = filtered_df["Credit Awarded (S2/S3/S4)"].sum()
avg_utilization = filtered_df["Utilization %"].mean() if len(filtered_df) > 0 else 0

col1, col2, col3 = st.columns(3)
col1.metric("💰 Revenue Generated", f"${total_revenue:,.2f}")
col2.metric("🎟️ Credit Awarded", f"${total_credit:,.2f}")
col3.metric("📊 Avg Utilization", f"{avg_utilization:.1f}%")

# ------------------
# KPI Row 2 (NEW)
# ------------------
total_quota = int(filtered_df["Quota"].sum())
total_enrollments = int(filtered_df["Enrollments"].sum())
total_waitlist = int(filtered_df["Waitlist"].sum())

col4, col5, col6 = st.columns(3)
col4.metric("📦 Total Quota", f"{total_quota:,}")
col5.metric("🧑‍🎓 Total Enrollments", f"{total_enrollments:,}")
col6.metric("⏳ Total Waitlist", f"{total_waitlist:,}")

# ------------------
# Table
# ------------------
st.subheader("Filtered Results")
st.dataframe(filtered_df, use_container_width=True)

# ------------------
# Download
# ------------------
st.download_button(
    "⬇️ Download Filtered CSV",
    data=filtered_df.to_csv(index=False),
    file_name="filtered_summer_camps.csv",
    mime="text/csv"
)
