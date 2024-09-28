import streamlit as st
import pandas as pd
import numpy as np

# Title and Description
st.set_page_config(page_title="Synthetic Data Generator", page_icon="🔮")
st.title("Synthetic Data Generator")
st.write("Upload a CSV file or specify columns to generate synthetic data based on a topic name.")
st.write("**Note:** This generator is not suitable for text-related tasks such as spam detection and sentiment analysis.")

# File Uploader for CSV-Based Generation
uploaded_file = st.file_uploader("Upload your input CSV file", type=["csv"])

# Data Generation Options
option = st.selectbox("Choose a Data Generation Method", ("CSV-Based", "Topic-Based"))

# CSV-Based Data Generation
if uploaded_file is not None and option == "CSV-Based":
    # Read the uploaded CSV
    input_df = pd.read_csv(uploaded_file)
    st.write("Uploaded CSV Data Preview:")
    st.dataframe(input_df)

    # Specify Number of Synthetic Rows to Generate
    num_rows = st.number_input("Number of Rows to Generate", min_value=1, value=10)

    # Generate Synthetic Data by Sampling from Uploaded CSV
    synthetic_data = input_df.sample(n=num_rows, replace=False).reset_index(drop=True)
    st.write("Generated Synthetic Data:")
    st.dataframe(synthetic_data)

    # Download as CSV
    csv = synthetic_data.to_csv(index=False).encode('utf-8')
    st.download_button(label="Download Synthetic Data as CSV", data=csv, file_name="synthetic_data.csv", mime='text/csv')

# Topic-Based Data Generation
elif option == "Topic-Based":
    # Specify a Topic Name
    topic_name = st.text_input("Enter a Topic Name", "Sample Topic")

    # Enter Columns Details
    st.write(f"Specify columns for the synthetic data based on **{topic_name}** topic:")
    num_columns = st.number_input("Number of Columns", min_value=1, value=3)

    # Create Empty Column Definitions
    column_details = {}
    for i in range(num_columns):
        col_name = st.text_input(f"Column {i+1} Name", f"Column_{i+1}")
        col_type = st.selectbox(f"Column {i+1} Type", ("Integer", "Float", "String", "Category"), key=f"type_{i}")
        column_details[col_name] = col_type

    # Specify Number of Rows for the Synthetic Data
    num_rows = st.number_input("Number of Rows to Generate", min_value=1, value=10)

    # Generate Synthetic Data Based on User-Defined Columns
    synthetic_data = pd.DataFrame()

    # Generate unique data for each column based on the defined type
    for col, col_type in column_details.items():
        if col_type == "Integer":
            synthetic_data[col] = np.random.choice(np.arange(0, 100), size=num_rows, replace=False)
        elif col_type == "Float":
            synthetic_data[col] = np.random.choice(np.round(np.linspace(0, 100, num_rows * 10)), size=num_rows, replace=False)
        elif col_type == "String":
            # Generate unique string values
            synthetic_data[col] = [f"Sample_Text_{i}" for i in range(num_rows)]
        elif col_type == "Category":
            synthetic_data[col] = np.random.choice(['A', 'B', 'C', 'D'], size=num_rows, replace=True)

    # Display Generated Data
    st.write(f"Generated Synthetic Data for Topic: **{topic_name}**")
    st.dataframe(synthetic_data)

    # Download as CSV
    csv = synthetic_data.to_csv(index=False).encode('utf-8')
    st.download_button(label="Download Synthetic Data as CSV", data=csv, file_name=f"{topic_name.lower().replace(' ', '_')}_synthetic_data.csv", mime='text/csv')
