import streamlit as st

# --- Page configuration ---
st.set_page_config(page_title="Login / Register", page_icon="🔑", layout="centered")

# --- Session state initialization ---
if "users" not in st.session_state:
    st.session_state.users = {}  # simple in-memory storage for users
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "username" not in st.session_state:
    st.session_state.username = ""

st.title(" Welcome")

#  If already logged in, show button to go to dashboard
if st.session_state.logged_in:
    st.success(f"Already logged in as **{st.session_state.username}**.")
    if st.button("Go to dashboard"):

        st.switch_page("pages/cyber.py")

    st.stop()

#  Tabs for Login / Register
tab_login, tab_register = st.tabs(["Login", "Register"])

#  LOGIN TAB
with tab_login:
    st.subheader("Login")
    login_username = st.text_input("Username", key="login_username")
    login_password = st.text_input("Password", type="password", key="login_password")

    if st.button("Log in", type="primary"):
        users = st.session_state.users
        if login_username in users and users[login_username] == login_password:
            st.session_state.logged_in = True
            st.session_state.username = login_username
            st.success(f"Welcome back, {login_username}! ")
            # In Home.py after login
            st.switch_page("pages/cyber.py")


        else:
            st.error("Invalid username or password.")

# ----- REGISTER TAB -----
with tab_register:
    st.subheader("Register")
    new_username = st.text_input("Choose a username")
    new_password = st.text_input("Choose a password", type="password")
    confirm_password = st.text_input("Confirm password", type="password")

    if st.button("Create account"):
        if not new_username or not new_password:
            st.warning("Please fill in all fields.")
        elif new_password != confirm_password:
            st.error("Passwords do not match.")
        elif new_username in st.session_state.users:
            st.error("Username already exists.")
        else:
            st.session_state.users[new_username] = new_password
            st.success("Account created! Go to the Login tab.")

