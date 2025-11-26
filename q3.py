import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import re

def show_page():
    st.title(" Northern Cape: Health Data Cleaning (Q3)")
    st.markdown("Processing raw patient data for the mobile clinic initiative.")
    
    uploaded_file = st.file_uploader("Upload 'health_data.csv'", type="csv")
    
    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
        
        # --- 3a ---
        st.header("3a. Raw Data Auditing")
        st.markdown("""
        <div class='story-box'>
        <b>The Story:</b> Field nurses record data manually, leading to messy inputs (e.g., '120mmHg' vs '120').<br>
        <b>The Goal:</b> Identify non-numeric characters that will break our calculations.<br>
        <b>Business Value:</b> Ensures medical accuracy. A computer reads '120mmHg' as text, not a number, preventing risk scoring.
        </div>
        """, unsafe_allow_html=True)
        st.write("Preview of Raw Data:")
        st.dataframe(df.head())

        # --- 3b ---
        st.header("3b. Advanced Cleaning (Regex)")
        st.markdown("""
        <div class='story-box'>
        <b>The Story:</b> We need to strip away the 'noise' to get the 'signal'.<br>
        <b>The Solution:</b> We use Regex (Regular Expressions) to remove any character that isn't a digit (0-9).
        </div>
        """, unsafe_allow_html=True)
        
        # Regex Cleaning
        df['blood_pressure_clean'] = df['blood_pressure'].astype(str).apply(lambda x: re.sub(r'[^0-9.]', '', x))
        df['blood_pressure_clean'] = pd.to_numeric(df['blood_pressure_clean'], errors='coerce')
        
        col1, col2 = st.columns(2)
        col1.write("Before (Dirty):")
        col1.dataframe(df['blood_pressure'].head())
        col2.write("After (Clean):")
        col2.dataframe(df['blood_pressure_clean'].head())
        
        # --- 3c ---
        st.header("3c. Algorithm Risk Scoring")
        st.markdown("""
        <div class='story-box'>
        <b>The Story:</b> Doctors cannot manually review every patient. We need an automated triage system.<br>
        <b>The Logic:</b> 
        * High Risk: BMI > 30 AND Disease Score > 80
        * Medium Risk: BMI > 25 AND Disease Score > 60
        * Low Risk: Everyone else
        </div>
        """, unsafe_allow_html=True)
        
        def classify_risk(row):
            if row['BMI'] > 30 and row['disease_score'] > 80:
                return 'High'
            elif row['BMI'] > 25 and row['disease_score'] > 60:
                return 'Medium'
            else:
                return 'Low'
        
        df['risk_level'] = df.apply(classify_risk, axis=1)
        st.success("Risk Levels Calculated.")
        st.bar_chart(df['risk_level'].value_counts())

        # Save to session state for Q4
        st.session_state['health_clean'] = df
        st.divider()
        st.info(" Data processed and stored in memory. Please proceed to **Q4: SQL Registry**.")
        
    else:
        st.info(" Please upload `health_data.csv` to begin.")