import streamlit as st
import pandas as pd

def MonthlyCases(df):
    # Convert date columns to datetime
    df['PC Date In'] = pd.to_datetime(df['PC Date In'], errors='coerce')
    df['PC Date Out'] = pd.to_datetime(df['PC Date Out'], errors='coerce')
    df['SC/SCP Date In'] = pd.to_datetime(df['SC/SCP Date In'], errors='coerce')
    df['SC/SCP Date Out'] = pd.to_datetime(df['SC/SCP Date Out'], errors='coerce')

    # Extract months
    df['PC Month'] = df['PC Date In'].dt.to_period('M')
    df['SC/SCP Month'] = df['SC/SCP Date In'].dt.to_period('M')

    # Determine the range of months in the data
    min_month = min(df['PC Month'].min(), df['SC/SCP Month'].min())
    max_month = max(df['PC Month'].max(), df['SC/SCP Month'].max())
    months_range = pd.period_range(start=min_month, end=max_month, freq='M')

     # Filter for PC, SC, SCP cases
    pc_cases = df[pd.isnull(df['PC Date Out']) & pd.notnull(df['PC Date In'])]
    sc_cases = df[pd.isnull(df['SC/SCP Date Out']) & pd.notnull(df['SC/SCP Date In']) & pd.isnull(df['SCP Date In'])]
    scp_cases = df[pd.isnull(df['SC/SCP Date Out']) & pd.notnull(df['SC/SCP Date In']) & pd.notnull(df['SCP Date In'])]

    # Initialize a DataFrame to store the results
    result = pd.DataFrame(index=months_range)

    # Count PC, SC, SCP cases for each month
    result['PC'] = pc_cases.groupby('PC Month').size().reindex(months_range, fill_value=0)
    result['SC'] = sc_cases.groupby('SC/SCP Month').size().reindex(months_range, fill_value=0)
    result['SCP'] = scp_cases.groupby('SC/SCP Month').size().reindex(months_range, fill_value=0)

    # Add a new column for SC + SCP
    result['SC + SCP'] = result['SC'] + result['SCP']

    # Format the index to 'YYYY-MM'
    result.index = result.index.strftime('%Y-%m')

    st.markdown("### Data Table: Monthly Case Count")
    st.dataframe(result)
