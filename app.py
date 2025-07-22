# import streamlit as st
# from auth import show_login_form, show_signup_form
# from db import init_db

# if 'username' not in st.session_state:
#     st.session_state['username'] = None
# if 'logged_in' not in st.session_state:
#     st.session_state['logged_in'] = False

# if 'role' not in st.session_state:
#     st.session_state['role'] = None

# # import scraper

# # Initialize DB
# init_db()

# st.set_page_config("Smart Scraper", layout="centered")
# st.title("🕵️ Web Scraper with Login System")

# # Session state setup
# if "logged_in" not in st.session_state:
#     st.session_state.logged_in = False

# # Tabs: Login / Signup
# tabs = st.tabs(["🔓 Login", "📝 Sign Up"])

# with tabs[0]:
#     show_login_form()

# with tabs[1]:
#     show_signup_form()

# # If logged in, show user dashboard
# if st.session_state.get("logged_in"):

#     st.success(f"Welcome, {st.session_state['username']}!")

#     st.info(f"Your Role: **{st.session_state['role']}**")

#     # Role-specific dashboard (future extension)
#     if st.session_state["role"] == "admin":
#         st.markdown("🧑‍💼 Admin Tools: (User stats, logs, etc. coming soon...)")
#     else:
#         st.markdown("🧑‍💻 Proceed to enter URL and scrape...")
#         import scraper

#         st.header("🔗 Enter URL to Scrape")

#         url = st.text_input("Website URL")

#         if url and st.button("Analyze Page"):
#             content = scraper.detect_page_content(url)

#             if "error" in content:
#                 st.error(f"Error fetching URL: {content['error']}")
#             elif content.get("auth_required"):
#                 st.warning("This page seems to require login/authentication.")
#                 st.info("You may need to log in using Selenium later. (Feature coming!)")
#             else:
#                 st.success("Page fetched successfully!")
#                 st.markdown("## Select Data Types to Scrape")

#                 # Checkboxes for available data
#                 scrape_text = st.checkbox(f"Text ({len(content['text'])} items)", value=True)
#                 scrape_links = st.checkbox(f"Links ({len(content['links'])} items)")
#                 scrape_images = st.checkbox(f"Images ({len(content['images'])} items)")
#                 scrape_tables = st.checkbox(f"Tables ({len(content['tables'])} tables)")

#                 # Export format
#                 st.markdown("### Choose Output Format")
#                 output_format = st.selectbox("Format", ["CSV", "JSON", "Excel"])

#                 # Preview Selected Data
#                 st.markdown("### Preview Selected Data")

#                 if scrape_text:
#                     st.subheader("📝 Text")
#                     for t in content['text'][:5]:
#                         st.write(t)

#                 if scrape_links:
#                     st.subheader("🔗 Links")
#                     st.write(content['links'][:5])

#                 if scrape_images:
#                     st.subheader("🖼️ Images")
#                     for src in content['images'][:3]:
#                         st.image(src) if src.startswith("http") else st.write(src)

#                 if scrape_tables and content["tables"]:
#                     st.subheader("📊 First Table")
#                     st.dataframe(content['tables'][0])

#                 # Final scrape button
#                 if st.button("Scrape Selected"):
#                     st.success("✅ Data Scraped Successfully!")

#                     # Combine scraped data into exportable format
#                     output = {}

#                     if scrape_text:
#                         output['text'] = content['text']
#                     if scrape_links:
#                         output['links'] = content['links']
#                     if scrape_images:
#                         output['images'] = content['images']
#                     if scrape_tables:
#                         output['tables'] = [df.to_dict() for df in content['tables']]

#                     # Export as JSON for now (we’ll add other formats next)
#                     import json
#                     st.download_button("Download Scraped Data (JSON)",
#                                     json.dumps(output, indent=2),
#                                     file_name="scraped_data.json",
#                                     mime="application/json")

    

#     # Add logout
#     if st.button("Logout"):
#         st.session_state.logged_in = False
#         st.experimental_rerun()

# import streamlit as st
# from auth import show_login_form, show_signup_form
# from db import init_db

# init_db()

# # Default view
# if "view" not in st.session_state:
#     st.session_state["view"] = "auth"

# if st.session_state["view"] == "auth":
#     st.title("🔐 Web Scraper Login System")

#     option = st.radio("Choose an option", ["Login", "Signup"])
#     if option == "Login":
#         show_login_form()
#     else:
#         show_signup_form()

# elif st.session_state["view"] == "scrape":
#     st.title("🌐 Web Scraper Dashboard")
#     st.success(f"Welcome, {st.session_state['username']} ({st.session_state['role']})")

#     # Scraper form
#     url = st.text_input("Enter URL to scrape")
#     if st.button("Scrape"):
#         if url:
#             st.info(f"Scraping initiated for: {url}")
#             # You’ll add scraping logic here next
#         else:
#             st.warning("Please enter a valid URL.")

import streamlit as st
import requests
from bs4 import BeautifulSoup
import pandas as pd
import base64
from io import BytesIO

from auth import show_login_form, show_signup_form
from db import init_db

init_db()

# ---------- Utility: Download Helpers ----------
def get_download_link(data, filename, filetype):
    buffer = BytesIO()
    if filetype == 'csv':
        pd.DataFrame(data).to_csv(buffer, index=False)
    elif filetype == 'json':
        buffer.write(str(data).encode())
    buffer.seek(0)
    b64 = base64.b64encode(buffer.read()).decode()
    return f'<a href="data:file/{filetype};base64,{b64}" download="{filename}">Download {filetype.upper()}</a>'

# ---------- Scraper Logic ----------
def scrape_website(url, options):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        results = {}

        if "Text" in options:
            results['Text'] = [p.get_text() for p in soup.find_all('p')]
        if "Images" in options:
            results['Images'] = [img['src'] for img in soup.find_all('img') if img.get('src')]
        if "Links" in options:
            results['Links'] = [a['href'] for a in soup.find_all('a', href=True)]

        return results

    except Exception as e:
        st.error(f"Error occurred during scraping: {e}")
        return {}

# ---------- Session View Routing ----------
if "view" not in st.session_state:
    st.session_state["view"] = "auth"

# ---------- Auth View ----------
if st.session_state["view"] == "auth":
    st.title("🔐 Web Scraper Login System")

    option = st.radio("Choose an option", ["Login", "Signup"])
    if option == "Login":
        show_login_form()
    else:
        show_signup_form()

# ---------- Scraper Dashboard ----------
elif st.session_state["view"] == "scrape":
    st.title("🌐 Web Scraper Dashboard")
    st.success(f"Welcome, {st.session_state['username']} ({st.session_state['role']})")

    if st.button("Logout"):
        st.session_state.clear()
        st.experimental_rerun()

    url = st.text_input("Enter URL to scrape")
    options = st.multiselect("Select data to scrape", ["Text", "Images", "Links"])

    if st.button("Scrape"):
        if url and options:
            scraped_data = scrape_website(url, options)
            st.session_state["scraped_data"] = scraped_data
            st.success("Scraping completed!")
        elif not url:
            st.warning("Please enter a URL.")
        else:
            st.warning("Select at least one option to scrape.")

    if "scraped_data" in st.session_state:
        for key, value in st.session_state["scraped_data"].items():
            st.subheader(key)
            st.write(value[:10])  # show preview only

        col1, col2 = st.columns(2)
        with col1:
            st.markdown(get_download_link(st.session_state["scraped_data"], "scraped_data.csv", "csv"), unsafe_allow_html=True)
        with col2:
            st.markdown(get_download_link(st.session_state["scraped_data"], "scraped_data.json", "json"), unsafe_allow_html=True)

