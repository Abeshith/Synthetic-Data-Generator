# Synthetic Data Generator App

This Streamlit application is designed to generate synthetic data based on user inputs. Users can either upload a CSV file for data sampling or define custom columns to generate topic-based synthetic data using a pre-trained language model.

**Click here for the app:** [Synthetic Data Generator  App](https://synthetic-data-generator-abe.streamlit.app/)

___

## Features

1. **Upload CSV File**: Users can upload a CSV file, and the app will generate synthetic data by sampling from the uploaded CSV.
2. **Topic-Based Data Generation**: Users can define columns (e.g., `Integer`, `String`, `Float`, `Category`) to create synthetic data based on a specified topic.
3. **Download Synthetic Data**: After generating the synthetic data, users can download it as a CSV file for further analysis.


___

## Code Explanation

### 1. Import Necessary Libraries
The following libraries are imported:
- **Streamlit (`st`)**: Used for creating the interactive web application.
- **Pandas (`pd`)**: For reading and manipulating CSV files.
- **NumPy (`np`)**: For generating numerical synthetic data.
- **Transformers (`pipeline`)**: To load the pre-trained language model (`gpt2`) for generating synthetic text values.


### 2. Page Configuration
The `st.set_page_config` function sets the title of the page to "Synthetic Data Generator" and uses an icon ("🔮") for visual appeal.

### 3. Application Title and Description
The main title is set using `st.title`, and a brief description is provided using `st.write` to inform users about the purpose of the app.

### 4. Sidebar Note
A small note is added in the sidebar using `st.sidebar.write` to warn users about a potential error when adding more than 5-10 rows simultaneously. This helps prevent common user errors.

### 5. File Uploader for CSV-Based Generation
- **`st.file_uploader`**: Enables users to upload a CSV file.
- If a file is uploaded and the user selects the **"CSV-Based"** option, the file is read using `pd.read_csv` and displayed in the app using `st.dataframe`.

### 6. Data Generation Options
A `selectbox` is created with two options:
1. **CSV-Based**: Generates synthetic data by sampling from the uploaded CSV.
2. **Topic-Based**: Generates synthetic data based on a user-defined topic.

### 7. CSV-Based Data Generation
If the uploaded file is not `None` and **"CSV-Based"** is selected:
1. **CSV Preview**: Displays a preview of the uploaded CSV file.
2. **Specify Number of Rows**: Users input the number of synthetic rows to generate.
3. **Sampling from CSV**: Generates synthetic data using `input_df.sample(n=min(num_rows, len(input_df)), replace=False)`.
4. **Data Display**: Shows the generated synthetic data in the Streamlit app.
5. **Download Option**: Enables the user to download the generated synthetic data as a CSV file.

### 8. Topic-Based Data Generation
If the **"Topic-Based"** option is selected:
1. **Specify Topic Name**: Users input a topic name to generate synthetic text values.
2. **Define Columns**: Users specify the number of columns (`num_columns`) and define the name and type of each column (`Integer`, `Float`, `String`, `Category`).
3. **Specify Number of Rows**: Users input the number of rows to generate for the synthetic data.
4. **Generate Synthetic Data**: Based on the user-defined columns:
   - **Integer**: Uses `np.random.choice(np.arange(0, 100), size=num_rows, replace=False)` to create unique integer values.
   - **Float**: Uses `np.random.uniform(0, 100, size=num_rows)` to generate random floating-point numbers.
   - **String**: Generates text values using the `text_generator` model (`GPT-2`). Each text value is generated based on the provided topic name and is stored as a unique entry.
   - **Category**: Creates categorical values using `np.random.choice(['A', 'B', 'C', 'D'], size=num_rows, replace=False)`.
   
5. **Data Display**: Displays the generated synthetic data in the Streamlit app.
6. **Download Option**: Enables the user to download the generated synthetic data as a CSV file.

### 9. Handling String Columns Efficiently
- For **String** columns, a set (`unique_entries`) is used to ensure that no duplicate entries are generated.
- Text values are generated using the `text_generator` model with `pipeline("text-generation", model="gpt2")`.
- The generated text values are appended to the column until the desired number of unique rows is achieved.

### 10. CSV Download Functionality
For both CSV-based and topic-based generation, the synthetic data is converted to CSV format using `to_csv(index=False)` and encoded using `encode('utf-8')`.
- **`st.download_button`**: Allows users to download the generated synthetic data with an appropriate file name.

## Requirements
The following libraries are needed to run the app:
- **Streamlit**: `pip install streamlit`
- **Pandas**: `pip install pandas`
- **NumPy**: `pip install numpy`
- **Transformers**: `pip install transformers`
- **Torch** (For using GPT-2): `pip install torch`

### App Usage Steps
1. **Select Data Generation Method**: Choose between **CSV-Based** or **Topic-Based** generation.
2. **For CSV-Based**:
   - Upload a CSV file and specify the number of synthetic rows.
   - Download the generated synthetic CSV.
3. **For Topic-Based**:
   - Define the topic name and column structure.
   - Generate and download synthetic data based on the topic.

## How to Run the Application Locally
1. Clone the repository:
    ```bash
    git clone https://github.com/your-repo/synthetic-data-generator.git
    ```
2. Navigate to the project directory:
    ```bash
    cd synthetic-data-generator
    ```
3. Install the required dependencies:
    ```bash
    pip install -r requirements.txt
    ```
4. Run the Streamlit application:
    ```bash
    streamlit run synthetic_data_generator.py
    ```
