import pandas as pd
import streamlit as st

def Referrals(df):
    # Ensure the date column is in datetime format
    df['Referral Date (Date received)'] = pd.to_datetime(df['Referral Date (Date received)'], errors='coerce')
    
    # Extract year and month from the referral date
    df['Year-Month'] = df['Referral Date (Date received)'].dt.strftime('%Y-%m')
    
    # Count total referrals by year-month
    monthly_referrals = df.groupby('Year-Month').size().rename('Referrals In')
    
    # Count successful intakes ('Y') by year-month
    successful_intakes = df[df['Successful intake? (Y/N)2'] == 'Y'].groupby('Year-Month').size().rename('Successful Intakes')
    
    # Count referrals by source for each month
    referrals_by_source = df.pivot_table(index='Year-Month', columns='Referral\nSource', aggfunc='size', fill_value=0)
    
    # Combine the counts into a single DataFrame
    summary_df = pd.concat([monthly_referrals, referrals_by_source, successful_intakes], axis=1).fillna(0)
    
    # Display the DataFrame in Streamlit
    st.markdown("### Monthly Referral Summary")
    st.dataframe(summary_df)

# Example usage:
# df = pd.read_csv("your_data.csv")  # Replace with your actual data loading method
# Referrals(df)
