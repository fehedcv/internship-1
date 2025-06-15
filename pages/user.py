import streamlit as st
import requests

API = "http://127.0.0.1:8000"

if "org" not in st.session_state:
    st.warning("Please log in first.")
    st.stop()

st.markdown("<h1 style='text-align: center;'>User Management</h1>", unsafe_allow_html=True)

with st.expander("Create User"):
    st.write("Create a new user with the following details:")
    with st.form("create_user"):
        name = st.text_input("Username")
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")
        organization_id = st.text_input("Organization id")
        if st.form_submit_button("Create user"):
                data = {
                    "name": name,
                    "email": email,
                    "password": password,
                    "organization_id": organization_id

                }
                try:
                    response = requests.post(f"{API}/users/create", json=data)

                    if response.status_code == 200:
                        st.success("User Created!")
                    else:
                        st.error("Something went wrong.")
                        st.warning(response.json())  # <- Call it as a function
                except Exception as e:
                    st.error(f"Error: {e}")



with st.expander("Users list"):
    if "page_user" not in st.session_state:
        st.session_state.page_user = 1

    userResponse = requests.get(f"{API}/users/{st.session_state.page}")
    data=userResponse.json()
    st.write(data)
     
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("⬅️ Previous", disabled=st.session_state.page <= 1):
            st.session_state.page -= 1
            st.rerun()
    with col3:
        if st.button("Next ➡️"):
            st.session_state.page += 1
            st.rerun()

with st.expander("Search User"):
    with st.form("search user"):
        org_name = st.text_input("User name")
        if st.form_submit_button("Search"):
            responseOrg = requests.get(f"{API}/users/search/{org_name}")
            dataOrg=responseOrg.json()
            st.write(dataOrg) 

with st.expander("Delete User"):
    with st.form("delete user"):
        user_id = st.text_input("User ID")
        if st.form_submit_button("Delete"):
            response = requests.delete(f"{API}/users/{user_id}")
            if response.status_code == 200:
                st.success("User Deleted")
            else:
                st.error(response.json())

if st.button("Go back"):
    st.switch_page("pages/Dashboard.py")