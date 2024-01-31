import streamlit as st
import pandas as pd
from datetime import datetime
from css import styles
from data_processors.cases_by_group import CasesByGroup
from data_processors.quarterly_status import QuartStatus
from data_processors.monthly_status import MonthlyStatus
from data_processors.monthly_cases import MonthlyCases
from data_processors.workerload import WorkerLoad
from data_processors.monthly import CombinedMonthlyStatusAndCases
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
    for col in ['PC Date In', 'PC Date Out', 'SC/SCP Date In', 'SC/SCP Date Out', 'SCP Date In']:
        df[col] = pd.to_datetime(df[col], errors='coerce')

    # Assuming your file uploading and data preprocessing steps are unchanged

    # Function calls with error handling
    functions_to_execute = [
        (CasesByGroup, "Cases by Group"),
        (CombinedMonthlyStatusAndCases, "Monthly Status and Cases"),
        (WorkerLoad, "Worker Load"),
        (StatusGroups, "Status by Groups"),
        (StatusWorkers, "Status by Workers"),
        (GenderDistribution, "Gender Distribution"),
        (RaceDistribution, "Race Distribution"),
        (AgeDistribution, "Age Distribution"),
        (AreaDistribution, "Area Distribution"),
        (Referrals, "Referral Count")
    ]

    for func, title in functions_to_execute:
        try:
            func(df)  # Attempt to execute the function with df as argument
        except Exception as e:
            st.error(f"Error in {title}: {e}")  # Display an error message specific to the function


    # # Function to plot cases by group in current month
    # CasesByGroup(df)

    # # Function to display monthly analysis
    # CombinedMonthlyStatusAndCases(df)

    # # Function to display workload per worker
    # WorkerLoad(df)

    # # Function to display monthly analysis
    # CombinedMonthlyStatusAndCases(df)

    # # Function to display status by groups
    # StatusGroups(df)

    # # Function to display status by workers
    # StatusWorkers(df)

    # # Function to display distributions
    # GenderDistribution(df)
    # RaceDistribution(df)
    # AgeDistribution(df)
    # AreaDistribution(df)

    # # Function to show referral count
    # Referrals(df)


