import pandas as pd
import streamlit as st

def MonthlyAnalysis(df):
    # Convert date columns to datetime
    df['PC Date In'] = pd.to_datetime(df['PC Date In'], errors='coerce')
    df['SC/SCP Date Out'] = pd.to_datetime(df['SC/SCP Date Out'], errors='coerce')

    # Drop rows where 'PC Date In' is NaT
    df = df.dropna(subset=['PC Date In'])

    # Set a default start and end date if they are NaT
    start_date = df['PC Date In'].min() if pd.notnull(df['PC Date In'].min()) else pd.Timestamp.now()
    end_date = df['SC/SCP Date Out'].max() if pd.notnull(df['SC/SCP Date Out'].max()) else pd.Timestamp.now()
    df['SC/SCP Date In'] = pd.to_datetime(df['SC/SCP Date In'], errors='coerce')
    df['SCP Date In'] = pd.to_datetime(df['SCP Date In'], errors='coerce')

    # Determine the range of dates to analyze
    monthly_range = pd.date_range(start=start_date, end=end_date, freq='M')

    # List to hold monthly data
    monthly_records = []

    # Analyze data for each month
    for month_end in monthly_range:
        month_start = month_end.replace(day=1)

        # Number of open cases
        open_cases = df[(df['PC Date In'] <= month_end) & 
                        ((df['SC/SCP Date Out'] > month_end) | pd.isnull(df['SC/SCP Date Out']))].shape[0]

        # Number of new cases
        new_cases = df[(df['PC Date In'] >= month_start) & (df['PC Date In'] <= month_end)].shape[0]

        # Number of closed cases
        closed_cases = df[(df['SC/SCP Date Out'] >= month_start) & (df['SC/SCP Date Out'] <= month_end)].shape[0]

        # Number of SC to SCP transitions
        sc_to_scp_transitions = df[(df['SC/SCP Date In'] >= month_start) & 
                                   (df['SC/SCP Date In'] <= month_end) &
                                   (df['SCP Date In'] > df['SC/SCP Date In'])].shape[0]

        # Add the data to the list
        monthly_records.append({
            'Month': month_end.strftime('%Y-%m'),
            'Open Cases': open_cases,
            'New Cases': new_cases,
            'Closed Cases': closed_cases,
            'SC to SCP': sc_to_scp_transitions
        })

    # Convert the list of dictionaries to a DataFrame
    monthly_data = pd.DataFrame(monthly_records)

    # Display the new result table in Streamlit
    st.markdown("### Monthly Case Analysis")
    st.dataframe(monthly_data)
