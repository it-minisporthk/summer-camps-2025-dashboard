import streamlit as st
import pandas as pd

st.set_page_config(page_title="Revenue Dashboard", layout="wide")

# ─────────────────────────────
# Authentication
# ─────────────────────────────
def check_password():
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False

    if st.session_state.authenticated:
        return True

    st.title("🔐 Login Required")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if (
            username == st.secrets["auth"]["username"]
            and password == st.secrets["auth"]["password"]
        ):
            st.session_state.authenticated = True
            st.rerun()
        else:
            st.error("Invalid username or password")

    return False


if not check_password():
    st.stop()

# ─────────────────────────────
# App title
# ─────────────────────────────
st.title("Interactive Revenue & Credit Dashboard")

# ─────────────────────────────
# Load & clean data
# ─────────────────────────────
@st.cache_data
def load_data():
    df = pd.read_csv("Code Playground - Analysis.csv")

    # Clean currency columns
    for col in ["Revenue", "Credit Awarded"]:
        df[col] = (
            df[col]
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
# Apply filters conditionally
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
total_credit = filtered_df["Credit Awarded"].sum()

col1, col2 = st.columns(2)

with col1:
    st.metric("Accumulated Revenue", f"${total_revenue:,.2f}")

with col2:
    st.metric("Accumulated Credit Awarded", f"${total_credit:,.2f}")

# ─────────────────────────────
# Data preview
# ─────────────────────────────
st.subheader("Filtered Data")
st.dataframe(filtered_df, use_container_width=True)
