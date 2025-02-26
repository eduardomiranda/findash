import streamlit as st


# Function to show the login popup
def show_login_popup():
    with st.form(key='login_form'):
        st.write("Please log in")
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        submit_button = st.form_submit_button("Login")

        if submit_button:
            if username == st.secrets['authentication'].get("username", '') and password == st.secrets['authentication'].get("password", ''):  # Replace with your authentication logic
                st.session_state.logged_in = True
                # st.session_state.username = username
                st.success("Logged in successfully!")
                st.rerun() 
            else:
                st.error("Invalid username or password")



def streamit_login():

    if st.secrets['environment'].get("location", '') == "local":
        st.session_state.logged_in = True
    else:
        if 'logged_in' not in st.session_state:
            st.session_state.logged_in = False

        if not st.session_state.logged_in:
            show_login_popup()
