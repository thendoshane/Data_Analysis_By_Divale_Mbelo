import streamlit as st
import pandas as pd
import sqlite3

def show_page():
    st.title(" Health Risk Registry (SQL) (Q4)")
    st.markdown("Building a scalable patient database.")
    
    if 'health_clean' in st.session_state:
        df = st.session_state['health_clean']
        
        # --- 4a Setup ---
        st.header("4a. Database Architecture")
        st.markdown("""
        <div class='story-box'>
        <b>Why use a Database (SQLite)?</b><br>
        Excel/CSV files are risky. They can be deleted, corrupted, or duplicated. A Database (SQL) provides:
        1.  <b>Security:</b> Controlled access.
        2.  <b>Scalability:</b> Can handle millions of patients, unlike Excel.
        3.  <b>Querying:</b> We can ask complex questions (e.g., "Show me all Critical females") instantly.
        </div>
        """, unsafe_allow_html=True)
        
        # Create In-Memory DB
        conn = sqlite3.connect(':memory:')
        df.to_sql('patients', conn, index=False, if_exists='replace')
        st.success("Connection Established: `health_registry.db` (In-Memory)")
        
        # --- 4b ---
        st.subheader("4b. SQL Analysis: Risk by Gender")
        st.markdown("**Goal:** To check if certain risks are gender-specific.")
        query1 = """
        SELECT sex, risk_level, COUNT(*) as count 
        FROM patients 
        GROUP BY sex, risk_level 
        ORDER BY sex
        """
        st.code(query1, language='sql')
        st.dataframe(pd.read_sql(query1, conn))
        st.divider()
        
        # --- 4d ---
        st.subheader("4d. Automated Status Classification")
        st.markdown("**Goal:** To generate a final 'Critical' list for immediate doctor intervention.")
        query3 = """
        SELECT patient_id, age, BMI, blood_pressure_clean, risk_level,
        CASE 
            WHEN disease_score > 80 AND risk_level = 'High' THEN 'Critical' 
            ELSE 'Stable' 
        END as status 
        FROM patients
        WHERE status = 'Critical'
        """
        st.code(query3, language='sql')
        df_critical = pd.read_sql(query3, conn)
        
        if not df_critical.empty:
            st.error(f" ALERT: {len(df_critical)} Critical Patients Identified!")
            st.dataframe(df_critical)
        else:
            st.success("No Critical Patients found based on current criteria.")
            
        # --- EXTRA SQL FEATURES ---
        st.header(" Advanced SQL Features (Extra)")
        
        st.markdown("### 1. Dynamic Patient Search")
        st.markdown("Doctors need to find patients quickly. SQL `WHERE` clauses make this instant.")
        
        search_id = st.text_input("Enter Patient ID (e.g., P001):")
        if search_id:
            query_search = f"SELECT * FROM patients WHERE patient_id LIKE '%{search_id}%'"
            st.dataframe(pd.read_sql(query_search, conn))
            
        st.markdown("### 2. High-Risk Filter")
        score_threshold = st.slider("Filter patients with Disease Score above:", 0, 100, 80)
        query_filter = f"SELECT * FROM patients WHERE disease_score > {score_threshold} ORDER BY disease_score DESC"
        st.dataframe(pd.read_sql(query_filter, conn))
        
    else:
        st.error(" No Data Found. Please complete **Q3: Health Cleaning** first to generate the clean dataset.")