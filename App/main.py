import streamlit as st
import pandas as pd
from datetime import datetime
from css import styles
from data_processors.cases_by_group import CasesByGroup
from data_processors.quarterly_status import QuartStatus
from data_processors.monthly_status import MonthlyStatus
from data_processors.monthly_cases import MonthlyCases
from data_processors.workerload import WorkerLoad
from data_processors.monthly import MonthlyAnalysis
from data_processors.status_by_group import StatusGroups
from data_processors.status_by_group import StatusWorkers
from data_processors.distribution import GenderDistribution
from data_processors.distribution import RaceDistribution
from data_processors.distribution import AgeDistribution
from data_processors.distribution import AreaDistribution
from data_processors.referral_count import Referrals

# Page configuration
st.set_page_config(page_title="Data Analysis Dashboard", page_icon="📊", layout="wide")

# CSS for styling
css = styles

st.markdown(css, unsafe_allow_html=True)

# Header
st.markdown('<p class="header">Streamlit Data Analysis Demonstration</p>', unsafe_allow_html=True)

st.markdown('''
<p class="big-font">This dashboard provides a dynamic and interactive way to explore 
your data. Use the filters in the sidebar to customize the data and charts displayed. Instructions for usage as follows:</p>
''', unsafe_allow_html=True)
st.markdown('''
<li class="big-font">Access the deployed web application via URL:</li>
<li class="big-font">Drag and drop or upload excel file into the upload box. Refer to sample excel file for required formatting. (Note that the column headers found in the sample excel file are required and should not be renamed or removed)</li>
<li class="big-font">Let the web application load and generate the analysis charts</li>
<li class="big-font">Download the necessary chart data before you close the application since no data is going to be stored.</li>
''', unsafe_allow_html=True)
st.markdown('''     
<p class="big-font">Column headers to have in excel file:</p>
<li class="big-font">Current Worker (Initials)</li>
<li class="big-font">Group Name</li>
<li class="big-font">Registration Status</li>
<li class="big-font">Gender</li>
<li class="big-font">Race</li>
<li class="big-font">Current Age (Year of Data Entry)</li>
<li class="big-font">SSO Region (usual hangout)</li>
<li class="big-font">PC Date In</li>
<li class="big-font">PC Date Out</li>
<li class="big-font">SC/SCP Date In</li>
<li class="big-font">SCP Date In</li>
<li class="big-font">SC/SCP Date Out</li>
<li class="big-font">Referral Date (Date received)</li>
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
    print(current_month, current_year)
    df_filtered = df[df['SC/SCP Date In'].dt.month == current_month]
    df_filtered = df_filtered[df_filtered['SC/SCP Date In'].dt.year == current_year]
    group_counts = df_filtered['Group Name'].value_counts()
    print(group_counts)

    # Sidebar filter component
    # st.sidebar.header("Filters")
    # if 'Group Name' in df:
    #     selected_group = st.sidebar.selectbox("Select a Group", df['Group Name'].unique())
    #     # Use this selection to filter data or modify charts

    # Function to plot cases by group in current month
    CasesByGroup(df, group_counts)

    # Function to plot monthly cases
    MonthlyCases(df)

    # Function to generate monthly status table
    MonthlyStatus(df)

    # Function to display workload per worker
    WorkerLoad(df)

    # Function to display monthly analysis
    MonthlyAnalysis(df)

    # Function to display status by groups
    StatusGroups(df)

    # Function to display status by workers
    StatusWorkers(df)

    # Function to display distributions
    GenderDistribution(df)
    RaceDistribution(df)
    AgeDistribution(df)
    AreaDistribution(df)

    # Function to show referral count
    Referrals(df)


