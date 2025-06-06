import streamlit as st

st.set_page_config(page_title="Dashboard", layout="wide")

if "org" not in st.session_state:
    st.warning("Please log in first.")
    st.stop()

org = st.session_state["org"]

st.title(f"Welcome, {org['name']}!")
st.write("You are now logged in as:")
st.json(org)

if st.button("Logout"):
    del st.session_state["org"]
    st.switch_page("app.py")
