import pandas as pd
import streamlit as st

def Referrals(df):
    # Convert "Referral Date (Date received)" to datetime and count valid dates
    df['Referral Date (Date received)'] = pd.to_datetime(df['Referral Date (Date received)'], errors='coerce')
    valid_referral_count = df['Referral Date (Date received)'].notna().sum()
    # Display the count in Streamlit
    st.markdown("### ")
    st.write(f"### Total Number of Referrals: {valid_referral_count}")
