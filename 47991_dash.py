import streamlit as st
import pandas as pd
import numpy as np
import altair as alt
from datetime import datetime, timedelta
import os
import warnings
warnings.filterwarnings('ignore')

st.set_page_config(page_title="BINANCE", page_icon=":bar_chart:",layout="wide")

st.title(" :bar_chart: BINANCE")
st.markdown('<style>div.block-container{padding-top:1rem;}</style>',unsafe_allow_html=True)

fl = st.file_uploader(":file_folder: Upload a file",type=(["csv","txt","xlsx","xls"]))
if fl is not None:
    filename = fl.name
    st.write(filename)
    df = pd.read_csv(filename, encoding = "ISO-8859-1")
else:
    os.chdir(r"/data/works/codes/data_csv")
    df = pd.read_csv("TABLE_10_11_ETHUSDT.csv", encoding = "ISO-8859-1")



# Define your list of currencies and intervals
currencies = ['ETHUSDT', 'ETHBTC', 'BTCUSDT', 'BNBETH', 'EOSETH', 'LTCBTC']
intervals = ['1 minute', '15 minutes', '30 minutes', '1 hour', '1 day', '1 month', '1 year']
years = [2020, 2021, 2022, 2023, 2024]

# Sidebar selections
selected_currency = st.sidebar.selectbox('Select Currency', currencies, key='currency_select')
selected_interval = st.sidebar.selectbox('Select Interval', intervals, key='interval_select')
selected_year = st.sidebar.selectbox('Select Year', years, key='year_select')
start_time = st.sidebar.time_input('Start Time', datetime.now().time().replace(microsecond=0), key='start_time_key')
end_time = st.sidebar.time_input('End Time', (datetime.now() + timedelta(hours=1)).time().replace(microsecond=0), key='end_time_key')


# Use the user-selected times to define the datetime range
start_datetime = datetime(selected_year, 1, 1, start_time.hour, start_time.minute, start_time.second)
end_datetime = datetime(selected_year, 12, 31, end_time.hour, end_time.minute, end_time.second)

# Define the get_pandas_freq and get_data functions
def get_pandas_freq(interval):
    return {
        '1 minute': 'T',
        '15 minutes': '15T',
        '30 minutes': '30T',
        '1 hour': 'H',
        '1 day': 'D',
        '1 month': 'M',
        '1 year': 'Y'
    }.get(interval, 'D')

def get_data(currency, start, end, interval, year):
    freq = get_pandas_freq(interval)
    start_date = datetime(year, 1, 1)
    end_date = datetime(year, 12, 31)
    dates = pd.date_range(start=start_date, end=end_date, freq=freq)
    prices = np.random.uniform(low=1000, high=2000, size=len(dates))
    return pd.DataFrame({'Time': dates, 'Price': prices})

# Fetch the data
data = get_data(selected_currency, start_datetime, end_datetime, selected_interval, selected_year)

if data is not None:
    # Process and display the data
    data['Price_Scale'] = data['Price'] * 1.5
    chart = alt.Chart(data).mark_line().encode(
        x=alt.X('hoursminutesseconds(EVENT_TIME):T', axis=alt.Axis(format='%H:%M:%S')),
        y='Price_Scale:Q',
        tooltip=['Time:T', 'Price_Scale:Q']
    ).interactive()
    
    st.altair_chart(chart, use_container_width=True)
    st.sidebar.metric("Maximum Price", f"${data['Price'].max():.2f}")
    st.sidebar.metric("Minimum Price", f"${data['Price'].min():.2f}")
else:
    st.error("No data available to display the chart.")

# Download orginal DataSet
csv = df.to_csv(index = False).encode('utf-8')
st.download_button('Download Data', data = csv, file_name = "TABLE_10_11_ETHUSDT.csv",mime = "text/csv")
# Create a line chart
#     line_chart = (
#         Line()
#         .add_xaxis(event_time)
#         .add_yaxis("PRICE", prices)
#         .add_yaxis("QUANTITY", quantities)
#         .set_global_opts(title_opts=opts.TitleOpts(title="Line Chart of PRICE and QUANTITY over Time"))
#     )

#     # Display the chart with Streamlit
#     st_pyecharts(line_chart)

# # Check if all required columns exist in the dataframe
# required_columns = ["EVENT_TYPE", "EVENT_TIME", "SYMBOL", "TRADE_ID", "PRICE", "QUANTITY", "BUYER_ORDER_ID", "SELLER_ORDER_ID", "TRADE_TIME", "IS_BUYER_MARKET_MAKER"]
# missing_columns = [col for col in required_columns if col not in df.columns]
# if missing_columns:
#     st.error(f"The dataframe is missing the following required columns: {', '.join(missing_columns)}")
#     st.stop()
