import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

def show_page():
    st.title(" ConnectSA: Community Data Analysis (Q1 & Q2)")
    st.markdown("Analyzing digital adoption trends in Cape Town, Durban, and Soweto.")

    uploaded_file = st.file_uploader("Upload 'customers.csv'", type="csv")
    
    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
        
        # --- DATA PROCESSING (Hidden from user view for cleanliness) ---
        # FIX for TypeError: Added default='Unknown'
        conditions = [
            (df['age'] < 25),
            (df['age'] >= 25) & (df['age'] < 60),
            (df['age'] >= 60)
        ]
        choices = ['Youth', 'Adult', 'Senior']
        df['age_group'] = np.select(conditions, choices, default='Unknown')
        
        df['subscription_date'] = pd.to_datetime(df['subscription_date'])
        df['year_joined'] = df['subscription_date'].dt.year
        df['month_joined'] = df['subscription_date'].dt.month_name()
        df['quarter_joined'] = df['subscription_date'].dt.to_period('Q').astype(str)
        
        # --- TABS FOR ANALYSIS ---
        tab_req, tab_extra = st.tabs([" Required Analysis (Q1 & Q2)", "🚀 Further Strategic Analysis (8 Extras)"])
        
        with tab_req:
            st.header("1. Core Project Requirements")
            
            # Q1a
            with st.container():
                st.subheader("Q1a: Data Structure Inspection")
                st.markdown("""
                <div class='story-box'>
                <b>The Story:</b> Before we can trust our insights, we must trust our data. We inspect the raw table to check for missing values or odd formats.<br>
                <b>Technical Goal:</b> Load CSV and display head/info.<br>
                <b>Business Value:</b> Prevents "garbage-in, garbage-out" decision making.
                </div>
                """, unsafe_allow_html=True)
                st.dataframe(df.head())
                st.write(df.describe())
                st.divider()

            # Q1b & Q1c
            with st.container():
                st.subheader("Q1b & Q1c: Youth Segment Identification")
                st.markdown("""
                <div class='story-box'>
                <b>The Story:</b> ConnectSA has a mandate to empower the youth. We need to isolate this demographic to measure our impact.<br>
                <b>Technical Goal:</b> Filter dataframe where <code>age < 25</code>.<br>
                <b>Business Value:</b> Creates a targeted mailing list for student-specific opportunities (e.g., coding bootcamps).
                </div>
                """, unsafe_allow_html=True)
                under_25 = df[df['age'] < 25]
                st.metric("Total Youth Customers", len(under_25))
                with st.expander("View Youth List"):
                    st.dataframe(under_25)
                st.divider()

            # Q2c
            with st.container():
                st.subheader("Q2c: Yearly Growth Trajectory")
                st.markdown("""
                <div class='story-box'>
                <b>The Story:</b> Are we growing or shrinking? Stakeholders need a clear visual of our momentum.<br>
                <b>Technical Goal:</b> Bar chart of count per <code>year_joined</code>.<br>
                <b>Business Value:</b> Validates marketing investment. A rising trend proves success; a flat trend signals a need for a pivot.
                </div>
                """, unsafe_allow_html=True)
                fig1, ax1 = plt.subplots(figsize=(10, 4))
                sns.countplot(x='year_joined', data=df, palette='viridis', ax=ax1)
                ax1.set_title("New Sign-ups per Year")
                st.pyplot(fig1)
                st.divider()

            # Q2d
            with st.container():
                st.subheader("Q2d: Demographic Composition")
                st.markdown("""
                <div class='story-box'>
                <b>The Story:</b> Who are we serving? We need to know the balance between students, workers, and retirees.<br>
                <b>Technical Goal:</b> Pie chart of <code>age_group</code>.<br>
                <b>Business Value:</b> Guides content strategy. If we have 40% Seniors, we need more accessibility features and digital basics courses.
                </div>
                """, unsafe_allow_html=True)
                fig2, ax2 = plt.subplots()
                df['age_group'].value_counts().plot.pie(autopct='%1.1f%%', ax=ax2, startangle=90, colors=['#ff9999','#66b3ff','#99ff99'])
                ax2.set_ylabel('')
                st.pyplot(fig2)

        with tab_extra:
            st.header("2. Strategic Deep-Dive (8 Additional Analyses)")
            
            # Analysis 1: City
            st.markdown("### 1. Geographic Footprint (By City)")
            st.markdown("""
            * **Story:** Where is the demand?
            * **Business Value:** Determines where to open physical support centers.
            """)
            st.bar_chart(df['city'].value_counts())
            st.divider()

            # Analysis 2: Seasonality
            st.markdown("### 2. Seasonal Pulse (By Month)")
            st.markdown("""
            * **Story:** When do people join?
            * **Business Value:** Optimizes ad spend. If Jan is high (Back to School), double the budget then.
            """)
            month_order = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
            fig_m, ax_m = plt.subplots(figsize=(10,4))
            sns.countplot(x='month_joined', data=df, order=month_order, palette='coolwarm', ax=ax_m)
            plt.xticks(rotation=45)
            st.pyplot(fig_m)
            st.divider()

            # Analysis 3: Tenure
            st.markdown("### 3. Loyalty Gauge (Tenure in Days)")
            st.markdown("""
            * **Story:** How long do customers stay?
            * **Business Value:** Identifies loyalists for "Anniversary Rewards" to reduce churn.
            """)
            current_date = pd.Timestamp.now()
            df['tenure_days'] = (current_date - df['subscription_date']).dt.days
            st.line_chart(df['tenure_days'])
            st.divider()

            # Analysis 4: Age vs City
            st.markdown("### 4. Regional Demographics (Age by City)")
            st.markdown("""
            * **Story:** Is Durban younger than Cape Town?
            * **Business Value:** Regional content curation. Push gaming in younger cities, finance news in older ones.
            """)
            city_age = df.groupby('city')['age'].mean().sort_values()
            st.bar_chart(city_age)
            st.divider()

            # Analysis 5: Weekday/Weekend
            st.markdown("### 5. Engagement Timing (Weekend vs Weekday)")
            st.markdown("""
            * **Story:** Do users sign up while working or relaxing?
            * **Business Value:** Dictates email campaign timing (e.g., Saturday mornings vs Monday 9am).
            """)
            df['is_weekend'] = df['subscription_date'].dt.dayofweek >= 5
            weekend_counts = df['is_weekend'].value_counts().rename({True: 'Weekend', False: 'Weekday'})
            st.bar_chart(weekend_counts)
            st.divider()

            # Analysis 6: Cumulative
            st.markdown("### 6. The 'Hockey Stick' (Cumulative Growth)")
            st.markdown("""
            * **Story:** What is our total load over time?
            * **Business Value:** Critical for IT scaling. Predicts when servers will crash.
            """)
            df_sorted = df.sort_values('subscription_date')
            df_sorted['cumulative_users'] = range(1, len(df_sorted)+1)
            st.line_chart(df_sorted.set_index('subscription_date')['cumulative_users'])
            st.divider()

            # Analysis 7: Country
            st.markdown("### 7. Data Integrity Audit (Country)")
            st.markdown("""
            * **Story:** Are we really only in South Africa?
            * **Business Value:** Detects fraud or data entry errors (e.g., seeing 'Peru' in a SA dataset).
            """)
            st.write(df['country'].value_counts())
            st.divider()

            # Analysis 8: Quarterly
            st.markdown("### 8. Financial Alignment (Quarterly)")
            st.markdown("""
            * **Story:** How do we look to the Board?
            * **Business Value:** Aligns metrics with standard Q1-Q4 financial reporting.
            """)
            st.bar_chart(df['quarter_joined'].value_counts().sort_index())

    else:
        st.info(" Please upload `customers.csv` to begin.")