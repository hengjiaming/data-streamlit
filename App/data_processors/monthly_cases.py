import streamlit as st
import pandas as pd

def MonthlyCases(df):
    # Convert date columns to datetime
    df['PC Date In'] = pd.to_datetime(df['PC Date In'])
    df['SC/SCP Date In'] = pd.to_datetime(df['SC/SCP Date In'])

    # Extract months
    df['PC Month'] = df['PC Date In'].dt.to_period('M')
    df['SC/SCP Month'] = df['SC/SCP Date In'].dt.to_period('M')

    # Determine the range of months in the data
    min_month = min(df['PC Month'].min(), df['SC/SCP Month'].min())
    max_month = max(df['PC Month'].max(), df['SC/SCP Month'].max())
    months_range = pd.period_range(start=min_month, end=max_month, freq='M')

    # Initialize a DataFrame to store the results
    result = pd.DataFrame(index=months_range)

    # Count PC, SC, SCP cases for each month
    result['PC'] = df[df['Registration Status'] == 'PC'].groupby('PC Month').size().reindex(months_range, fill_value=0)
    result['SC'] = df[df['Registration Status'] == 'SC'].groupby('SC/SCP Month').size().reindex(months_range, fill_value=0)
    result['SCP'] = df[df['Registration Status'] == 'SCP'].groupby('SC/SCP Month').size().reindex(months_range, fill_value=0)

    # Format the index to 'YYYY-MM'
    result.index = result.index.strftime('%Y-%m')

    st.markdown("### Data Table: Monthly Case Count")
    st.dataframe(result)
