import streamlit as st
from datetime import datetime, timezone
from datetime import datetime, timezone

from datetime import datetime

from pytz import utc
import pandas as pd
import numpy as np
import altair as alt
import warnings
warnings.filterwarnings('ignore')

st.set_page_config(page_title="BINANCE", page_icon=":bar_chart:", layout="wide")
st.title(" :bar_chart: BINANCE")
st.markdown('<style>div.block-container{padding-top:1rem;}</style>',  unsafe_allow_html=True)

# Sidebar for uploading a file - add a unique key to the widget
uploaded_file = st.sidebar.file_uploader("Upload a file",  type=["csv", "txt", "xlsx", "xls"], key='file_uploader', encoding="utf-8" )

# Function to read and process uploaded file
def read_and_process_file(uploaded_file):
    if uploaded_file is not None:
        try:
            # Use the file size to check if the file is empty
            if uploaded_file.size > 0:
                # Read the file based on extension
                if uploaded_file.name.lower().endswith('.csv'):
                    df = pd.read_csv(uploaded_file)
                elif uploaded_file.name.lower().endswith(('.xlsx', '.xls')):
                    df = pd.read_excel(uploaded_file)
                elif uploaded_file.name.lower().endswith('.txt'):
                    df = pd.read_csv(uploaded_file, delimiter='\t')
                
                # Ensure 'EVENT_TIME' is a datetime column
                df['EVENT_TIME'] = pd.to_datetime(df['EVENT_TIME'])
                return df
            else:
                st.error("Uploaded file is empty.")
                return None
        except Exception as e:
            st.error(f"An error occurred while reading the file: {e}")
            return None
    else:
        st.info("Please upload a file to visualize the data.")
        return None

# Function to get unique currencies from the dataframe
def get_unique_currencies(df):
    if df is not None and 'SYMBOL' in df.columns:
        return df['SYMBOL'].unique().tolist()
    return []


# Function to create the Altair chart
def create_chart(df, selected_currency, start_datetime, end_datetime):
    df_filtered = df[(df['SYMBOL'] == selected_currency) &
                     (df['EVENT_TIME'] >= start_datetime) &
                     (df['EVENT_TIME'] <= end_datetime)]

    chart = alt.Chart(df_filtered).mark_line().encode(
    x='EVENT_TIME:T',  # Altair recognizes 'T' as a datetime field
    y='PRICE:Q',
    tooltip=['EVENT_TIME:T', 'PRICE:Q']
).properties(
    title='Cryptocurrency Prices'
).interactive()
    return chart


# Read and process the uploaded file
df = read_and_process_file(uploaded_file)
import pandas as pd

# Example: Assuming your EVENT_TIME is in UTC and you want to convert it to 'Europe/Berlin' timezone
df['EVENT_TIME'] = pd.to_datetime(df['EVENT_TIME'], utc=True)
df['EVENT_TIME'] = df['EVENT_TIME'].dt.tz_convert('Europe/Berlin')  # Convert from UTC to your desired timezone

# Check if dataframe is loaded
if df is not None:
    # Check for required columns in the dataframe
    required_columns = [
        "EVENT_TYPE", "EVENT_TIME", "SYMBOL", "TRADE_ID", "PRICE", "QUANTITY",
        "BUYER_ORDER_ID", "SELLER_ORDER_ID", "TRADE_TIME", "IS_BUYER_MARKET_MAKER"
    ]
    missing_columns = [col for col in required_columns if col not in df.columns]
    if missing_columns:
        st.error(f"The dataframe is missing the following required columns: {', '.join(missing_columns)}")
        st.stop()

    # Verify 'SYMBOL' column exists and get unique currencies
    if 'SYMBOL' in df.columns:
        st.dataframe(df.head(5))
        
        unique_currencies = get_unique_currencies(df)
        selected_currency = st.sidebar.selectbox('Select Currency', unique_currencies)
        
        # Extract unique times from EVENT_TIME column for the dropdown
        unique_times = df['EVENT_TIME'].dt.strftime('%Y-%m-%d %H:%M:%S').sort_values().unique()
        selected_start_time = st.sidebar.selectbox('Select Start Time', unique_times, index=0)
        selected_end_time = st.sidebar.selectbox('Select End Time', unique_times, index=len(unique_times) - 1)

                # Convert EVENT_TIME to timezone-aware UTC if it's not already
        if df['EVENT_TIME'].dt.tz is None:
            df['EVENT_TIME'] = pd.to_datetime(df['EVENT_TIME']).dt.tz_localize('UTC')
        else:
            df['EVENT_TIME'] = df['EVENT_TIME'].dt.tz_convert('UTC')

        # Convert selected times to timezone-aware UTC datetime
        start_datetime = datetime.strptime(selected_start_time, '%Y-%m-%d %H:%M:%S').replace(tzinfo=timezone.utc)
        end_datetime = datetime.strptime(selected_end_time, '%Y-%m-%d %H:%M:%S').replace(tzinfo=timezone.utc)

        # Filter the dataframe for the selected time range
        df_filtered = df[
            (df['EVENT_TIME'] >= pd.to_datetime(start_datetime)) &
            (df['EVENT_TIME'] <= pd.to_datetime(end_datetime))
        ]

        # Generate and display the chart
        chart = create_chart(df_filtered, selected_currency, start_datetime, end_datetime)
        st.altair_chart(chart, use_container_width=True)
else:
    st.error("Dataframe could not be loaded.")
