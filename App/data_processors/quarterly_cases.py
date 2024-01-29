import streamlit as st
import pandas as pd

def QuartCases(df):
    # Convert date columns to datetime
    df['PC Date In'] = pd.to_datetime(df['PC Date In'])
    df['SC/SCP Date In'] = pd.to_datetime(df['SC/SCP Date In'])

    # Extract quarters
    df['PC Quarter'] = df['PC Date In'].dt.to_period('Q')
    df['SC/SCP Quarter'] = df['SC/SCP Date In'].dt.to_period('Q')

    # Determine the range of quarters in the data
    min_quarter = min(df['PC Quarter'].min(), df['SC/SCP Quarter'].min())
    max_quarter = max(df['PC Quarter'].max(), df['SC/SCP Quarter'].max())
    quarters_range = pd.period_range(start=min_quarter, end=max_quarter, freq='Q')

    # Initialize a DataFrame to store the results
    result = pd.DataFrame(index=quarters_range)

    # Count PC, SC, SCP cases for each quarter
    result['PC'] = df[df['Registration Status'] == 'PC'].groupby('PC Quarter').size().reindex(quarters_range, fill_value=0)
    result['SC'] = df[df['Registration Status'] == 'SC'].groupby('SC/SCP Quarter').size().reindex(quarters_range, fill_value=0)
    result['SCP'] = df[df['Registration Status'] == 'SCP'].groupby('SC/SCP Quarter').size().reindex(quarters_range, fill_value=0)

    st.markdown("### Data Table: Quarterly Case Count")
    st.dataframe(result)