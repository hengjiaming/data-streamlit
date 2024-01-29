import streamlit as st
import plotly.express as px

def CasesByGroup(df, group_counts):
    st.markdown('### Cases Open by Group in Current Month')

    # Create a pie chart using Plotly
    fig = px.pie(group_counts, values=group_counts, names=group_counts.index, title='Cases Open by Group in Current Month')

    # Show the figure in Streamlit
    st.plotly_chart(fig)

    