#loading screen welcome to invoice managemnet system 5 second
#organization create , dashboard => userAll,RoleCreate,AssignRole,UserRole,
#side bar ee buttons oronnum click cheyuumbo oro forms aa form vachitte data handle chyde
#role and user manage cheyyanam 

import streamlit as st
import requests

API = "127.0.0.1:8000"

st.header("Create organization")

with st.form("orgFrom"):
    name = st.text_input("Organization name")
    if st.form_submit_button():
        response = requests.post(f"http://{API}/orgs/", json={"name": name})
        if response.status_code == 200:
            st.success("Organization created successfully")
        else:
            st.error("Failed to create organization")

st.divider()

if 'page' not in st.session_state:
    st.session_state.page = 1
if 'show_orgs' not in st.session_state:
    st.session_state.show_orgs = False

if st.button("Get organizations"):
    st.session_state.show_orgs = True
    st.session_state.page=1

if st.session_state.show_orgs:
    col1, col2 = st.columns([1, 1])

    with col1:
        if st.button("⬅️ Previous") and st.session_state.page > 1:
            st.session_state.page -= 1

    with col2:
        if st.button("➡️ Next"):
            st.session_state.page += 1

    
    response = requests.get(f"http://{API}/orgs/{st.session_state.page}")
    organizations = response.json()
    st.write(f"### Page {st.session_state.page}")
    for org in organizations:
        st.write(f"- {org}")
st.divider()

st.header("Search organization by name")
search_org = st.text_input("Enter organization name")
if st.button("Search"):
    response = requests.get(f"http://{API}/orgs/?name={search_org}")
    if response.status_code == 200:
        orgs = response.json()
        for org in orgs:
            st.write(org["name"])
        else:
            st.error("No organization found")
    else:
        st.error("Failed to search organization")








