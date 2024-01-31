import streamlit as st
import pandas as pd

def MonthlyCases(df):
    # Convert date columns to datetime
    df['PC Date In'] = pd.to_datetime(df['PC Date In'], errors='coerce')
    df['PC Date Out'] = pd.to_datetime(df['PC Date Out'], errors='coerce')
    df['SC/SCP Date In'] = pd.to_datetime(df['SC/SCP Date In'], errors='coerce')
    df['SC/SCP Date Out'] = pd.to_datetime(df['SC/SCP Date Out'], errors='coerce')
    df['SCP Date In'] = pd.to_datetime(df['SCP Date In'], errors='coerce')

    # Extract months
    df['PC Month In'] = df['PC Date In'].dt.to_period('M')
    df['PC Month Out'] = df['PC Date Out'].dt.to_period('M')
    df['SC/SCP Month In'] = df['SC/SCP Date In'].dt.to_period('M')
    df['SCP Month In'] = df['SCP Date In'].dt.to_period('M')

    # Determine the range of months in the data
    min_month = df[['PC Month In', 'SC/SCP Month In', 'SCP Month In']].min().min()
    max_month = df[['PC Month In', 'SC/SCP Month In', 'SCP Month In']].max().max()
    months_range = pd.period_range(start=min_month, end=max_month, freq='M')

    # Initialize a DataFrame to store the results
    result = pd.DataFrame(index=months_range)

    # Calculate cumulative counts for each status
    for month in months_range:
        # PC cases are those entered as PC and not yet out or moved to SC/SCP
        result.at[month, 'PC'] = df[(df['PC Month In'] <= month) & 
                                    ((df['PC Month Out'] > month) | pd.isna(df['PC Month Out'])) & 
                                    (df['SC/SCP Month In'] > month)].shape[0]

        # SC cases are those entered as SC/SCP but not SCP yet
        result.at[month, 'SC'] = df[(df['SC/SCP Month In'] <= month) & 
                                    ((df['SCP Month In'] > month) | pd.isna(df['SCP Month In']))].shape[0]

        # SCP cases are those with SCP Date In
        result.at[month, 'SCP'] = df[df['SCP Month In'] <= month].shape[0]

        # SC + SCP cases are the sum of SC and SCP
        result.at[month, 'SC + SCP'] = result.at[month, 'SC'] + result.at[month, 'SCP']

    # Format the index to 'YYYY-MM'
    result.index = result.index.strftime('%Y-%m')

    st.markdown("### Data Table: Monthly Case Count")
    st.dataframe(result)
