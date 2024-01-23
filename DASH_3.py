import streamlit as st
import pandas as pd
import altair as alt
import numpy as np
from datetime import datetime, timedelta,datetime
import plotly.express as px
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)


# Suppress specific warnings from pandas
pd.options.mode.chained_assignment = None
   # Set up the page configuration
st.set_page_config(page_title="BINANCE", page_icon=":bank:", layout="wide")
# Title and custom styles
st.title(":bar_chart: BINANCE")
st.markdown('<style>div.block-container{padding-top:1rem;}</style>', unsafe_allow_html=True)

def read_and_process_file(uploaded_file):
    if uploaded_file:
        try:
            df = pd.read_csv(uploaded_file) if uploaded_file.name.endswith('.csv') else pd.read_excel(uploaded_file)
          
            df['SYMBOL'] = df['SYMBOL'].str.replace('"', '').str.strip()
            df['PRICE'] = pd.to_numeric(df['PRICE'].str.replace('"', '').str.strip(), errors='coerce')
            df['QUANTITY'] = pd.to_numeric(df['QUANTITY'].str.strip(), errors='coerce')
            df.dropna(inplace=True)
            df['PRICE'] = df['PRICE'].round(4)
            df['QUANTITY'] = df['QUANTITY'].round(4)
            
            return df
        except Exception as e:
            print(f"Error reading file: {e}")
    return pd.DataFrame()

def format_datetime(df, column_name='EVENT_TIME'):
    if column_name in df.columns:
        df[column_name] = pd.to_datetime(df[column_name], format='%Y-%m-%d %H:%M:%S', errors='coerce')

        df.dropna(subset=[column_name], inplace=True)
        df[column_name] = df[column_name].dt.tz_localize(None)
    return df

def create_combined_chart(df1, column1, currency1, df2, column2, currency2):
    # Check if DataFrame df1 is empty
    if df1 is None or df1.empty:
        st.error("DataFrame 1 is empty. Cannot create chart.")
        return None

    # Check if DataFrame df2 is empty
    if df2 is None or df2.empty:
        st.error("DataFrame 2 is empty. Cannot create chart.")
        return None
    
    # Convert column to numeric and drop NaNs in df1
    df1[column1] = pd.to_numeric(df1[column1], errors='coerce')
    df1.dropna(subset=[column1], inplace=True)

    # Convert column to numeric and drop NaNs in df2
    df2[column2] = pd.to_numeric(df2[column2], errors='coerce')
    df2.dropna(subset=[column2], inplace=True)

    # Create 'Value' and 'Category' columns in df1
    df1['Value'] = df1[column1]
    df1['Category'] = f"{currency1} {column1}"

    # Create 'Value' and 'Category' columns in df2
    df2['Value'] = df2[column2]
    df2['Category'] = f"{currency2} {column2}"

    # Concatenate df1 and df2 along rows
    combined_df = pd.concat([df1[['EVENT_TIME', 'Value', 'Category']], df2[['EVENT_TIME', 'Value', 'Category']]], axis=0, ignore_index=True)

    # Check if 'Value' and 'Category' columns are numeric
    combined_df['Value'] = pd.to_numeric(combined_df['Value'], errors='coerce')
    combined_df.dropna(subset=['Value'], inplace=True)

    if combined_df.empty:
        st.error("No numeric values found in 'Value' column.")
        return None

    zoom = alt.selection_interval(bind='scales', encodings=['x', 'y'])

    chart = alt.Chart(combined_df).mark_line().encode(
        x=alt.X('utchoursminutesseconds(EVENT_TIME):T', title='Event Time',
                axis=alt.Axis(format='%H:%M:%S', labelFontSize=15, labelColor='white', labelAngle=-90)),
        y=alt.Y('Value:Q', title='Values', scale=alt.Scale(zero=False)),
        color=alt.Color('Category:N', scale=alt.Scale(domain=[df1['Category'].iloc[0], df2['Category'].iloc[0]], range=['yellow', 'red'])),
        tooltip=['EVENT_TIME:T', 'Value:Q', 'Category:N']
    ).add_params(
        zoom
    ).properties(
        title=f"{currency1} {column1} and {currency2} {column2} Over Time",
        background='black',
        width=1950,
        height=1200
    ).configure_view(
        strokeOpacity=0
    ).configure_axis(
        gridColor='grey',
        titleColor='white',
        labelColor='white',
        tickColor='white'
    ).configure_title(
        color='white',
        fontSize=20
    )

    return chart


def create_histogram(df, selected_column, currency, df1, column1, currency1, df2, column2, currency2):
    # Check if DataFrame is empty
    if df is None or df.empty:
        st.error("DataFrame is empty. Cannot create histogram.")
        return None

    # Check if selected column exists in the DataFrame
    if selected_column not in df.columns:
        st.error(f"Column '{selected_column}' not found in the dataframe.")
        return None

    # Convert column to numeric and drop NaNs
    df[selected_column] = pd.to_numeric(df[selected_column], errors='coerce')
    df.dropna(subset=[selected_column], inplace=True)

    # Create 'Value' and 'Category' columns in df1
    df1['Value'] = pd.to_numeric(df1[column1], errors='coerce')
    df1['Category'] = f"{currency1} {column1}"

    # Create 'Value' and 'Category' columns in df2
    df2['Value'] = pd.to_numeric(df2[column2], errors='coerce')
    df2['Category'] = f"{currency2} {column2}"

    # Concatenate df1 and df2 along rows
    combined_df = pd.concat([df1[['EVENT_TIME', 'Value', 'Category']], df2[['EVENT_TIME', 'Value', 'Category']]], axis=0, ignore_index=True)

    # Check if 'Value' and 'Category' columns are numeric
    combined_df['Value'] = pd.to_numeric(combined_df['Value'], errors='coerce')
    combined_df.dropna(subset=['Value'], inplace=True)

    if combined_df.empty:
        st.error(f"No numeric values found in 'Value' column.")
        return None

    zoom = alt.selection_interval(bind='scales', encodings=['x', 'y'])

    # Create histogram chart with X and Y axis settings
    histogram_chart = alt.Chart(combined_df).mark_bar().encode(
        x=alt.X('utchoursminutesseconds(EVENT_TIME):T', title='Event Time',
                axis=alt.Axis(format='%H:%M:%S', labelFontSize=15, labelColor='white', labelAngle=-90)),
        y=alt.Y('Value:Q', title='Values', scale=alt.Scale(zero=False)),
        color=alt.Color('Category:N', scale=alt.Scale(domain=[df1['Category'].iloc[0], df2['Category'].iloc[0]], range=['yellow', 'red'])),
        tooltip=['EVENT_TIME:T', 'Value:Q', 'Category:N']
    ).properties(
        title=f"{currency1} {column1} and {currency2} {column2} Over Time",
        background='black',
        width=1000,
        height=800
    ).configure_view(
        strokeOpacity=0
    ).configure_axis(
        gridColor='grey',
        titleColor='white',
        labelColor='white',
        tickColor='white'
    ).configure_title(
        color='white',
        fontSize=20
    )

    # Display the histogram chart
    st.altair_chart(histogram_chart, use_container_width=True)

def create_interactive_table(df1, df2):
    st.write("Interactive Table")

    # Create a layout with two columns
    col1, col2 = st.columns(2)

    # Display the first 10 rows of the first DataFrame in the first column
    with col1:
        st.subheader("First DataFrame")
        st.write(df1)

    # Display the first 10 rows of the second DataFrame in the second column
    with col2:
        st.subheader("Second DataFrame")
        st.write(df2)

def make_table_interactive(table, columns, table_name):
    # Add interactivity to the table
    with st.expander(f"Options for {table_name}"):
        # Create checkboxes for each column
        selected_columns = st.multiselect(f"Select columns for {table_name}", columns, default=columns)

        # Extract data from the table
        table_data = table() if callable(table) else table

        # Filter the table based on selected columns
        if selected_columns:
            table_data = table_data[selected_columns]

        if hasattr(table_data, 'index') and table_data.index is not None:
            # Get the index column name
            index_column_name = table_data.index.name if hasattr(table_data.index, 'name') else 'index'

            # Convert the index column to a list
            index_column_values = table_data.index.tolist() if hasattr(table_data.index, 'tolist') else list(table_data.index)

            selected_rows = st.multiselect(f"Select rows for {table_name}", index_column_values, [])
            if selected_rows:
                st.write(f"Selected Rows for {table_name}: {selected_rows}")


def generate_file_processing_ui(uploaded_file, file_label, key_suffix):
    if uploaded_file is not None:
        # Read the file into a DataFrame
        df = pd.read_csv(uploaded_file)

        if 'EVENT_TIME' not in df.columns:
            st.error(f"'EVENT_TIME' column is missing from the {file_label} file.")
            return None, None, None, None, None

        df['EVENT_TIME'] = pd.to_datetime(df['EVENT_TIME'], format='%d.%m.%y %H:%M:%S', errors='coerce')
        unique_currencies = df['SYMBOL'].unique().tolist()
        selected_currency = st.sidebar.selectbox('Currency', unique_currencies, key=f'currency_select_{key_suffix}')
        selected_column = st.sidebar.selectbox('Column', df.columns, key=f'column_select_{key_suffix}')

        times = df['EVENT_TIME'].dt.strftime('%Y-%m-%d %H:%M:%S').unique().tolist()
        selected_start_time = st.sidebar.selectbox("Start Time", times, key=f'start_time_select_{key_suffix}')
        selected_end_time = st.sidebar.selectbox("End Time", times, key=f'end_time_select_{key_suffix}')

        currency_filtered_df = df[df['SYMBOL'] == selected_currency]
        time_filtered_df = currency_filtered_df[(currency_filtered_df['EVENT_TIME'] >= selected_start_time) & (currency_filtered_df['EVENT_TIME'] <= selected_end_time)]

        if selected_column and selected_column in time_filtered_df.columns:
            max_value = time_filtered_df[selected_column].max()
            min_value = time_filtered_df[selected_column].min()

            if pd.api.types.is_numeric_dtype(time_filtered_df[selected_column]):
                max_value = f"{max_value:.4f}" if selected_column == 'PRICE' else f"{max_value:.4f}"
                min_value = f"{min_value:.4f}" if selected_column == 'PRICE' else f"{min_value:.4f}"
            elif pd.api.types.is_datetime64_any_dtype(time_filtered_df[selected_column]):
                min_value = min_value.strftime('%Y-%m-%d %H:%M:%S')
                max_value = max_value.strftime('%Y-%m-%d %H:%M:%S')
            else:
                max_value = str(max_value)
                min_value = str(min_value)

            color = "blue"
            font_size = "16px"
            st.sidebar.markdown(f"<h1 style='color: {color}; font-size: {font_size};'>Min/{selected_column}: {min_value}</h1>", unsafe_allow_html=True)
            st.sidebar.markdown(f"<h1 style='color: {color}; font-size: {font_size};'>Max/{selected_column}: {max_value}</h1>", unsafe_allow_html=True)

            return time_filtered_df, selected_currency, selected_column, selected_start_time, selected_end_time
        else:
            st.error(f"No {file_label} file uploaded. Please upload a file.")
    else:
        st.warning(f"Please upload the {file_label} CSV file.")
    
    return None, None, None, None, None

def main(selected_panel):
    st.sidebar.title("Settings")

    # File upload logic
    uploaded_file_1 = st.sidebar.file_uploader("Upload FIRST CSV", type=["csv", "txt", "xlsx", "xls"], key='file_uploader_1')
    uploaded_file_2 = st.sidebar.file_uploader("Upload SECOND CSV", type=["csv", "txt", "xlsx", "xls"], key='file_uploader_2')

    # Generate processing UI for the first file
    df1, selected_currency1, selected_column1, start_datetime1, end_datetime1 = generate_file_processing_ui(uploaded_file_1, 'FIRST', '1')

    # Generate processing UI for the second file
    df2, selected_currency2, selected_column2, start_datetime2, end_datetime2 = generate_file_processing_ui(uploaded_file_2, 'SECOND', '2')

    if selected_panel == "HISTOGRAM":
        st.write("Histogram Display")

        # Create the histogram chart for the first DataFrame
        create_histogram(df1, selected_column1, 'USD', df1, selected_column1, selected_currency1, df2, selected_column2, selected_currency2)

        # Create the histogram chart for the second DataFrame
        create_histogram(df2, selected_column2, 'EUR', df1, selected_column1, selected_currency1, df2, selected_column2, selected_currency2)

    if selected_panel == "CHART":
        st.subheader("Line Chart")
        # Ensure both dataframes are available and then create and display the chart
        if df1 is not None and df2 is not None:
            combined_chart = create_combined_chart(df1, selected_column1, selected_currency1, df2, selected_column2, selected_currency2)
            print(combined_chart)  # Add this line for debugging
            if combined_chart is not None:
                st.altair_chart(combined_chart, use_container_width=True)

            else:
                st.error("Unable to create chart. Please check the data.")
        else:
            st.error("Both datasets must be available to display the combined chart.")

    if selected_panel == "DATA":
        # Display interactive table for the "DATA" panel
        if df1 is not None and df2 is not None:
            create_interactive_table(df1, df2)

if __name__ == "__main__":
    selected_panel = st.sidebar.radio("Select Panel", ['HISTOGRAM', 'CHART', 'DATA'])
    main(selected_panel)
