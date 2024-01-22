import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
from css import styles
from data_processors.cases_by_group import CasesByGroup
from data_processors.quarterly_status import QuartStatus
from data_processors.quarterly_cases import QuartCases
from data_processors.workerload import WorkerLoad

# Page configuration
st.set_page_config(page_title="Data Analysis Dashboard", page_icon="📊", layout="wide")

# CSS for styling
css = styles

st.markdown(css, unsafe_allow_html=True)

# Header
st.markdown('<p class="header">Streamlit Data Analysis Demonstration</p>', unsafe_allow_html=True)

st.markdown('''
<p class="big-font">This dashboard provides a dynamic and interactive way to explore 
your data. Use the filters in the sidebar to customize the data and charts displayed.</p>
''', unsafe_allow_html=True)

# File Uploader
file_uploader = st.sidebar.file_uploader("Upload your Excel file", type=["xlsx"])

# Process file if uploaded
if file_uploader:
    df = pd.read_excel(file_uploader)

    # Data processing steps
    df = df.fillna("NIL")
    df['SC/SCP Date In'] = pd.to_datetime(df['SC/SCP Date In'], errors='coerce')
    current_month = datetime.now().month
    current_year = datetime.now().year
    df_filtered = df[df['SC/SCP Date In'].dt.month == current_month]
    df_filtered = df_filtered[df_filtered['SC/SCP Date In'].dt.year == current_year]
    group_counts = df_filtered['Group Name'].value_counts()

    # Sidebar filter component
    st.sidebar.header("Filters")
    if 'Group Name' in df:
        selected_group = st.sidebar.selectbox("Select a Group", df['Group Name'].unique())
        # Use this selection to filter data or modify charts

    # Function to plot cases by group in current month
    CasesByGroup(df, group_counts)

    # Function to plot quarterly cases
    QuartCases(df)

    # Function to generate quarterly status table
    QuartStatus(df)

    # Function to display workload per worker
    WorkerLoad(df)



