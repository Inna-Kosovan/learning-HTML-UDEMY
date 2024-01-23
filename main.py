import streamlit as st
import pandas as pd
import altair as alt
import datetime
import numpy as np
import warnings
from datetime import datetime, timedelta
import warnings

warnings.filterwarnings('ignore')

# Set up the page configuration
st.set_page_config(page_title="BINANCE", page_icon=":bar_chart:", layout="wide")

# Title and custom styles
st.title(":bar_chart: BINANCE")
st.markdown('<style>div.block-container{padding-top:1rem;}</style>', unsafe_allow_html=True)

def upload_file():
    """Handles the file upload process in the sidebar."""
    return st.sidebar.file_uploader("Upload a file", type=["csv", "txt", "xlsx", "xls"], key='file_uploader')

# Function to read and process the file
def read_and_process_file(uploaded_file):
    # Dummy function for file processing
    return None  # Replace with actual file processing code

# # Function to validate datetime selection
def is_valid_datetime_range(start_datetime, end_datetime):
    return start_datetime < end_datetime

# Function to format the date and time
def format_datetime(dt):
    return dt.strftime('YY-MM-D HH:MM:SS')

def reformat_columns(df):
    """
    Reformats columns to remove commas from numbers and convert categorical columns to strings.
    """
    # Convert to integer and remove commas from numerical columns safely
    for column in ['TRADE_ID', 'BUYER_ORDER_ID', 'SELLER_ORDER_ID']:
        df[column] = df[column].astype(str).str.replace(',', '').astype(int)

    # Convert price and quantity to float, in case they are read as strings with commas
    df['PRICE'] = df['PRICE'].astype(str).str.replace(',', '').astype(int)
    df['QUANTITY'] = df['QUANTITY'].astype(str).str.replace(',', '').astype(float)

    # Convert yes/no columns to boolean
    df['IS_BUYER_MARKET_MAKER'] = df['IS_BUYER_MARKET_MAKER'].map({'N': False, 'Y': True})

    return df

# Define the create_chart function here
def create_chart(filtered_df, selected_column, selected_currency):
    # Ensure EVENT_TIME is timezone-naive
    filtered_df['EVENT_TIME'] = filtered_df['EVENT_TIME'].dt.tz_localize(None)
    
    # Create a chart using the filtered DataFrame
    chart = alt.Chart(filtered_df).mark_line().encode(
        x=alt.X('hoursminutesseconds(EVENT_TIME):T', title='Event Time'),  # Format axis
        y=alt.Y(f'{selected_column}:Q', title='Price or Quantity', scale=alt.Scale(zero=False)),
        tooltip=['EVENT_TIME:T', f'{selected_column}:Q']
    ).interactive().properties(
        title=f"{selected_currency} {selected_column} Over Time",
        background='black'
    ).configure_view(
        strokeOpacity=0
    ).configure_axis(
        gridColor='grey',
        titleColor='white',
        labelColor='white',
        tickColor='white'
    ).configure_title(
        color='white'
    )
    
    # Display the chart in Streamlit
    st.altair_chart(chart, use_container_width=True)
    
    return chart  # Return the chart object

def main():
    # Place the file uploader in the sidebar
    uploaded_file = st.sidebar.file_uploader("Upload CSV", type=["csv"], key='file_uploader')
    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
        if 'EVENT_TIME' not in df.columns:
            st.error("'EVENT_TIME' column is missing from the uploaded file.")
            return  # Stop execution if 'EVENT_TIME' is missing

        df['EVENT_TIME'] = pd.to_datetime(df['EVENT_TIME'])

        required_columns = [
            "EVENT_TYPE", "EVENT_TIME", "SYMBOL", "TRADE_ID", "PRICE", "QUANTITY",
            "BUYER_ORDER_ID", "SELLER_ORDER_ID", "TRADE_TIME", "IS_BUYER_MARKET_MAKER",
        ]
        # This is where you should define selected_column
        price_quantity_columns = ['PRICE', 'QUANTITY']
        if not all(col in df.columns for col in price_quantity_columns):
            st.error('The DataFrame does not contain all the required columns for charting.')
            return
        selected_column = st.sidebar.selectbox('Column', price_quantity_columns, key='data_column_select')
        unique_currencies = df['SYMBOL'].unique().tolist()
        selected_currency = st.sidebar.selectbox('Currency', unique_currencies, key='currency_select')

        # Assuming EVENT_TIME is already in the correct string format
        times = df['EVENT_TIME'].unique().tolist()
        selected_timeS = st.sidebar.selectbox("Start Time", times, key='start_time_select')
        selected_timeE = st.sidebar.selectbox("End Time", times, key='end_time_select')

        # Remove timezone info immediately after reading the CSV
        if 'EVENT_TIME' in df.columns:
            df['EVENT_TIME'] = pd.to_datetime(df['EVENT_TIME'])
        else:
            st.error("'EVENT_TIME' column is missing from the uploaded file.")
            return

        # Directly use the string values for filtering
        filtered_df = df[(df['EVENT_TIME'] >= selected_timeS) & (df['EVENT_TIME'] <= selected_timeE)]
       
        # Create tabs
        tab1, tab2 = st.tabs(["📈 Chart", "🗃 Data"])
        with tab1:
            st.subheader(f"Chart for {selected_currency}")
            # Now that selected_column is defined, pass it to create_chart
            chart = create_chart(filtered_df, selected_column, selected_currency)

        with tab2:
            st.subheader("Data")
            st.write(filtered_df)

    else:
        st.sidebar.info("Awaiting CSV file upload.")


# Ensure your create_chart function is defined before calling main
if __name__ == "__main__":
    main()