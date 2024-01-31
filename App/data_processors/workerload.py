import streamlit as st
import pandas as pd

def WorkerLoad(df):
    # Group by 'Current Worker (Initials)' to count total cases per worker
    total_cases = df['Current Worker (Initials)'].value_counts()

    # Count 'PC Date In' occurrences per worker
    cases_in = df.groupby('Current Worker (Initials)')['PC Date In'].count()

    # Count 'SC/SCP Date Out' occurrences per worker
    cases_closed = df.groupby('Current Worker (Initials)')['SC/SCP Date Out'].count()

    # Creating dataframe for worker load
    worker_stats = pd.DataFrame({
        'Worker': total_cases.index,
        'Number of Cases In': cases_in.reindex(total_cases.index, fill_value=0).values,
        'Number of Cases Closed': cases_closed.reindex(total_cases.index, fill_value=0).values
    })

    # Display worker statistics table in Streamlit
    st.markdown('### Work Load Per Worker')
    st.dataframe(worker_stats)