import pandas as pd
import streamlit as st

def Referrals(df):
    # Adjust column names based on the actual columns in the dataframe
    referral_source_column = 'Referral\nSource'
    successful_intake_column = 'Successful intake? (Y/N)2'

    # Count total referrals
    total_referrals = df[referral_source_column].notna().sum()

    # Count successful intakes
    successful_intakes = df[successful_intake_column].value_counts().get('Y', 0)

    # Count referrals by source
    referrals_by_source = df[referral_source_column].value_counts()

    # Prepare the DataFrame to display in Streamlit
    # Initialize with Total Referral Count and Number of Successful Intakes
    summary_df = pd.DataFrame({
        "Total Referral Count": [total_referrals],
        "Number of Successful Intakes": [successful_intakes]
    })

    # Dynamically add each referral source and its count to the summary DataFrame
    for source, count in referrals_by_source.items():
        summary_df[f"Source - {source}"] = count

    # Display the DataFrame in Streamlit
    st.markdown("### Referral Summary")
    st.dataframe(summary_df.transpose().rename(columns={0: 'Count'}), height=600)