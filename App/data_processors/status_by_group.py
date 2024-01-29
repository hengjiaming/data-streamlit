import pandas as pd
import streamlit as st

def StatusGroups(df):
    # Ensure proper datetime format for all date columns
    df['PC Date In'] = pd.to_datetime(df['PC Date In'], errors='coerce')
    df['PC Date Out'] = pd.to_datetime(df['PC Date Out'], errors='coerce')
    df['SC/SCP Date In'] = pd.to_datetime(df['SC/SCP Date In'], errors='coerce')
    df['SC/SCP Date Out'] = pd.to_datetime(df['SC/SCP Date Out'], errors='coerce')
    df['Date of Parental Consent'] = pd.to_datetime(df['Date of Parental Consent'], errors='coerce')

    # Filter for PC, SC, SCP cases
    pc_cases = df[pd.isnull(df['PC Date Out']) & pd.notnull(df['PC Date In'])]
    sc_cases = df[pd.isnull(df['SC/SCP Date Out']) & pd.notnull(df['SC/SCP Date In']) & pd.isnull(df['Date of Parental Consent'])]
    scp_cases = df[pd.isnull(df['SC/SCP Date Out']) & pd.notnull(df['SC/SCP Date In']) & pd.notnull(df['Date of Parental Consent'])]

    # Group by 'Group Name' and count cases
    pc_counts = pc_cases.groupby('Group Name').size().rename('PC')
    sc_counts = sc_cases.groupby('Group Name').size().rename('SC')
    scp_counts = scp_cases.groupby('Group Name').size().rename('SCP')

    # Combine counts into a single DataFrame
    combined_counts = pd.concat([pc_counts, sc_counts, scp_counts], axis=1).fillna(0)

# Display the new result table in Streamlit
    st.markdown("### Status Counts by Groups")
    st.dataframe(combined_counts)