import streamlit as st
import plotly.express as px
from app_db import get_table_from_csv
import sys
import os

# Compute absolute path to week 10 folder
week10_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..", "week 10"))
print("Week10 path:", week10_path, "Exists?", os.path.exists(week10_path))
sys.path.insert(0, week10_path)

# Import chatgpt_bot correctly (no .py extension)
from chatgpt_bot import ask_chatgpt


#  Require login
if "logged_in" not in st.session_state or st.session_state.logged_in is False:
    st.error(" You must be logged in to view this page.")
    st.stop()

st.set_page_config(page_title="IT Tickets Dashboard", layout="wide")
st.title(" IT Tickets Dashboard")

# Load CSV
df = get_table_from_csv("it_tickets_1000")



# -----------------------------
# Sidebar Filters (dynamic)
# -----------------------------
def safe_select(df, col_name, label):
    if col_name in df.columns:
        return st.sidebar.selectbox(label, ["All"] + sorted(df[col_name].astype(str).unique()))
    else:
        st.sidebar.warning(f"Column '{col_name}' not found in CSV, skipping filter.")
        return "All"

# Example columns to filter — adjust if your CSV has different names
priority_filter = safe_select(df, "priority", "Priority")
status_filter = safe_select(df, "status", "Status")
assigned_filter = safe_select(df, "assigned_to", "Assigned To")

# -----------------------------
# Filter the DataFrame
# -----------------------------
filtered = df.copy()
if "priority" in df.columns and priority_filter != "All":
    filtered = filtered[filtered["priority"] == priority_filter]
if "status" in df.columns and status_filter != "All":
    filtered = filtered[filtered["status"] == status_filter]
if "assigned_to" in df.columns and assigned_filter != "All":
    filtered = filtered[filtered["assigned_to"] == assigned_filter]

# -----------------------------
# Display Table
# -----------------------------
st.subheader(f"Showing {len(filtered)} ticket(s)")
st.dataframe(filtered, use_container_width=True)

# -----------------------------
# Charts
# -----------------------------
st.header("IT Tickets Overview")

# 1️⃣ Tickets by Priority
if "priority" in filtered.columns:
    count_by_priority = filtered.groupby("priority").size().reset_index(name="count")
    fig1 = px.bar(count_by_priority, x="priority", y="count", title="Tickets by Priority", color="priority")
    st.plotly_chart(fig1, use_container_width=True)

# 2️⃣ Tickets by Status
if "status" in filtered.columns:
    count_by_status = filtered.groupby("status").size().reset_index(name="count")
    fig2 = px.pie(count_by_status, names="status", values="count", title="Status Breakdown")
    st.plotly_chart(fig2, use_container_width=True)

# 3️⃣ Tickets by Assigned To
if "assigned_to" in filtered.columns:
    count_by_assigned = filtered.groupby("assigned_to").size().reset_index(name="count")
    fig3 = px.bar(count_by_assigned, x="assigned_to", y="count", title="Tickets by Assigned To", color="assigned_to")
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




