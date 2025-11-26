import streamlit as st
import pandas as pd
import q1_q2
import q3
import q4

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="Eduvos Data Analysis Project",
    page_icon="",
    layout="wide",
    initial_sidebar_state="collapsed" # Hiding sidebar to enforce Top Nav
)

# --- SESSION STATE INITIALIZATION ---
if 'current_page' not in st.session_state:
    st.session_state['current_page'] = "Home"

# --- CUSTOM CSS FOR TOP NAV ---
st.markdown("""
    <style>
    .stButton button {
        width: 100%;
        border-radius: 5px;
        height: 3em;
        font-weight: bold;
    }
    .main-header {
        font-size: 2.5rem;
        color: #2c3e50;
        text-align: center;
        margin-bottom: 1rem;
    }
    .sub-header {
        font-size: 1.5rem;
        color: #7f8c8d;
        text-align: center;
        margin-bottom: 2rem;
    }
    .story-box {
        background-color: #f0f2f6;
        padding: 20px;
        border-radius: 10px;
        border-left: 5px solid #3498db;
        margin-bottom: 20px;
    }
    </style>
""", unsafe_allow_html=True)

# --- TOP NAVIGATION BAR ---
col1, col2, col3, col4 = st.columns(4)

with col1:
    if st.button(" Home & Overview"):
        st.session_state['current_page'] = "Home"
with col2:
    if st.button(" Q1 & Q2: Community"):
        st.session_state['current_page'] = "Q1_Q2"
with col3:
    if st.button(" Q3: Health Cleaning"):
        st.session_state['current_page'] = "Q3"
with col4:
    if st.button(" Q4: SQL Registry"):
        st.session_state['current_page'] = "Q4"

st.markdown("---") # Divider between nav and content

# --- PAGE ROUTING ---
if st.session_state['current_page'] == "Home":
    st.markdown("<div class='main-header'> Data Analysis with Python: Final Project</div>", unsafe_allow_html=True)
    st.markdown("<div class='sub-header'>Faculty of Information Technology | Module: ITAYA0-44</div>", unsafe_allow_html=True)

    st.markdown("""
    ###  Project Context & Objectives
    
    This project demonstrates the end-to-end data analysis lifecycle for two distinct clients: **ConnectSA** (a non-profit) and the **Northern Cape Department of Health**.
    
    ####  Client 1: ConnectSA (Community Analysis)
    * **The Problem:** ConnectSA provides digital literacy to underserved communities but lacks insight into *who* their customers are and *how* they are growing.
    * **Our Solution:** We analyze `customers.csv` to segment the audience by Age and Location, tracking growth over time to optimize resource allocation.
    
    ####  Client 2: Northern Cape Health (Health Risks)
    * **The Problem:** Rural mobile clinics are collecting patient data, but it is "dirty" (inconsistent formatting) and currently stored in flat CSV files, making it hard to identify high-risk patients.
    * **Our Solution:** 1.  **Clean** the dirty data using Regex (Regular Expressions).
        2.  **Classify** patients into risk categories (Low, Medium, High).
        3.  **Migrate** the data into a **SQLite Database** to build a robust Health Registry for doctors.
    
    ####  Technical Competencies Demonstrated
    * **Data Wrangling:** Pandas & NumPy (Filtering, Grouping, Transformation).
    * **Visualization:** Matplotlib & Seaborn (Storytelling with data).
    * **Database Management:** SQLite3 (SQL Queries, Relational Data).
    * **Web Development:** Streamlit (Interactive Dashboarding).
    """)

    st.info(" **Navigation:** Click the buttons at the top of the page to move between the different project sections.")

elif st.session_state['current_page'] == "Q1_Q2":
    q1_q2.show_page()

elif st.session_state['current_page'] == "Q3":
    q3.show_page()

elif st.session_state['current_page'] == "Q4":
    q4.show_page()