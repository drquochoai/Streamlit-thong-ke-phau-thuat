import streamlit as st
import streamlit as st
import pandas as pd

st.set_page_config(page_title="Tất cả các sheet")

# Load the data
data = pd.read_csv('path_to_your_data.csv')

# Set page title
st.set_page_config(page_title="Patient Surgery Weekly Report")

# Create a title
st.title("Patient Surgery Weekly Report")

# Display the data
st.dataframe(data)

# Add some visualizations
st.subheader("Number of Surgeries by Day")
surgery_count = data['Date'].value_counts().sort_index()
st.bar_chart(surgery_count)

st.subheader("Average Surgery Duration by Surgeon")
avg_duration = data.groupby('Surgeon')['Duration'].mean()
st.bar_chart(avg_duration)

# Add some additional sections and visualizations as needed

# Add a footer
st.footer("© 2022 Your Company")
