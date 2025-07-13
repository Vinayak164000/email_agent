import streamlit as st
import requests

import os
BASE_URL = "https://email-agent-backend.onrender.com"  # FastAPI backend

st.set_page_config(
    page_title="Email Writing Agentic Application",
    page_icon="🌍",
    layout="centered",
    initial_sidebar_state="expanded",
)

# --------------------------
# 🔐 Authentication Logic
# --------------------------

def register_user(username, password):
    response = requests.post(f"{BASE_URL}/register", json={"username": username, "password": password})
    return response

def login_user(username, password):
    response = requests.post(
        f"{BASE_URL}/login",
        data={"username": username, "password": password},
        headers={"Content-Type": "application/x-www-form-urlencoded"}
    )
    return response

if "token" not in st.session_state:
    st.session_state.token = None

if st.session_state.token is None:
    st.title("🔐 Login / Register")

    auth_choice = st.radio("Choose action:", ["Login", "Register"])
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if auth_choice == "Login":
        if st.button("Login"):
            res = login_user(username, password)
            if res.status_code == 200:
                if res.status_code == 200:
                    st.success("Logged in successfully ✅")
                    st.session_state.token = res.json()["access_token"]
                    st.session_state.username = username  # Store username
                    st.rerun()

            else:
                st.error(res.json().get("detail", "Login failed."))

    else:  # Register
        if st.button("Register"):
            res = register_user(username, password)
            if res.status_code == 200:
                st.success("Registered successfully 🎉 You can now login.")
            else:
                st.error(res.json().get("detail", "Registration failed."))

    st.stop()  # Don't show the main app until logged in

# --------------------------
# 🤖 Main App After Login
# --------------------------

st.title("📧 Email Writing Agent")
st.write(f"👋 Welcome, **{st.session_state.username}**!")


# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

st.header("What email should I write for you?")

with st.form(key="query_form", clear_on_submit=True):
    user_input = st.text_input("User Input", placeholder="e.g. Write a leave application")
    submit_button = st.form_submit_button("Send")

if submit_button and user_input.strip():
    try:
        with st.spinner("Generating email..."):
            payload = {"question": user_input}
            headers = {"Authorization": f"Bearer {st.session_state.token}"}
            response = requests.post(f"{BASE_URL}/query", json=payload, headers=headers)

        if response.status_code == 200:
            answer = response.json().get("answer", "No answer returned.")
            markdown_content = f"""# 📩 AI-Written Email

---

{answer}

---
"""
            st.markdown(markdown_content)
        else:
            st.error("Bot failed to respond: " + response.text)

    except Exception as e:
        st.error(f"The response failed due to: {e}")

# --------------------------
# 🔚 Logout Button
# --------------------------
if st.button("Logout"):
    st.session_state.token = None
    st.rerun()
