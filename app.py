#loading screen welcome to invoice managemnet system 5 second
#organization create , dashboard => userAll,RoleCreate,AssignRole,UserRole,
#side bar ee buttons oronnum click cheyuumbo oro forms aa form vachitte data handle chyde
#role and user manage cheyyanam 

import streamlit as st
import requests

API = "127.0.0.1:8000"


st.set_page_config(page_title="Org Login", layout="centered")

st.title("Login as Organization")

org_id = st.text_input("Enter your Organization ID")

if st.button("Login"):
        response = requests.get(f"http://127.0.0.1:8000/orgs/login/{org_id}")
        if response.status_code == 200:
            st.session_state["org"] = response.json()
            st.success("Login successful!")
            st.switch_page("pages/Dashboard.py")  # This is the title of the file pages/dashboard.py
        else:
            st.error("Invalid Organization ID")



st.header("Create organization")

with st.form("orgFrom"):
    name = st.text_input("Organization name")
    if st.form_submit_button():
        response = requests.post(f"http://{API}/orgs/", json={"name": name})
        if response.status_code == 200:
            st.success("Organization created successfully")
        else:
            st.error("Failed to create organization")








