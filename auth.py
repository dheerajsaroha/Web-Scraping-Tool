# import streamlit as st
# # from db import add_user, login_user, get_user_role
# from db import add_user, login_user, get_user_role, init_db
# init_db()

# # def show_login_form():
# #     st.subheader("🔐 Login")

# #     username = st.text_input("Username")
# #     password = st.text_input("Password", type="password")

# #     if st.button("Login"):
# #         result = login_user(username, password)
# #         if result:
# #             st.session_state["logged_in"] = True
# #             st.session_state["username"] = username
# #             st.session_state["role"] = get_user_role(username)
# #             st.success(f"Logged in as {username} ({st.session_state['role']})")
# #         else:
# #             st.error("Invalid username or password")

# # def show_signup_form():
# #     st.subheader("📝 Sign Up")

# #     username = st.text_input("New Username")
# #     password = st.text_input("New Password", type="password")
# #     role = st.selectbox("Select Role", ["user", "admin"])

# #     if st.button("Create Account"):
# #         try:
# #             add_user(username, password, role)
# #             st.success("User created successfully! You can now log in.")
# #         except:
# #             st.error("Username already exists.")
# def show_login_form():
#     st.subheader("Login")
#     username = st.text_input("Username", key="login_user")
#     password = st.text_input("Password", type="password", key="login_pass")
#     if st.button("Login"):
#         if username == "admin" and password == "admin":
#             st.session_state["logged_in"] = True
#             st.success("Logged in as admin!")
#         elif username == "user" and password == "user":
#             st.session_state["logged_in"] = True
#             st.success("Logged in as user!")
#         else:
#             st.error("Invalid credentials")

# def show_signup_form():
#     st.subheader("Signup")
#     username = st.text_input("New Username", key="signup_user")
#     password = st.text_input("New Password", type="password", key="signup_pass")
#     if st.button("Create Account"):
#         st.success(f"Account created for {username}!")
#         st.session_state["logged_in"] = True


# import streamlit as st
# from db import add_user, login_user, get_user_role, init_db
# import time

# # Best placed in app.py, not here:
# # init_db()

# def auto_dismiss_message(message, message_type="success", delay=2):
#     if message_type == "success":
#         st.success(message)
#     else:
#         st.error(message)
#     time.sleep(delay)
#     st.rerun()

# def show_login_form():
#     st.subheader("🔐 Login")

#     username = st.text_input("Username", key="login_user")
#     password = st.text_input("Password", type="password", key="login_pass")

#     if st.button("Login"):
#         result = login_user(username, password)
#         if result:
#             st.session_state["logged_in"] = True
#             st.session_state["username"] = username
#             st.session_state["role"] = get_user_role(username)
#             st.success(f"Logged in as {username} ({st.session_state['role']})")
#         else:
#             st.error("Invalid credentials")

# def show_signup_form():
#     st.subheader("📝 Sign Up")

#     username = st.text_input("New Username", key="signup_user")
#     password = st.text_input("New Password", type="password", key="signup_pass")
#     role = st.selectbox("Select Role", ["user", "admin"])

#     if st.button("Create Account"):
#         try:
#             add_user(username, password, role)
#             st.success(f"Account created for {username}!")
#             st.session_state["logged_in"] = True
#             st.session_state["username"] = username
#             st.session_state["role"] = role
#         except:
#             st.error("Username already exists.")

import streamlit as st
from db import add_user, login_user, get_user_role, init_db

init_db()

def show_login_form():
    st.subheader("🔐 Login")
    username = st.text_input("Username", key="login_user")
    password = st.text_input("Password", type="password", key="login_pass")

    if st.button("Login"):
        result = login_user(username, password)
        if result:
            st.session_state["logged_in"] = True
            st.session_state["username"] = username
            st.session_state["role"] = get_user_role(username)
            st.session_state["view"] = "scrape"
            st.rerun()  # 🚀 force switch to scrape view
        else:
            st.error("Invalid username or password")

def show_signup_form():
    st.subheader("📝 Sign Up")
    username = st.text_input("New Username", key="signup_user")
    password = st.text_input("New Password", type="password", key="signup_pass")
    role = st.selectbox("Role", ["user", "admin"])

    if st.button("Create Account"):
        try:
            add_user(username, password, role)
            st.session_state["logged_in"] = True
            st.session_state["username"] = username
            st.session_state["role"] = role
            st.session_state["view"] = "scrape"
            st.rerun()  # 🚀 immediately show scraper page
        except:
            st.error("Username already exists.")

