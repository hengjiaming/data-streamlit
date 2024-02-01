import pandas as pd
import streamlit as st
from datetime import datetime

def StatusGroups(df):
   # Convert date columns to datetime format
    for col in ['PC Date In', 'PC Date Out', 'SC/SCP Date In', 'SC/SCP Date Out', 'SCP Date In']:
        df[col] = pd.to_datetime(df[col], errors='coerce')

    # Determine the current month's start and end
    current_month_start = datetime.now().replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    next_month_start = (current_month_start + pd.offsets.MonthBegin(1)).to_pydatetime()

    # Filter for PC, SC, SCP cases with additional logic
    pc_cases = df[(df['PC Date In'] <= current_month_start) & 
                  ((df['PC Date Out'] >= next_month_start) | pd.isnull(df['PC Date Out'])) & 
                  ((df['SC/SCP Date In'] >= next_month_start) | pd.isnull(df['SC/SCP Date In']))]

    sc_cases = df[(df['SC/SCP Date In'] <= current_month_start) & 
                  ((df['SC/SCP Date Out'] >= next_month_start) | pd.isnull(df['SC/SCP Date Out'])) & 
                  ((df['SCP Date In'] >= next_month_start) | pd.isnull(df['SCP Date In']))]

    scp_cases = df[(df['SCP Date In'] <= current_month_start) & 
                   ((df['SC/SCP Date Out'] >= next_month_start) | pd.isnull(df['SC/SCP Date Out']))]

    # Group by 'Group Name' and count cases
    pc_counts = pc_cases.groupby('Group Name').size().rename('PC Count')
    sc_counts = sc_cases.groupby('Group Name').size().rename('SC Count')
    scp_counts = scp_cases.groupby('Group Name').size().rename('SCP Count')

    # Combine counts into a single DataFrame
    combined_counts = pd.concat([pc_counts, sc_counts, scp_counts], axis=1).fillna(0)

# Display the new result table in Streamlit
    st.markdown("### Status Counts by Groups")
    st.dataframe(combined_counts)

def StatusWorkers(df):
    # Convert date columns to datetime format
    for col in ['PC Date In', 'PC Date Out', 'SC/SCP Date In', 'SC/SCP Date Out', 'SCP Date In']:
        df[col] = pd.to_datetime(df[col], errors='coerce')

    # Determine the current month's start and end
    current_month_start = datetime.now().replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    next_month_start = (current_month_start + pd.offsets.MonthBegin(1)).to_pydatetime()

    # Filter for PC, SC, SCP cases with additional logic
    pc_cases = df[(df['PC Date In'] <= current_month_start) & 
                  ((df['PC Date Out'] >= next_month_start) | pd.isnull(df['PC Date Out'])) & 
                  ((df['SC/SCP Date In'] >= next_month_start) | pd.isnull(df['SC/SCP Date In']))]

    sc_cases = df[(df['SC/SCP Date In'] <= current_month_start) & 
                  ((df['SC/SCP Date Out'] >= next_month_start) | pd.isnull(df['SC/SCP Date Out'])) & 
                  ((df['SCP Date In'] >= next_month_start) | pd.isnull(df['SCP Date In']))]

    scp_cases = df[(df['SCP Date In'] <= current_month_start) & 
                   ((df['SC/SCP Date Out'] >= next_month_start) | pd.isnull(df['SC/SCP Date Out']))]

    # Group by 'Worker' and count cases
    pc_counts = pc_cases.groupby('Current Worker (Initials)').size().rename('PC Count')
    sc_counts = sc_cases.groupby('Current Worker (Initials)').size().rename('SC Count')
    scp_counts = scp_cases.groupby('Current Worker (Initials)').size().rename('SCP Count')

    # Combine counts into a single DataFrame
    combined_counts = pd.concat([pc_counts, sc_counts, scp_counts], axis=1).fillna(0)

    # Display the new result table in Streamlit
    st.markdown("### Status Counts by Worker")
    st.dataframe(combined_counts)
