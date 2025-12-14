import streamlit as st
import plotly.express as px
from app_db import get_table_from_csv
import pandas as pd
import sys
import os

# Compute absolute path to week 10 folder
week10_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..", "week 10"))
print("Week10 path:", week10_path, "Exists?", os.path.exists(week10_path))
sys.path.insert(0, week10_path)

# Import chatgpt_bot correctly (no .py extension)
from chatgpt_bot import ask_chatgpt

# Page config MUST be first

st.set_page_config(page_title="AI Analytics Dashboard", layout="wide")


# Require login
if "logged_in" not in st.session_state or not st.session_state.logged_in:
    st.error("You must be logged in to view this page.")
    st.stop()

st.title("AI Analytics Dashboard")


# Load CSV
# -------------------------------------------------
df = get_table_from_csv("datasets_metadata_1000")

# Normalize column names
df.columns = df.columns.str.strip().str.lower()

# Parse dates safely
df["last_updated"] = pd.to_datetime(df["last_updated"], errors="coerce")
df["created_at"] = pd.to_datetime(df["created_at"], errors="coerce")

# -------------------------------------------------
# Sidebar Filters (REAL columns)
# -------------------------------------------------
def safe_select(df, col, label):
    values = sorted(df[col].dropna().astype(str).unique())
    return st.sidebar.selectbox(label, ["All"] + values)

dataset_name = safe_select(df, "dataset_name", "Dataset")
category = safe_select(df, "category", "Category")
source = safe_select(df, "source", "Source")

# -------------------------------------------------
# Filter Data
# -------------------------------------------------
filtered = df.copy()

if dataset_name != "All":
    filtered = filtered[filtered["dataset_name"].astype(str) == dataset_name]

if category != "All":
    filtered = filtered[filtered["category"].astype(str) == category]

if source != "All":
    filtered = filtered[filtered["source"].astype(str) == source]

# -------------------------------------------------
# Display Table
# -------------------------------------------------
st.subheader(f"Showing {len(filtered)} record(s)")
st.dataframe(filtered, use_container_width=True)

if filtered.empty:
    st.warning("No data available for selected filters.")
    st.stop()

# -------------------------------------------------
# Charts
# -------------------------------------------------
st.header("AI Analytics Charts")

# 1️⃣ Datasets by Category
cat_count = (
    filtered.groupby("category")
    .size()
    .reset_index(name="count")
    .sort_values("count", ascending=False)
)

fig1 = px.bar(
    cat_count,
    x="category",
    y="count",
    title="Datasets by Category",
    color="category"
)
st.plotly_chart(fig1, use_container_width=True)

# 2️⃣ Dataset Sources Breakdown
src_count = (
    filtered.groupby("source")
    .size()
    .reset_index(name="count")
)

fig2 = px.pie(
    src_count,
    names="source",
    values="count",
    title="Dataset Sources"
)
st.plotly_chart(fig2, use_container_width=True)

# 3️⃣ Storage Size Over Time
size_time = (
    filtered.groupby("last_updated")["file_size_mb"]
    .sum()
    .reset_index()
    .sort_values("last_updated")
)

fig3 = px.line(
    size_time,
    x="last_updated",
    y="file_size_mb",
    title="Total Dataset Size Over Time (MB)",
    markers=True
)
st.plotly_chart(fig3, use_container_width=True)

st.header(" :) ChatGPT ")

# Initialize conversation in session state
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Input form at the bottom
with st.form(key="chat_form", clear_on_submit=True):
    user_input = st.text_input("Type your message here:")
    send_button = st.form_submit_button("Send")

    if send_button and user_input:
        try:
            answer = ask_chatgpt(user_input)
            st.session_state.chat_history.append({"user": user_input, "bot": answer})
        except Exception as e:
            st.error(f"API call failed: {e}")

# Display chat history (after form, so input stays at bottom)
for chat in st.session_state.chat_history:
    # User message
    st.markdown(
        f"""
        <div style="
            background-color: #DCF8C6;
            padding: 10px;
            border-radius: 10px;
            margin: 5px 0;
            max-width: 70%;
            float: right;
            clear: both;
        ">
            <strong>You:</strong> {chat['user']}
        </div>
        """,
        unsafe_allow_html=True
    )
    # ChatGPT message
    st.markdown(
        f"""
        <div style="
            background-color: #F1F0F0;
            padding: 10px;
            border-radius: 10px;
            margin: 5px 0;
            max-width: 70%;
            float: left;
            clear: both;
        ">
            <strong>ChatGPT:</strong> {chat['bot']}
        </div>
        """,
        unsafe_allow_html=True
    )

st.markdown("<div style='clear: both;'></div>", unsafe_allow_html=True)