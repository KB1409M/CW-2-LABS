import plotly.express as px
from app_db import get_table_from_csv
import streamlit as st
import sys
import os

# Compute absolute path to week 10 folder
week10_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..", "week 10"))
print("Week10 path:", week10_path, "Exists?", os.path.exists(week10_path))
sys.path.insert(0, week10_path)

# Import chatgpt_bot correctly (no .py extension)
from chatgpt_bot import ask_chatgpt

#  Block page access unless logged in
if "logged_in" not in st.session_state or st.session_state.logged_in is False:
    st.error(" You must be logged in to view this page.")
    st.stop()

st.set_page_config(page_title="Cyber Security Dashboard", layout="wide")
st.title("Cyber Security Incidents Dashboard")

df = get_table_from_csv("cyber_incidents_1000")

# Sidebar filters
st.sidebar.header("Filters")
incident_type = st.sidebar.selectbox("Incident Type", ["All"] + sorted(df["incident_type"].unique()))
severity = st.sidebar.selectbox("Severity", ["All"] + sorted(df["severity"].unique()))
status = st.sidebar.selectbox("Status", ["All"] + sorted(df["status"].unique()))

filtered = df.copy()
if incident_type != "All":
    filtered = filtered[filtered["incident_type"] == incident_type]
if severity != "All":
    filtered = filtered[filtered["severity"] == severity]
if status != "All":
    filtered = filtered[filtered["status"] == status]

st.subheader(f"Showing {len(filtered)} incident(s)")
st.dataframe(filtered, use_container_width=True)

# Charts
st.header("Incident Trends")

count_by_type = filtered.groupby("incident_type").size().reset_index(name="count")
fig = px.bar(count_by_type, x="incident_type", y="count", title="Incidents by Type", color="incident_type")
st.plotly_chart(fig, use_container_width=True)

severity_count = filtered.groupby("severity").size().reset_index(name="count")
fig2 = px.pie(severity_count, names="severity", values="count", title="Severity Breakdown")
st.plotly_chart(fig2, use_container_width=True)

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