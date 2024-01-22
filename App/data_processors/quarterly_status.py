import streamlit as st
import pandas as pd

def QuartStatus(df):
    date_columns = ['PC Date In', 'PC Date Out', 'SC/SCP Date In', 'SC/SCP Date Out']
    for col in date_columns:
        df[col] = pd.to_datetime(df[col], errors='coerce')

    # Extract quarters
    df['PC In Quarter'] = df['PC Date In'].dt.to_period('Q')
    df['PC Out Quarter'] = df['PC Date Out'].dt.to_period('Q')
    df['SC In Quarter'] = df['SC/SCP Date In'].dt.to_period('Q')
    df['SC Out Quarter'] = df['SC/SCP Date Out'].dt.to_period('Q')
    df['SCP In Quarter'] = df['SC/SCP Date Out'].dt.to_period('Q')
    df['SCP Out Quarter'] = df['SC/SCP Date Out'].dt.to_period('Q')
    df['Case Closed Quarter'] = df['SC/SCP Date Out'].dt.to_period('Q')

    # Determine the range of quarters in the data
    all_quarters = pd.period_range(start=df[date_columns].min().min(), end=df[date_columns].max().max(), freq='Q')

    # Initialize dataframe to store new results
    quarterly_status_counts = pd.DataFrame(index=all_quarters)

    # Count occurences for each category per quarter 
    quarterly_status_counts['PC Ins'] = df.groupby('PC In Quarter').size().reindex(all_quarters, fill_value=0)
    quarterly_status_counts['PC Outs'] = df.groupby('PC Out Quarter').size().reindex(all_quarters, fill_value=0)
    # Count occurrences for SC and SCP separately
    sc_df = df[df['Registration Status'] == 'SC']
    scp_df = df[df['Registration Status'] == 'SCP']

    quarterly_status_counts['SC Ins'] = sc_df.groupby('SC In Quarter').size().reindex(all_quarters, fill_value=0)
    quarterly_status_counts['SCP Ins'] = scp_df.groupby('SCP In Quarter').size().reindex(all_quarters, fill_value=0)

    quarterly_status_counts['SC Outs'] = sc_df.groupby('SC Out Quarter').size().reindex(all_quarters, fill_value=0)
    quarterly_status_counts['SCP Outs'] = scp_df.groupby('SCP Out Quarter').size().reindex(all_quarters, fill_value=0)
    quarterly_status_counts['Case Closed'] = df.groupby('Case Closed Quarter').size().reindex(all_quarters, fill_value=0)

    # Display the new result table in Streamlit
    st.markdown("### Quarterly Status Counts")
    st.dataframe(quarterly_status_counts)