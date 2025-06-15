import streamlit as st
import requests

API = "http://127.0.0.1:8000"

if "org" not in st.session_state:
    st.warning("Please log in first.")
    st.stop()



st.markdown("<h1 style='text-align: center;'>Organization Management</h1>", unsafe_allow_html=True)

with st.expander("Create Organization"):
    st.write("Create a new organization with the following details:")
    with st.form("create org"):
        org_name = st.text_input("Organization name")
        if st.form_submit_button("Create Organization"):
                data = {
                    "name": org_name
                }
                try:
                    response = requests.post(f"{API}/orgs", json=data)

                    if response.status_code == 200:
                        st.success(f"{response.json()}")
                    else:
                        st.error("Something went wrong.")
                        st.warning(response.json())  # <- Call it as a function
                except Exception as e:
                    st.error(f"Error: {e}")


with st.expander("Organizations list"):

    if "page" not in st.session_state:
        st.session_state.page = 1

    userResponse = requests.get(f"{API}/orgs/{st.session_state.page}")
    data = userResponse.json()
    st.write(data)

    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("⬅️ Previous", key="prev", disabled=st.session_state.page <= 1):
            st.session_state.page -= 1
            st.rerun()
    with col3:
        if st.button("Next ➡️", key="next"):
            st.session_state.page += 1
            st.rerun()



with st.expander("Search organization"):
    with st.form("search org"):
        org_name = st.text_input("Organization name")
        if st.form_submit_button("Search"):
            responseOrg = requests.get(f"{API}/orgs/search/{org_name}")
            dataOrg=responseOrg.json()
            st.write(dataOrg) 

with st.expander("Delete Organization"):
    with st.form("delete organization"):
        user_id = st.text_input("Organization ID")
        if st.form_submit_button("Delete"):
            response = requests.delete(f"{API}/orgs/{user_id}")
            if response.status_code == 200:
                st.success("Organization Deleted")
            else:
                st.error(response.json())


if st.button("Go back"):
    st.switch_page("pages/Dashboard.py")