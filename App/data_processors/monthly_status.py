import streamlit as st
import pandas as pd

def MonthlyStatus(df):
    date_columns = ['PC Date In', 'PC Date Out', 'SC/SCP Date In', 'SC/SCP Date Out']
    for col in date_columns:
        df[col] = pd.to_datetime(df[col], errors='coerce')

    # Extract months
    df['PC In Month'] = df['PC Date In'].dt.to_period('M')
    df['PC Out Month'] = df['PC Date Out'].dt.to_period('M')
    df['SC In Month'] = df['SC/SCP Date In'].dt.to_period('M')
    df['SC Out Month'] = df['SC/SCP Date Out'].dt.to_period('M')
    df['SCP In Month'] = df['SC/SCP Date Out'].dt.to_period('M')
    df['SCP Out Month'] = df['SC/SCP Date Out'].dt.to_period('M')
    df['Case Closed Month'] = df['SC/SCP Date Out'].dt.to_period('M')

    # Determine the range of months in the data
    all_months = pd.period_range(start=df[date_columns].min().min(), end=df[date_columns].max().max(), freq='M')

    # Initialize dataframe to store new results
    monthly_status_counts = pd.DataFrame(index=all_months)

    # Count occurences for each category per quarter 
    monthly_status_counts['PC Ins'] = df.groupby('PC In Month').size().reindex(all_months, fill_value=0)
    monthly_status_counts['PC Outs'] = df.groupby('PC Out Month').size().reindex(all_months, fill_value=0)
    # Count occurrences for SC and SCP separately
    sc_df = df[df['Registration Status'] == 'SC']
    scp_df = df[df['Registration Status'] == 'SCP']

    monthly_status_counts['SC Ins'] = sc_df.groupby('SC In Month').size().reindex(all_months, fill_value=0)
    monthly_status_counts['SCP Ins'] = scp_df.groupby('SCP In Month').size().reindex(all_months, fill_value=0)

    monthly_status_counts['SC Outs'] = sc_df.groupby('SC Out Month').size().reindex(all_months, fill_value=0)
    monthly_status_counts['SCP Outs'] = scp_df.groupby('SCP Out Month').size().reindex(all_months, fill_value=0)
    monthly_status_counts['Case Closed'] = df.groupby('Case Closed Month').size().reindex(all_months, fill_value=0)

    monthly_status_counts.index = monthly_status_counts.index.strftime('%Y-%m')

        # Sidebar filter component
    # st.sidebar.header("Filters")
    # if 'Group Name' in df:
    #     selected_group = st.sidebar.selectbox("Select a Group", df['Group Name'].unique())
    #     # Use this selection to filter data or modify charts

    # Display the new result table in Streamlit
    st.markdown("### Monthly Status Counts")
    st.dataframe(monthly_status_counts)