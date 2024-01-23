# ilgrim@bi-node1:/data/works/codes/neiron4_model_ML$ timedatectl
#                Local time: Tue 2023-11-07 21:14:52 UTC
#            Universal time: Tue 2023-11-07 21:14:52 UTC
#                  RTC time: n/a
#                 Time zone: Etc/UTC (UTC, +0000)
# System clock synchronized: yes
#               NTP service: inactive
#           RTC in local TZ: no
# pilgrim@bi-node1:/data/works/codes/neiron4_model_ML$ 

# # Display max and min values in the sidebar
#         if selected_column:
#             max_value = filtered_df[selected_column].max()
#             min_value = filtered_df[selected_column].min()
#             color = "blue"
#             font_size = "16px"
#             st.sidebar.markdown(f"<h1 style='color: {color}; font-size: {font_size};'>Maximum {selected_column}: {max_value}</h1>", unsafe_allow_html=True)
#             st.sidebar.markdown(f"<h1 style='color: {color}; font-size: {font_size};'>Minimum {selected_column}: {min_value}</h1>", unsafe_allow_html=True)

# {
#   "$schema": "https://vega.github.io/schema/vega-lite/v5.json",
#   "data": {"values": [{"x": "2010-06-09T00:05:00+00:00"}]},
#   "hconcat": [
#     {
#       "mark": "rule",
#       "encoding": {
#         "x": {"type": "ordinal", "field": "x", "timeUnit": "utchoursminutes"}
#       },
#       "title": "Ordinal"
#     },
#     {
#       "mark": "rule",
#       "encoding": {
#         "x": {"type": "temporal", "field": "x", "timeUnit": "utchoursminutes"}
#       },
#       "title": "Temporal"
#     }
#   ]
# }

# def create_interactive_bar_chart(filtered_df, selected_column):
#     # Filter the dataframe based on selected times
#     filtered_df['QUANTITY'] = filtered_df['QUANTITY']
#     # Set up the selection interaction
#     click = alt.selection_multi(fields=['SYMBOL'])

#     # Define the bar chart
#     bars = alt.Chart(filtered_df).mark_bar().encode(
#         x=alt.X('count()', title='Number of Trades'),
#         y=alt.Y('SYMBOL:N', title='Currency Symbol'),
        
#         color=alt.condition(click, 'SYMBOL:N', alt.value('lightgray')),
#         tooltip=[alt.Tooltip('count()', title='Number of Trades'), 'SYMBOL:N']
#     ).add_selection(
#         click
#     ).properties(
#         title=f"Trade Counts for {selected_column} within Selected Time Range",
#         background='grey', width=950, height=600
#     ).configure_view(
#         strokeOpacity=0
#     ).configure_axis(
#         gridColor='grey',
#         titleColor='white',
#         labelColor='white',
#         tickColor='white'
#     ).configure_title(
#         color='white'
#     )

#     # Display the bar chart in Streamlit
#     st.altair_chart(bars, use_container_width=True)

#     return bars  # Return the bar chart object

# with tab2:
#             st.subheader(f"Bar Chart  {selected_currency}")
#             # Create an interactive bar chart
#             interactive_bar_chart = create_interactive_bar_chart(filtered_df, selected_currency)

# def main():
#     # Initialize the menu at the start of the main function
#     with st.sidebar:
#         selected = option_menu("Menu", ["Home", 'Settings'], 
#                                icons=['house', 'gear'], default_index=0)
#     if selected == "Home":
#         st.write("Home is where the heart is.")
#     elif selected == "Settings":
#         st.write("Adjust your settings here.")
    
# # First file uploader
# uploaded_file_1 = st.sidebar.file_uploader("Upload FIRST CSV", type=["csv", "txt", "xlsx", "xls"], key='file_uploader_1')
# # Second file uploader
# uploaded_file_2 = st.sidebar.file_uploader("Upload SECOND CSV", type=["csv", "txt", "xlsx", "xls"], key='file_uploader_2')
# # In the main function, pass a unique suffix to each call of generate_file_processing_ui
# if uploaded_file_1 is not None:
#     df1 = pd.read_csv(uploaded_file_1, encoding="ISO-8859-1")
#     df1_processed = generate_file_processing_ui(df1, 'FIRST CSV', '1')

# if uploaded_file_2 is not None:
#     df2 = pd.read_csv(uploaded_file_2, encoding="ISO-8859-1")
#     df2_processed = generate_file_processing_ui(df2, 'SECOND CSV', '2')










# import datetime
# import pytz

# # For a naive datetime object
# naive_dt = datetime.datetime.now()
# # Localize the naive datetime object to the system's local timezone
# local_dt = datetime.datetime.now(datetime.timezone.utc).astimezone().tzinfo

# print(f"The system's local timezone is: {local_dt}")


# import datetime
# import pytz

# # If you have a timezone-aware datetime object
# aware_dt = datetime.datetime.now(pytz.timezone('US/Eastern'))

# print(f"The timezone of aware_dt is: {aware_dt.tzinfo}")


# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# df = read_and_process_file(uploaded_file)

# if df is not None:
#     st.write(df)
    
#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!


# import streamlit as st
# import pandas as pd
# import altair as alt
# import datetime
# import numpy as np
# import warnings

# warnings.filterwarnings('ignore')

# # Set up the page configuration
# st.set_page_config(page_title="BINANCE", page_icon=":bar_chart:", layout="wide")

# # Title and custom styles
# st.title(":bar_chart: BINANCE")
# st.markdown('<style>div.block-container{padding-top:1rem;}</style>', unsafe_allow_html=True)

# def upload_file():
#     """Handles the file upload process in the sidebar."""
#     return st.sidebar.file_uploader("Upload a file", type=["csv", "txt", "xlsx", "xls"], key='file_uploader')





















# import streamlit as st
# import plotly.express as px
# import os
# import warnings
# warnings.filterwarnings('ignore')
# from datetime import datetime, time
# import plotly.figure_factory as ff
# from pyecharts import options as opts
# from pyecharts.charts import Line
# from streamlit_echarts import st_pyecharts
# import pandas as pd
# from pyecharts.charts import Bar
# import plotly.graph_objects as go
# import altair as alt

# # Check if all required columns exist in the dataframe
# required_columns = ["EVENT_TYPE", "EVENT_TIME", "SYMBOL", "TRADE_ID", "PRICE", "QUANTITY", "BUYER_ORDER_ID", "SELLER_ORDER_ID", "TRADE_TIME", "IS_BUYER_MARKET_MAKER"]
# missing_columns = [col for col in required_columns if col not in df.columns]
# if missing_columns:
#     st.error(f"The dataframe is missing the following required columns: {', '.join(missing_columns)}")
#     st.stop()

# # Getting the min and max date range
# startDate = df["EVENT_TIME"].min().date()
# endDate = df["EVENT_TIME"].max().date()

# # Create columns for the date and time selections
# col_date1, col_hour1, col_min1, col_sec1, col_date2, col_hour2, col_min2, col_sec2 = st.columns(8)

# # Start date input
# with col_date1:
#     date1 = st.date_input("Start Date", startDate)

# # Start hour selection
# with col_hour1:
#     hour1 = st.selectbox("Start Hour", range(24), format_func=lambda x: f'{x:02d}')

# # Start minute selection
# with col_min1:
#     minute1 = st.selectbox("Start Minute", range(60), format_func=lambda x: f'{x:02d}')

# # Start second selection
# with col_sec1:
#     second1 = st.selectbox("Start Second", range(60), format_func=lambda x: f'{x:02d}')

# # End date input
# with col_date2:
#     date2 = st.date_input("End Date", endDate)

# # End hour selection
# with col_hour2:
#     hour2 = st.selectbox("End Hour", range(24), index=23, format_func=lambda x: f'{x:02d}')  # default to the last hour of the day

# # End minute selection
# with col_min2:
#     minute2 = st.selectbox("End Minute", range(60), index=59, format_func=lambda x: f'{x:02d}')  # default to the last minute of the hour

# # End second selection
# with col_sec2:
#     second2 = st.selectbox("End Second", range(60), index=59, format_func=lambda x: f'{x:02d}')  # default to the last second of the minute

# # Combine date and time selections into datetime objects
# start_datetime = pd.to_datetime(f'{date1} {hour1}:{minute1}:{second1}')
# end_datetime = pd.to_datetime(f'{date2} {hour2}:{minute2}:{second2}')

# # Filter the dataframe based on the datetime range
# df_filtered = df[(df["EVENT_TIME"] >= start_datetime) & (df["EVENT_TIME"] <= end_datetime)]

# # Function to update and display the chart
# def update_chart(dataframe):
#     # Prepare the data
#     event_time = dataframe['EVENT_TIME'].dt.strftime('%H:%M:%S').tolist()
#     prices = dataframe['PRICE'].tolist()
#     quantities = dataframe['QUANTITY'].tolist()

#     # Create a line chart
#     line_chart = (
#         Line()
#         .add_xaxis(event_time)
#         .add_yaxis("PRICE", prices)
#         .add_yaxis("QUANTITY", quantities)
#         .set_global_opts(title_opts=opts.TitleOpts(title="Line Chart of PRICE and QUANTITY over Time"))
#     )

#     # Display the chart with Streamlit
#     st_pyecharts(line_chart)

# # Call update_chart function whenever a selection is made
# update_chart(df_filtered)


# import streamlit as st
# import datetime
# import pandas as pd
# import numpy as np
# import altair as alt
# from datetime import datetime, timedelta
# import warnings
# warnings.filterwarnings('ignore')

# st.set_page_config(page_title="BINANCE", page_icon=":bar_chart:",layout="wide")

# st.title(" :bar_chart: BINANCE")
# st.markdown('<style>div.block-container{padding-top:1rem;}</style>',unsafe_allow_html=True)

# # File uploader widget - add a unique key to the widget
# uploaded_file = st.file_uploader("Upload a file", type=["csv", "txt", "xlsx", "xls"], key='file_uploader')


# def read_and_process_file(uploaded_file):
#     if uploaded_file is not None:
#         try:
#             # Use the file size to check if the file is empty
#             if uploaded_file.size > 0:
#                 # Read the file based on extension
#                 if uploaded_file.name.lower().endswith('.csv'):
#                     df = pd.read_csv(uploaded_file)
#                 elif uploaded_file.name.lower().endswith(('.xlsx', '.xls')):
#                     df = pd.read_excel(uploaded_file)
#                 elif uploaded_file.name.lower().endswith('.txt'):
#                     df = pd.read_csv(uploaded_file, delimiter='\t')
                
#                 # Ensure 'EVENT_TIME' is a datetime column
#                 df['EVENT_TIME'] = pd.to_datetime(df['EVENT_TIME'])
#                 return df
#             else:
#                 st.error("Uploaded file is empty.")
#                 return None
#         except Exception as e:
#             st.error(f"An error occurred while reading the file: {e}")
#             return None
#     else:
#         st.info("Please upload a file to visualize the data.")
#         return None

# # Function to get unique currencies from the dataframe
# def get_unique_currencies(df):
#     if df is not None and 'SYMBOL' in df.columns:
#         return df['SYMBOL'].unique().tolist()
#     return []

# # Define your list of currencies and intervals
# years = [2020, 2021, 2022, 2023, 2024]
# currencies = ['ETHUSDT', 'ETHBTC', 'BTCUSDT', 'BNBETH', 'EOSETH', 'LTCBTC']
# intervals = ['1 minute', '15 minutes', '30 minutes', '1 hour', '1 day', '1 month', '1 year']


# # Define the get_pandas_freq and get_data functions before they are called
# def get_pandas_freq(interval):
#     return {
#         '1 minute': 'T',
#         '15 minutes': '15T',
#         '30 minutes': '30T',
#         '1 hour': 'H',
#         '1 day': 'D',
#         '1 month': 'M',
#         '1 year': 'Y'
#     }.get(interval, 'D')

# def get_data(currency, start, end, interval, year):
#     freq = get_pandas_freq(interval)
#     start_date = datetime(year, 1, 1)
#     end_date = datetime(year, 12, 31)
#     dates = pd.date_range(start=start_date, end=end_date, freq=freq)
#     prices = np.random.uniform(low=1000, high=2000, size=len(dates))
#     return pd.DataFrame({'Time': dates, 'Price': prices})

# # Sidebar selections
# selected_year = st.sidebar.selectbox('Select Year', years, key='year_select')

# selected_currency = st.sidebar.selectbox('Select Currency', currencies, key='currency_select')
# selected_interval = st.sidebar.selectbox('Select Interval', intervals, key='interval_select')


# # Define the start and end times using the sidebar time inputs
# start_time = st.sidebar.time_input('Start Time', datetime.now().time().replace(microsecond=0), key='start_time_key')
# end_time = st.sidebar.time_input('End Time', (datetime.now() + timedelta(hours=1)).time().replace(microsecond=0), key='end_time_key')

# # Use the user-selected times to define the datetime range
# start_datetime = datetime(selected_year, 1, 1, start_time.hour, start_time.minute, start_time.second)
# end_datetime = datetime(selected_year, 12, 31, end_time.hour, end_time.minute, end_time.second)

# # Fetch the data
# data = get_data(selected_currency, start_datetime, end_datetime, selected_interval, selected_year)

# def get_time_values(interval):
#     if interval == '1 minute':
#         return [(f'{i:02d}:{j:02d}') for i in range(24) for j in range(0, 60, 1)]
#     elif interval == '15 minutes':
#         return [(f'{i:02d}:{j:02d}') for i in range(24) for j in range(15, 60, 15)]
#     elif interval == '30 minutes':
#         return [(f'{i:02d}:{j:02d}') for i in range(24) for j in range(30, 60, 30)]
#     elif interval == '1 hour':
#         return [(f'{i:02d}:00') for i in range(24) for j in range(1, 24, 24)]
#     else:
#         return ['00:00', '00:01']  # default


# def create_chart(df, selected_currency, selected_interval, start_datetime, end_datetime):
#     # Define the interval mapping inside the function
#     interval_mapping = {
#         '1 minute': 'T',
#         '15 minutes': '15T',
#         '30 minutes': '30T',
#         '1 hour': 'H',
#         '1 day': 'D',
#         '1 month': 'M',
#         '1 year': 'Y'
#     }
#     # Convert EVENT_TIME to datetime if it's not already
#     df['EVENT_TIME'] = pd.to_datetime(df['EVENT_TIME'])
    
#     # Ensure the dates range between the start and end datetime
#     df = df[(df['EVENT_TIME'] >= start_datetime) & (df['EVENT_TIME'] <= end_datetime)]

#     # Resample the DataFrame
#     resampled_df = df.resample(interval_mapping[selected_interval], on='EVENT_TIME')['PRICE'].mean().reset_index()

#     # Create the chart using the resampled DataFrame
#     chart = alt.Chart(resampled_df).mark_line().encode(
#         x=alt.X('hoursminutesseconds(EVENT_TIME):T', axis=alt.Axis(format='%H:%M:%S')),
#         y=alt.Y('PRICE:Q', axis=alt.Axis(title='Price'), scale=alt.Scale(zero=False)),
#         tooltip=['EVENT_TIME:T', 'PRICE:Q']
#     ).interactive().properties(
#         title='Cryptocurrency Prices Over Time'
#     )

#     return chart

# def get_time_inputs(selected_interval):
#     time_values = get_time_values(selected_interval)
#     start_time = st.sidebar.selectbox('Start Time', time_values, index=0)
#     end_time = st.sidebar.selectbox('End Time', time_values, index=1, key='end_time')
#     return pd.to_datetime(start_time).time(), pd.to_datetime(end_time).time()

# # Initialize the dataframe
# df = None

# # Check if a file has been uploaded
# if uploaded_file is not None:
#     # Read and process the uploaded file
#     df = read_and_process_file(uploaded_file)

#     # If the dataframe is successfully created, check for required columns
#     if df is not None:
#         # Define required columns
#         required_columns = [
#             "EVENT_TYPE", "EVENT_TIME", "SYMBOL", "TRADE_ID", "PRICE", "QUANTITY",
#             "BUYER_ORDER_ID", "SELLER_ORDER_ID", "TRADE_TIME", "IS_BUYER_MARKET_MAKER"
#         ]
#         # Check for missing columns in the dataframe
#         missing_columns = [col for col in required_columns if col not in df.columns]
#         # If there are missing columns, display an error and stop execution
#         if missing_columns:
#             st.error(f"The dataframe is missing the following required columns: {', '.join(missing_columns)}")
#             st.stop()  # Stop execution if required columns are missing

#         # Update the list of currencies based on the uploaded data
#         currencies = get_unique_currencies(df)
#         selected_currency = st.sidebar.selectbox('Select Currency', currencies, key='select_currency_updated')

#             # Define the start_datetime and end_datetime based on the uploaded file's EVENT_TIME column
#         start_date = df['EVENT_TIME'].min().date()
#         end_date = df['EVENT_TIME'].max().date()
#         start_datetime = datetime.combine(start_date, datetime.min.time())
#         end_datetime = datetime.combine(end_date, datetime.max.time())
#             # Filter the dataframe for the selected currency and within the date range
#         df_filtered = df[
#             (df['SYMBOL'] == selected_currency) &
#             (df['EVENT_TIME'].dt.date >= start_date) &
#             (df['EVENT_TIME'].dt.date <= end_date)
#         ]
#         # Find the maximum and minimum prices
#         max_price = df_filtered['PRICE'].max()
#         min_price = df_filtered['PRICE'].min()
#         # Display maximum and minimum prices
#         st.sidebar.metric("Maximum Price", f"${max_price:.2f}")
#         st.sidebar.metric("Minimum Price", f"${min_price:.2f}")

# # Now call create_chart with the correct datetime objects
# chart = create_chart(df_filtered, selected_currency, selected_interval, start_datetime, end_datetime)
# st.altair_chart(chart, use_container_width=True)


# # Debug print statements
        # st.write("Selected currency:", selected_currency)
        # st.write("Selected start time:", selected_start_time)
        # st.write("Selected end time:", selected_end_time)

# # Debug print statements
        # st.write("Start datetime:", start_datetime)
        # st.write("End datetime:", end_datetime)

 # # Debug print statements
        # st.write("Filtered DataFrame shape:", df_filtered.shape)
        # #st.write(df_filtered.head())

 # # Debug print statements
        # st.write("Maximum price:", max_price)
        # st.write("Minimum price:", min_price)
