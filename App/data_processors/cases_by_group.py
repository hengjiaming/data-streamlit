import pandas as pd
import streamlit as st
import plotly.express as px

def CasesByGroup(df):
    # Convert date columns to datetime
    df['PC Date In'] = pd.to_datetime(df['PC Date In'], errors='coerce')
    df['PC Date Out'] = pd.to_datetime(df['PC Date Out'], errors='coerce')
    df['SC/SCP Date In'] = pd.to_datetime(df['SC/SCP Date In'], errors='coerce')
    df['SC/SCP Date Out'] = pd.to_datetime(df['SC/SCP Date Out'], errors='coerce')
    df['SCP Date In'] = pd.to_datetime(df['SCP Date In'], errors='coerce')

    # Get current month as a datetime object representing the first day of the month
    current_month_start = pd.to_datetime('today').replace(day=1)

    # Adjust the conditions for filtering based on datetime comparisons
    open_cases_current_month = df[((df['SC/SCP Date In'] < current_month_start) & 
                                   ((df['SC/SCP Date Out'] >= current_month_start) | pd.isna(df['SC/SCP Date Out'])) |
                                   ((df['SCP Date In'] <= current_month_start) & pd.isna(df['SC/SCP Date Out'])))]
    
    # Calculate counts for each group
    group_counts = open_cases_current_month['Group Name'].value_counts()

    st.markdown('### Cases Open by Group in Current Month')
    # Create a pie chart using Plotly
    fig = px.pie(group_counts, values=group_counts.values, names=group_counts.index, 
                 title='Cases Open by Group in Current Month')

    # Show the figure in Streamlit
    st.plotly_chart(fig)
