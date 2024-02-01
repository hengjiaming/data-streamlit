import pandas as pd
import plotly.express as px
import streamlit as st
from datetime import datetime

def GenderDistribution(df):
    # Normalize the Gender column: trim whitespace and unify categories
    df['Gender'] = df['Gender'].str.replace('\xa0', '')  # Replace non-breaking spaces
    df['Gender'] = df['Gender'].str.strip()  # Trim leading/trailing whitespace
    df['Gender'] = df['Gender'].replace({'M': 'Male', 'F': 'Female'}).fillna('NIL')

    # Count the occurrences of each gender
    gender_counts = df['Gender'].value_counts()

    # Create a pie chart
    fig = px.pie(gender_counts, values=gender_counts.values, names=gender_counts.index, title='Gender Distribution',
                 hole=.3, labels={'index':'Gender', 'value':'Count'})

    # Show absolute numbers in the pie chart
    fig.update_traces(textinfo='label+percent+value')

    # Display the new result table in Streamlit
    if gender_counts.empty:
        st.markdown("### Gender Distribution for Cases")
        st.write("No Data Found")
    else:
        st.markdown("### Gender Distribution for Cases")
        st.plotly_chart(fig)

def RaceDistribution(df):
    # Count the occurrences of each race
    race_counts = df['Race'].value_counts()

    # Create a pie chart
    fig = px.pie(race_counts, values=race_counts, names=race_counts.index, title='Race Distribution',
                 hole=.3, labels={'index':'Race', 'value':'Count'})

    # Show absolute numbers and percentages in the pie chart
    fig.update_traces(textinfo='label+percent+value')

    # Display the new result table in Streamlit
    if race_counts.empty:
        st.markdown("### Race Distribution for Cases")
        st.write("No Data Found")
    else:
        st.markdown("### Race Distribution for Cases")
        st.plotly_chart(fig)

def AgeDistribution(df):
    # Extract age and year of data entry, handling NaN values
    df[['Original Age', 'Year of Data Entry']] = df['Current Age (Year of Data Entry)'].str.extract(r'(\d+) \((\d+)\)')
    
    # Drop rows where either 'Original Age' or 'Year of Data Entry' is NaN
    df = df.dropna(subset=['Original Age', 'Year of Data Entry'])

    # Convert to integer
    df[['Original Age', 'Year of Data Entry']] = df[['Original Age', 'Year of Data Entry']].astype(int)

    # Update age based on the current year
    current_year = datetime.now().year
    df['Updated Age'] = df['Original Age'] + (current_year - df['Year of Data Entry'])

    # Define age ranges
    bins = [0, 11, 14, 16, 18, 21]
    labels = ['<11', '12-14', '15-16', '17-18', '19-21']
    
    # Categorize updated ages into specified ranges
    df['Age Range'] = pd.cut(df['Updated Age'], bins=bins, labels=labels, right=True)

    # Count the occurrences of each age range
    age_range_counts = df['Age Range'].value_counts()

    # Create and display a pie chart (assuming you are using Plotly Express)
    fig = px.pie(age_range_counts, values=age_range_counts, names=age_range_counts.index, title='Age Range Distribution',
                 hole=.3, labels={'index':'Age Range', 'value':'Count'})
    fig.update_traces(textinfo='label+percent+value')

    # Display the new result table in Streamlit
    if age_range_counts.empty:
        st.markdown("### Age Range Distribution for Cases")
        st.write("No Data Found")
    else:
        st.markdown("### Age Range Distribution for Cases")
        st.plotly_chart(fig)

def AreaDistribution(df):
    # Count the occurrences of each area
    area_counts = df['SSO Region (usual hangout)'].value_counts().reset_index()
    area_counts.columns = ['Area', 'Count']

    # Create a horizontal bar chart
    fig = px.bar(area_counts, y='Area', x='Count', title='Distribution by Area',
                 orientation='h',  # Make the bar chart horizontal
                 labels={'Area':'SSO Region (Usual Hangout)', 'Count':'Count'},
                 text='Count')  # Display count as text on the bars

    # Sort bars by count
    fig.update_layout(yaxis={'categoryorder':'total ascending'})
    
    # Show the text on the bars
    fig.update_traces(texttemplate='%{text}', textposition='outside')

    # Adjust layout for readability and to accommodate text
    fig.update_layout(height=400 + 20 * len(area_counts),  # Adjust height based on number of bars
                      margin=dict(l=10, r=10, t=50, b=10))

    # Display the new result table in Streamlit
    if area_counts.empty:
        st.markdown("### SSO Region (Usual Hangout) Distribution for Cases")
        st.write("No Data Found")
    else:
        st.markdown("### SSO Region (Usual Hangout) Distribution for Cases")
        st.plotly_chart(fig)
