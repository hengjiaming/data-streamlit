import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

# Page configuration
st.set_page_config(page_title="Data Analysis Dashboard", page_icon="📊", layout="wide")

# CSS for styling
css = """
<style>
    .big-font {
        font-size: 20px !important;
    }
    .header {
        color: blue;
        font-size: 30px;
        font-weight: bold;
    }
    .stDataFrame {
        font-size: 20px !important;
    }
</style>
"""
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

    st.markdown("### Cases Open by Group in Current Month")
    plt.figure(figsize=(10, 6))
    plt.pie(group_counts, labels=group_counts.index, autopct='%1.1f%%', startangle=140)
    plt.axis('equal')
    plt.title('Cases Open by Group in Current Month')
    st.pyplot(plt.gcf())

    # Additional Data Processing for Table
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
    st.dataframe(result.style.set_properties(**{'background-color': 'lightgray', 
                                                    'color': 'black', 
                                                    'border-color': 'white'}))
    
    # # Plot table for visualization using Matplotlib
    # st.markdown("### Matplotlib Table: Quarterly Case Count")
    # fig, ax = plt.subplots(figsize=(10, 2))
    # ax.axis('off')
    # ax.table(cellText=result.values,colLabels=result.columns, rowLabels=result.index, loc='center')
    # st.pyplot(fig)

    st.sidebar.header("Filters")
    if 'Group Name' in df:
        selected_group = st.sidebar.selectbox("Select a Group", df['Group Name'].unique())
        # Use this selection to filter data or modify charts

    # Convert relevant date columns to datetime
    date_columns = ['PC Date In', 'PC Date Out', 'SC/SCP Date In', 'SC/SCP Date Out']
    for col in date_columns:
        df[col] = pd.to_datetime(df[col], errors='coerce')

    # Extract quarters
    df['PC In Quarter'] = df['PC Date In'].dt.to_period('Q')
    df['PC Out Quarter'] = df['PC Date Out'].dt.to_period('Q')
    df['SC In Quarter'] = df['SC/SCP Date In'].dt.to_period('Q')
    df['SC Out Quarter'] = df['SC/SCP Date Out'].dt.to_period('Q')
    df['SCP In Quarter'] = df['SC/SCP Date Out'].dt.to_period('Q')
    df['SCP Out Quarter'] = df['SC/SCP Date Out'].dt.to_period('Q')
    df['Case Closed Quarter'] = df['SC/SCP Date Out'].dt.to_period('Q')

    # Determine the range of quarters in the data
    all_quarters = pd.period_range(start=df[date_columns].min().min(), end=df[date_columns].max().max(), freq='Q')

    # Initialize a DataFrame to store the new results
    quarterly_status_counts = pd.DataFrame(index=all_quarters)

    # Count occurrences for each category per quarter
    quarterly_status_counts['PC Ins'] = df.groupby('PC In Quarter').size().reindex(all_quarters, fill_value=0)
    quarterly_status_counts['PC Outs'] = df.groupby('PC Out Quarter').size().reindex(all_quarters, fill_value=0)
    # Count occurrences for SC and SCP separately
    sc_df = df[df['Registration Status'] == 'SC']
    scp_df = df[df['Registration Status'] == 'SCP']

    quarterly_status_counts['SC Ins'] = sc_df.groupby('SC In Quarter').size().reindex(all_quarters, fill_value=0)
    quarterly_status_counts['SCP Ins'] = scp_df.groupby('SCP In Quarter').size().reindex(all_quarters, fill_value=0)

    quarterly_status_counts['SC Outs'] = sc_df.groupby('SC Out Quarter').size().reindex(all_quarters, fill_value=0)
    quarterly_status_counts['SCP Outs'] = scp_df.groupby('SCP Out Quarter').size().reindex(all_quarters, fill_value=0)
    quarterly_status_counts['Case Closed'] = df.groupby('Case Closed Quarter').size().reindex(all_quarters, fill_value=0)

    # Display the new result table in Streamlit
    st.markdown("### Quarterly Status Counts")
    st.dataframe(quarterly_status_counts)

    # New Data Processing for Worker Statistics
    # Group by 'Current Worker (Initials)' to count total cases per worker
    total_cases = df['Current Worker (Initials)'].value_counts()

    # Count 'PC Date In' occurrences per worker
    cases_in = df.groupby('Current Worker (Initials)')['PC Date In'].count()

    # Count 'SC/SCP Date Out' occurrences per worker
    cases_closed = df.groupby('Current Worker (Initials)')['SC/SCP Date Out'].count()

    # Creating a DataFrame for worker statistics
    worker_stats = pd.DataFrame({
        'Worker': total_cases.index,
        'Total Number of Cases': total_cases.values,
        'Number of Cases In': cases_in.reindex(total_cases.index, fill_value=0).values,
        'Number of Cases Closed': cases_closed.reindex(total_cases.index, fill_value=0).values
    })

    # Display the worker statistics table in Streamlit
    st.markdown("### Worker Statistics")
    st.dataframe(worker_stats)



