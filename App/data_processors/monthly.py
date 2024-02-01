import pandas as pd
import streamlit as st

def CombinedMonthlyStatusAndCases(df):
    # Convert date columns to datetime
    date_columns = ['PC Date In', 'PC Date Out', 'SC/SCP Date In', 'SC/SCP Date Out', 'SCP Date In']
    for col in date_columns:
        df[col] = pd.to_datetime(df[col], errors='coerce')
    
    # Extract months
    df['PC Month In'] = df['PC Date In'].dt.to_period('M')
    df['PC Month Out'] = df['PC Date Out'].dt.to_period('M')
    df['SC/SCP Month In'] = df['SC/SCP Date In'].dt.to_period('M')
    df['SC/SCP Month Out'] = df['SC/SCP Date Out'].dt.to_period('M')
    df['SCP Month In'] = df['SCP Date In'].dt.to_period('M')

    # Determine the range of months in the data
    min_month = df[date_columns].min().min().to_period('M')
    max_month = df[date_columns].max().max().to_period('M')
    months_range = pd.period_range(start=min_month, end=max_month, freq='M')

    # Initialize a DataFrame to store the results
    combined_results = pd.DataFrame(index=months_range.strftime('%Y-%m'))

    # Calculate cumulative and in/out counts for each status
    # Cumulative counts
    for month in months_range:
        combined_results.at[month.strftime('%Y-%m'), 'PC'] = df[(df['PC Month In'] <= month) & 
                                                                ((df['PC Month Out'] > month) | pd.isna(df['PC Month Out'])) & 
                                                                (df['SC/SCP Month In'] > month)].shape[0]
        combined_results.at[month.strftime('%Y-%m'), 'SC'] = df[(df['SC/SCP Month In'] <= month) & 
                                                                ((df['SC/SCP Month Out'] > month) | pd.isna(df['SC/SCP Month Out'])) & 
                                                                ((df['SCP Month In'] > month) | pd.isna(df['SCP Month In']))].shape[0]
        combined_results.at[month.strftime('%Y-%m'), 'SCP'] = df[(df['SCP Month In'] <= month) &
                                                                 ((df['SC/SCP Month Out'] > month) | pd.isna(df['SC/SCP Month Out']))].shape[0]

        combined_results.at[month.strftime('%Y-%m'), 'SC + SCP'] = combined_results.at[month.strftime('%Y-%m'), 'SC'] + combined_results.at[month.strftime('%Y-%m'), 'SCP']
        combined_results.at[month.strftime('%Y-%m'), 'SC to SCP Transitions'] = df[(df['SC/SCP Month In'] < month) & 
                                                                                   (df['SCP Month In'] == month)].shape[0]

    # In/Out counts
    combined_results['PC Ins'] = df.groupby('PC Month In').size().reindex(months_range, fill_value=0).values
    combined_results['PC Outs'] = df.groupby('PC Month Out').size().reindex(months_range, fill_value=0).values
    combined_results['SC Ins'] = df.groupby('SC/SCP Month In').size().reindex(months_range, fill_value=0).values
    combined_results['SC Outs'] = df.groupby('SC/SCP Month Out').size().reindex(months_range, fill_value=0).values
    combined_results['SCP Ins'] = df.groupby('SCP Month In').size().reindex(months_range, fill_value=0).values
    
    # Display the new result table in Streamlit
    st.markdown("### Combined Monthly Status and Case Counts")
    st.dataframe(combined_results)

# Example usage:
# df = pd.read_csv("your_data.csv")  # Make sure to load your data
# CombinedMonthlyStatusAndCases(df)
