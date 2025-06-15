import streamlit as st
import requests


API = "http://127.0.0.1:8000"

st.set_page_config(page_title="Dashboard", layout="wide")

if "org" not in st.session_state:
    st.warning("Please log in first.")
    st.stop()




org = st.session_state["org"]

st.title(f"Welcome, {org['name']}!")
st.write("You are now logged in as:")
st.json(org)

if st.button("User Management"):
    st.switch_page("pages/user.py")

if st.button("Organization Management"):
    st.switch_page("pages/orgs.py")


if st.button("Logout"):
    del st.session_state["org"]
    st.switch_page("app.py")
