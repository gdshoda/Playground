import streamlit as st
import pandas as pd
from bs4 import BeautifulSoup
import requests
from collections import Counter
import pyrebase

# Retrieve Firebase config from Streamlit secrets
firebase_config = {
    "apiKey": st.secrets["firebase"]["api_key"],
    "authDomain": st.secrets["firebase"]["auth_domain"],
    "databaseURL": st.secrets["firebase"]["database_url"],
    "projectId": st.secrets["firebase"]["project_id"],
    "storageBucket": st.secrets["firebase"]["storage_bucket"],
    "messagingSenderId": st.secrets["firebase"]["messaging_sender_id"],
    "appId": st.secrets["firebase"]["app_id"]
}

# Initialize Firebase
firebase = pyrebase.initialize_app(firebase_config)
auth = firebase.auth()

# Streamlit UI for login
email = st.text_input("Email")
password = st.text_input("Password", type="password")


url = st.text_input("Job Link")
if url:
    response = requests.get(url)

    soup = BeautifulSoup(response.text, "html.parser")
    soup.title.text

    # Extract job title
    # headers = soup.find_all("h1")
    # for header in headers:
    #     if header.text:
    #         header.text


    # subheaders = soup.find_all("h2")
    # for sub in subheaders:
    #     if sub.text:
    #         sub.text

    # Step 2: Extract structured data
    data = {
        "title": soup.title.string if soup.title else None,
        "meta": {meta["name"]: meta["content"] for meta in soup.find_all("meta", attrs={"name": True, "content": True})},
        "headings": {f"h{i}": [h.text.strip() for h in soup.find_all(f"h{i}")] for i in range(1, 7)},
        "paragraphs": [p.text.strip() for p in soup.find_all("p") if p.text.strip()],
        "links": [{"text": a.text.strip(), "href": a["href"]} for a in soup.find_all("a", href=True)],
        "tables": [
            [[td.get_text(strip=True) for td in row.find_all(["td", "th"])] for row in table.find_all("tr")]
            for table in soup.find_all("table")
        ],
        "classes": {
            class_name: [element.get_text(strip=True) for element in soup.find_all(class_=class_name)]
            for class_name in set(cls for tag in soup.find_all(class_=True) for cls in tag["class"])
        }
    }

    data

    # # Extract all class names from the page
    # data = {}
    # classes = set()

    # tags = soup.find_all(class_=True)

    # for tag in tags:  # Finds elements with a class attribute
    #     classes.update(tag["class"])  # Add all class names to the set
    
    # classes

    # for element in tags:
    #     class_name = " ".join(element["class"])  # Get class names as a single string
    #     content = element.get_text(strip=True)   # Get text without extra spaces
        
    #     if class_name in data:
    #         data[class_name].append(content)  # Append content if class already exists
    #     else:
    #         data[class_name] = [content]  # Initialize list with first content
    
    # for class_name, contents in data.items():
    #     st.write(f"Class: {class_name}")
    #     for content in contents:
    #         st.write(f"  - {content}")