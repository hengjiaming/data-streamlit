import streamlit as st
import matplotlib.pyplot as plt

def CasesByGroup(df, group_counts):
    st.markdown('### Cases Open by Group in Current Month')
    plt.figure(figsize=(10, 6))
    plt.pie(group_counts, labels=group_counts.index, autopct='%1.1f%%', startangle=140)
    plt.axis('equal')
    plt.title('Cases Open by Group in Current Month')
    st.pyplot(plt.gcf())
    