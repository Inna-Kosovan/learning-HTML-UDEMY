import streamlit as st
import pandas as pd
import altair as alt
import numpy as np
import warnings
from datetime import datetime, timedelta
import plotly.express as px
from streamlit_option_menu import option_menu



# Suppress specific warnings from pandas
pd.options.mode.chained_assignment = None
warnings.filterwarnings('ignore')
   # Set up the page configuration
st.set_page_config(page_title="BINANCE", page_icon=":bank:", layout="wide")

# Title and custom styles
st.title(":bar_chart: BINANCE")
st.markdown('<style>div.block-container{padding-top:1rem;}</style>', unsafe_allow_html=True)


def read_and_process_file(uploaded_file):
        if uploaded_file:
            try:
                df = pd.read_csv(uploaded_file) if uploaded_file.name.endswith('.csv') else pd.read_excel(uploaded_file)
                df = reformat_columns(df)
                return df
            except Exception as e:
                st.error(f"Error reading file: {e}")
        return None

def reformat_columns(df):
    df['PRICE'] = pd.to_numeric(df['PRICE'].astype(str).str.replace(',', ''), errors='coerce')
    df['QUANTITY'] = pd.to_numeric(df['QUANTITY'].astype(str).str.replace(',', ''), errors='coerce')
    return df

def format_datetime(dt):
    return dt.strftime('%Y-%m-%d %H:%M:%S')


# def generate_file_processing_ui(df, file_label, key_suffix):
#     if df is not None:
#         try:
#             if 'EVENT_TIME' not in df.columns:
#                 st.error(f"'EVENT_TIME' column is missing from the {file_label} file.")
#                 return None
#             df['EVENT_TIME'] = pd.to_datetime(df['EVENT_TIME'], format='%d.%m.%y %H:%M:%S', errors='coerce').dt.tz_localize(None)
            
#             unique_currencies = df['SYMBOL'].unique().tolist()
#             selected_currency = st.sidebar.selectbox('Currency', unique_currencies, key=f'currency_select_{key_suffix}')
#             selected_column = st.sidebar.selectbox('Column', df.columns, key=f'column_select2_{key_suffix}')
            
#             times = df['EVENT_TIME'].dt.strftime('%Y-%m-%d %H:%M:%S').unique().tolist()
#             selected_start_time = st.sidebar.selectbox("Start Time", times, key=f'start_time_select_{key_suffix}')
#             selected_end_time = st.sidebar.selectbox("End Time", times, key=f'end_time_select_{key_suffix}')
            
#             currency_filtered_df = df[df['SYMBOL'] == selected_currency]
#             time_filtered_df = currency_filtered_df[(currency_filtered_df['EVENT_TIME'] >= selected_start_time) & (currency_filtered_df['EVENT_TIME'] <= selected_end_time)]
            
#             return time_filtered_df, selected_column, selected_currency, selected_start_time, selected_end_time
        
#         except pd.errors.EmptyDataError:
#             st.error(f"No columns to parse from the {file_label} file. Please check the file's contents.")
#         except Exception as e:
#             st.error(f"An error occurred with the {file_label} file: {e}")
#     else:
#         st.error(f"No {file_label} file uploaded. Please upload a file.")
#     return None, None, None, None, None

def create_combined_chart(df1, column1, currency1, df2, column2, currency2):
    if df1 is None or df1.empty or df2 is None or df2.empty:
        return None

    df1 = df1.copy()
    df2 = df2.copy()

    if column1 not in df1.columns:
        raise KeyError(f"Column '{column1}' not found in the first dataframe.")
    if column2 not in df2.columns:
        raise KeyError(f"Column '{column2}' not found in the second dataframe.")

    df1['Value'] = df1[column1]
    df1['Category'] = f"{currency1} {column1}"
    df2['Value'] = df2[column2]
    df2['Category'] = f"{currency2} {column2}"

    combined_df = pd.concat([df1[['EVENT_TIME', 'Value', 'Category']], df2[['EVENT_TIME', 'Value', 'Category']]], ignore_index=True)

    if not pd.api.types.is_numeric_dtype(combined_df['Value']):
        raise TypeError("Values in 'Value' column must be numeric.")

    zoom = alt.selection_interval(bind='scales', encodings=['x', 'y'])

    chart = alt.Chart(combined_df).mark_line().encode(
        x=alt.X('utchoursminutesseconds(EVENT_TIME):T', title='Event Time',
                axis=alt.Axis(format='%H:%M:%S', labelFontSize=15, labelColor='white', labelAngle=-90)),
        y=alt.Y('Value:Q', title='Values', scale=alt.Scale(zero=False)),
        color=alt.Color('Category:N', scale=alt.Scale(domain=[df1['Category'].iloc[0], df2['Category'].iloc[0]], range=['yellow', 'red'])),
        tooltip=['EVENT_TIME:T', 'Value:Q', 'Category:N']
    ).add_selection(
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


def generate_file_processing_ui(df, file_label, key_suffix):
    if df is not None:
        # No need to read the file here as 'df' is already the DataFrame
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
       
        
        # Ensure that selected_column is defined
        if selected_column and selected_column in time_filtered_df.columns:
            # Display max and min values in the sidebar
            max_value = time_filtered_df[selected_column].max()
            min_value = time_filtered_df[selected_column].min()

            # Check if the column is numeric
            if pd.api.types.is_numeric_dtype(time_filtered_df[selected_column]):
                # Format numeric values with appropriate decimal places
                max_value = f"{max_value:.4f}" if selected_column == 'PRICE' else f"{max_value:.4f}"
                min_value = f"{min_value:.4f}" if selected_column == 'PRICE' else f"{min_value:.4f}"
            elif pd.api.types.is_datetime64_any_dtype(time_filtered_df[selected_column]):
                # Format datetime values
                min_value = min_value.strftime('%Y-%m-%d %H:%M:%S')
                max_value = max_value.strftime('%Y-%m-%d %H:%M:%S')
            else:
                # If it's a non-numeric and non-datetime value, convert it to string
                max_value = str(max_value)
                min_value = str(min_value)
            color = "blue"
            font_size = "16px"
            st.sidebar.markdown(f"<h1 style='color: {color}; font-size: {font_size};'>Min/{selected_column}: {min_value}</h1>", unsafe_allow_html=True)
            st.sidebar.markdown(f"<h1 style='color: {color}; font-size: {font_size};'>Max/{selected_column}: {max_value}</h1>", unsafe_allow_html=True)

            return time_filtered_df, selected_currency, selected_column, selected_start_time, selected_end_time
        else:
            st.error(f"No {file_label} file uploaded. Please upload a file.")
        return None, None, None, None, None  # Return None for all expected outputs

def main():
    # Initialize variables to None or appropriate defaults
    time_filtered_df1 = None
    time_filtered_df2 = None

    with st.sidebar:
        selected = st.selectbox("PANEL", ['HOME', 'CHART'], 
                                format_func=lambda x: '🏠 HOME' if x == 'HOME' else '📈 Line Chart')

    if selected == "HOME":
        st.write("Home is where the heart is. Welcome to the main page!")

        uploaded_file_1 = st.file_uploader("Upload FIRST CSV", type=["csv", "txt", "xlsx", "xls"], key='file_uploader_1')
        if uploaded_file_1 is not None and isinstance(uploaded_file_1.name, str):
            df1 = pd.read_csv(uploaded_file_1) if uploaded_file_1.name.endswith('.csv') else pd.read_excel(uploaded_file_1)
            result = generate_file_processing_ui(df1, 'FIRST CSV', '1')
            if result:
                time_filtered_df1, selected_currency1, selected_column1, selected_start_time1, selected_end_time1 = result

        uploaded_file_2 = st.file_uploader("Upload SECOND CSV", type=["csv", "txt", "xlsx", "xls"], key='file_uploader_2')
        if uploaded_file_2 is not None:
            df2 = pd.read_csv(uploaded_file_2) if uploaded_file_2.name.endswith('.csv') else pd.read_excel(uploaded_file_2)
            result = generate_file_processing_ui(df2, 'SECOND CSV', '2')
            if result:
                time_filtered_df2, selected_currency2, selected_column2, selected_start_time2, selected_end_time2 = result

    elif selected == "CHART":
        st.write("Line Chart Display")
        st.write("Filtered Data")

    # Create tabs
    tabs = st.tabs(["🏠 HOME", "🗃 Data", "📈 Line Chart", "📊 Another Chart"])

    with tabs[1]:
        st.subheader("Filtered Data")
        # ... (code to display DataFrames)

    with tabs[2]:
        st.subheader("Line Chart")
        # Ensure both dataframes are available and then create and display the chart
        if time_filtered_df1 is not None and time_filtered_df2 is not None:
            # Assuming selected_currency1, selected_column1, selected_currency2, and selected_column2 are defined
            # and hold the appropriate values selected by the user
            combined_chart = create_combined_chart(time_filtered_df1, selected_column1, selected_currency1, 
                                                   time_filtered_df2, selected_column2, selected_currency2)
            if combined_chart is not None:
                st.altair_chart(combined_chart, use_container_width=True)
            else:
                st.error("Unable to create chart. Please check the data.")
        else:
            st.error("Both datasets must be available to display the combined chart.")

    with tabs[3]:
        st.write("Settings for the chart can be adjusted here.")

# Rest of your code...

if __name__ == "__main__":
    main()