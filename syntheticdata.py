import streamlit as st
import pandas as pd
import numpy as np
from transformers import pipeline

# Load a pre-trained language model for generating text
text_generator = pipeline("text-generation", model="gpt2")

# Title and Description
st.set_page_config(page_title="Synthetic Data Generator", page_icon="🔮")
st.title("Synthetic Data Generator")
st.write("Upload a CSV file or specify columns to generate synthetic data based on a topic name.")

# Sidebar Note
st.sidebar.markdown("### Important Note:")
st.sidebar.write("This generator is not suitable for text-related tasks such as spam detection and sentiment analysis.Also Add rows one by one and if ypu add 5-10 rows at onece it'll show error!!")

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

    # Generate Synthetic Data by Sampling from Uploaded CSV without repetition
    synthetic_data = input_df.sample(n=min(num_rows, len(input_df)), replace=False).reset_index(drop=True)
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

    # Use a set to ensure unique entries
    unique_entries = set()

    # Generate data for each column based on the defined type
    for col, col_type in column_details.items():
        if col_type == "Integer":
            synthetic_data[col] = np.random.choice(np.arange(0, 100), size=num_rows, replace=False)
        elif col_type == "Float":
            synthetic_data[col] = np.random.uniform(0, 100, size=num_rows)
        elif col_type == "String":
            while len(synthetic_data[col]) < num_rows:
                entry = text_generator(f"Generate a realistic value for {topic_name}", max_length=10, num_return_sequences=1)[0]['generated_text']
                if entry not in unique_entries:
                    unique_entries.add(entry)
                    synthetic_data[col].append(entry)
            synthetic_data[col] = synthetic_data[col][:num_rows]  # Ensure exact number of rows
        elif col_type == "Category":
            synthetic_data[col] = np.random.choice(['A', 'B', 'C', 'D'], size=num_rows, replace=False)

    # Display Generated Data
    st.write(f"Generated Synthetic Data for Topic: **{topic_name}**")
    st.dataframe(synthetic_data)

    # Download as CSV
    csv = synthetic_data.to_csv(index=False).encode('utf-8')
    st.download_button(label="Download Synthetic Data as CSV", data=csv, file_name=f"{topic_name.lower().replace(' ', '_')}_synthetic_data.csv", mime='text/csv')
