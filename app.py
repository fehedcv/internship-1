#loading screen welcome to invoice managemnet system 5 second
#organization create , dashboard => userAll,RoleCreate,AssignRole,UserRole,
#side bar ee buttons oronnum click cheyuumbo oro forms aa form vachitte data handle chyde
#role and user manage cheyyanam 

import streamlit as st
import requests

API = "127.0.0.1:8000"


st.set_page_config(page_title="Org Login", layout="centered")

st.markdown("<h1 style='text-align: center;'>Login</h1>", unsafe_allow_html=True)


with st.form("user login"):
    user_id = st.text_input("Enter your User ID")
    if st.form_submit_button("Login"):
            response = requests.get(f"http://127.0.0.1:8000/users/login/{user_id}")
            if response.status_code == 200:
                st.session_state["org"] = response.json()
                st.success("Login successful!")
                st.switch_page("pages/Dashboard.py")  # This is the title of the file pages/dashboard.py
            else:
                st.error("Invalid User ID")












