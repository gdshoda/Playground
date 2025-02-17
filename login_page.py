import streamlit as st
import pyrebase
import requests

# Retrieve Firebase config from Streamlit secrets
firebase_config = {
    "apiKey": st.secrets["firebase"]["api_key"],
    "authDomain": st.secrets["firebase"]["auth_domain"],
    "projectId": st.secrets["firebase"]["project_id"],
    "storageBucket": st.secrets["firebase"]["storage_bucket"],
    "messagingSenderId": st.secrets["firebase"]["messaging_sender_id"],
    "appId": st.secrets["firebase"]["app_id"],
    "databaseURL": st.secrets["firebase"]["database_url"]
}

# Initialize Firebase
firebase = pyrebase.initialize_app(firebase_config)
auth = firebase.auth()

#creating a login header
login_header = st.header("Sign In")

# Streamlit UI for login
email = st.text_input("Email")
password = st.text_input("Password", type="password")

if st.button("Login"):
    try:
        # Sign in the user
        user = auth.sign_in_with_email_and_password(email, password)
        st.success("Logged in successfully!")
        # You can store the user's session token (if needed)
        st.write(user)

    except requests.exceptions.HTTPError as e:
        error_message = str(e)
        if "400" in error_message:
            st.write("Invalid Login Credentials!")
        # Handle the specific FirebaseError
        #st.write(e)

# creating a sign up header
signup_header = st.header("New to Job Search App?")
signup_subheader = st.subheader("Enter your username and password above and hit the Sign Up button below to create an account!")

if st.button("Sign Up"):
    try:
        auth.create_user_with_email_and_password(email, password)
        st.success("Account created successfully!")
    except Exception as e:
        st.error("Sign-up failed: " + str(e))

#creating a demo header
demo_header = st.header("Just curious about the app and its functions? Enter Demo mode!")

if st.button("Demo Mode"):
    st.write("Demo functionality coming soon!")


