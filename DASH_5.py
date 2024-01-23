import streamlit as st
import pandas as pd
import altair as alt
import numpy as np
import time

from datetime import datetime, timedelta,datetime
import plotly.express as px
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)

# Suppress specific warnings from pandas
pd.options.mode.chained_assignment = None
   # Set up the page configuration
st.set_page_config(page_title="TRADING_LEVELS", page_icon=":dollar:", layout="wide")
# Title and custom styles
st.title(":bar_chart: TRADING_LEVELS")
st.markdown('<style>div.block-container{padding-top:1rem;}</style>', unsafe_allow_html=True)


# Function to load data from a CSV file
def load_data(file):
    data = pd.read_csv(file)

    # Extract unique values from the 'SYMBOL' column and 'EVENT_TIME' column
    if 'SYMBOL' in data.columns and 'EVENT_TIME' in data.columns:
        currency_values = data['SYMBOL'].unique()
        time_values = data['EVENT_TIME'].unique()
        return data  # Return only the DataFrame
    else:
        st.error("The 'SYMBOL' or 'EVENT_TIME' column is not present in the CSV file.")
        return pd.DataFrame()  # Return an empty DataFrame if columns are not present

def read_and_process_file(uploaded_file):
    if uploaded_file:
        try:
            date_format = '%Y-%m-%d %H:%M:%S'
            converters = {'EVENT_TIME': lambda x: pd.to_datetime(x, format=date_format, errors='coerce')}
            
            df = pd.read_csv(uploaded_file, converters=converters) if uploaded_file.name.endswith('.csv') else pd.read_excel(uploaded_file)          
            df['SYMBOL'] = df['SYMBOL'].str.replace('"', '').str.strip()
            df['PRICE'] = pd.to_numeric(df['PRICE'].str.replace('"', '').str.strip(), errors='coerce')
            df['QUANTITY'] = pd.to_numeric(df['QUANTITY'].str.strip(), errors='coerce')
            
            # Add the code to convert 'Column_Name' to numeric and handle errors
            df['Column_Name'] = pd.to_numeric(df['Column_Name'], errors='coerce')
            df['Column_Name'] = df['Column_Name'].fillna(0)  # Replace NaN values with 0 or handle missing values

            df.dropna(inplace=True)
            df['PRICE'] = df['PRICE'].round(4)
            df['QUANTITY'] = df['QUANTITY'].round(4)
            df['AMOUNT_SOLD_QUANTITY'] = df['AMOUNT_SOLD_QUANTITY'].astype(float)
            df['TOTAL_AMOUNT_SOLD_PRICE'] = df['TOTAL_AMOUNT_SOLD_PRICE'].astype(float)

            # Remove or comment out the print statements for the final version
            print(df.dtypes)
            return df
        except Exception as e:
            print(f"Error reading file: {e}")
    return pd.DataFrame()


def format_datetime(df, column_name='EVENT_TIME'):

    if column_name in df.columns:
        df[column_name] = pd.to_datetime(df[column_name], errors='coerce')

        df.dropna(subset=[column_name], inplace=True)
        df[column_name] = df[column_name].dt.tz_localize(None)
    return df

# Function to create Altair line chart
def create_chart(data, selected_currencies, selected_columns, start_time, end_time):
    # Filter data based on selected currencies and time interval
    filtered_data = data[data['SYMBOL'].isin(selected_currencies)]
    filtered_data = filtered_data[
        (filtered_data['EVENT_TIME'] >= start_time) & (filtered_data['EVENT_TIME'] <= end_time)
    ]

    # Check if there are selected currencies
    if not selected_currencies:
        st.warning("Please select at least one currency.")
        return None
    
    # Check if there are selected columns
    if not selected_columns:
        st.warning("Please select at least one column.")
        return None
    
    # Dynamically generate Y-axis encoding for selected columns
    y_encoding = [alt.Y(f'{col}:Q', title=f'{col} (Min-Max)', scale=alt.Scale(zero=False))
                  for col in selected_columns]

    zoom = alt.selection_interval(bind='scales', encodings=['x', 'y'])

    # Create Altair chart only if there are selected currencies and columns
    chart = alt.Chart(filtered_data).mark_line().encode(
        x=alt.X('EVENT_TIME:T', title='Event Time',
                axis=alt.Axis(format='%H:%M:%S', labelFontSize=15, labelColor='white', labelAngle=-90)),
        color=alt.Color('SYMBOL:N', legend=alt.Legend(title="Currencies")),  # Ensure legend title is set
        tooltip=['SYMBOL:N', 'EVENT_TIME:T'] + selected_columns
    ).properties(
        background='black',
        width=1450,
        height=800
    ).interactive()

    # Layer the dynamically generated Y-axis encoding on the chart
    chart = chart.encode(*y_encoding)

    return chart


# Function to create an interactive table
def create_interactive_table(df1, df2):
    st.write("Interactive Table")

    # Create a layout with two columns
    col1, col2 = st.columns(2)

    # Display the first 10 rows of the first DataFrame in the first column
    with col1:
        st.subheader("First DataFrame")
        st.write(df1)
        st.subheader("First dtypes")
        st.write(df1.dtypes)

    # Display the first 10 rows of the second DataFrame in the second column
    with col2:
        st.subheader("Second DataFrame")
        st.write(df2)
        st.subheader("Second dtypes")
        st.write(df2.dtypes)

# Function to display data type and table for the first DataFrame
def display_data_type(data, page_name):
    st.subheader(f"Data Types for {page_name} CSV File")
    st.write(data.dtypes)

# Function to display data table for the first DataFrame
def display_data_table(data, page_name):
    st.subheader(f"DataFrame Table for {page_name} CSV File")
    st.write(data)


# Main function
def main(selected_panel):
    st.sidebar.title("Settings")

    # Declare file1 and file2 at a higher scope with initial values
    file1 = None
    file2 = None

    # Upload CSV files
    st.sidebar.header("Upload CSV Files")

    # Button for the first CSV file
    file1 = st.sidebar.file_uploader("Upload CSV First", type=["csv"])

    # Button for the second CSV file
    file2 = st.sidebar.file_uploader("Upload CSV Second", type=["csv"])

    # Select currencies, columns, and time interval
    if file1 is not None and file2 is not None:
        st.sidebar.header("Select Options")

        # Load data from CSV files
        data1 = load_data(file1)

        # Get column names for CSV First
        column_names1 = data1.columns.tolist()

        # Display the 'Select Columns' button for CSV First
        selected_columns1 = st.sidebar.multiselect("Columns First", column_names1)

        # Combine unique currency values for the first file
        currency_values1 = list(set(data1['SYMBOL']))

        # Display the 'Select Currencies' button with unique values from both files
        currency_options1 = st.sidebar.multiselect("Currencies First", currency_values1)

        # Display the 'Select Start Time' and 'Select End Time' dropdowns for file1
        start_time1 = st.sidebar.selectbox("Start Time First", data1['EVENT_TIME'])
        end_time1 = st.sidebar.selectbox("End Time First", data1['EVENT_TIME'])

        # Load data from CSV files for the second file
        data2 = load_data(file2)

        # Get column names for CSV Second
        column_names2 = data2.columns.tolist()

        # Display the 'Select Columns' button for CSV Second
        selected_columns2 = st.sidebar.multiselect("Columns Second", column_names2)

        # Combine unique currency values for the second file
        currency_values2 = list(set(data2['SYMBOL']))

        # Display the 'Select Currencies' button with unique values from both files
        currency_options2 = st.sidebar.multiselect("Currencies Second", currency_values2)

        # Display the 'Select Start Time' and 'Select End Time' dropdowns for file2
        start_time2 = st.sidebar.selectbox("Start Time Second", data2['EVENT_TIME'])
        end_time2 = st.sidebar.selectbox("End Time Second", data2['EVENT_TIME'])

    if selected_panel == "CHART":
        # Display charts
        st.subheader("Chart for First")
        chart1 = create_chart(data1, currency_options1, selected_columns1, start_time1, end_time1)
        st.altair_chart(chart1)

        st.subheader("Chart for Second")
        chart2 = create_chart(data2, currency_options2, selected_columns2, start_time2, end_time2)
        st.altair_chart(chart2)

    if selected_panel == "DATA_CSV":
        # Display interactive table for the "DATA_CSV" panel
        if data1 is not None and data2 is not None:
            create_interactive_table(data1, data2)

if __name__ == "__main__":
    selected_panel = st.sidebar.radio("Select Panel", ['CHART', 'DATA_CSV'])
    main(selected_panel)
