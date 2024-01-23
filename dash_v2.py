# def create_combined_chart(df1, column1, currency1, df2, column2, currency2):
#     if df1 is None or df1.empty or df2 is None or df2.empty:
#         st.error("One or both DataFrames are empty. Cannot create chart.")
#         return None

#     # Check if columns exist
#     for df, column in [(df1, column1), (df2, column2)]:
#         if column not in df.columns:
#             st.error(f"Column '{column}' not found in the dataframe.")
#             return None

#     # Convert columns to numeric and drop NaNs
#     df1[column1] = pd.to_numeric(df1[column1], errors='coerce')
#     df2[column2] = pd.to_numeric(df2[column2], errors='coerce')
#     df1.dropna(subset=[column1], inplace=True)
#     df2.dropna(subset=[column2], inplace=True)

#     if df1[column1].empty or df2[column2].empty:
#         st.error("Selected columns do not contain numeric data.")
#         return None

#     df1['Value'] = df1[column1]
#     df1['Category'] = f"{currency1} {column1}"
#     df2['Value'] = df2[column2]
#     df2['Category'] = f"{currency2} {column2}"

#     combined_df = pd.concat([df1[['EVENT_TIME', 'Value', 'Category']], df2[['EVENT_TIME', 'Value', 'Category']]], ignore_index=True)

#     zoom = alt.selection_interval(bind='scales', encodings=['x', 'y'])

#     chart = alt.Chart(combined_df).mark_line().encode(
#         x=alt.X('utchoursminutesseconds(EVENT_TIME):T', title='Event Time',
#                 axis=alt.Axis(format='%H:%M:%S', labelFontSize=15, labelColor='white', labelAngle=-90)),
#         y=alt.Y('Value:Q', title='Values', scale=alt.Scale(zero=False)),
#         color=alt.Color('Category:N', scale=alt.Scale(domain=[df1['Category'].iloc[0], df2['Category'].iloc[0]], range=['blue', 'red'])),
#         tooltip=['EVENT_TIME:T', 'Value:Q', 'Category:N']
#     ).add_selection(
#         zoom
#     ).properties(
#         title=f"{currency1} {column1} and {currency2} {column2} Over Time",
#         background='black',
#         width=1950,
#         height=1200
#     ).configure_view(
#         strokeOpacity=0
#     ).configure_axis(
#         gridColor='grey',
#         titleColor='white',
#         labelColor='white',
#         tickColor='white'
#     ).configure_title(
#         color='white',
#         fontSize=20
#     )

#     return chart

# def create_combined_chart(df1, column1, currency1, df2, column2, currency2, show_histogram=True):
#     if df1 is None or df1.empty or df2 is None or df2.empty:
#         st.error("One or both DataFrames are empty. Cannot create chart.")
#         return None

#     # Check if columns exist
#     for df, column in [(df1, column1), (df2, column2)]:
#         if column not in df.columns:
#             st.error(f"Column '{column}' not found in the dataframe.")
#             return None

#     # Convert columns to numeric and drop NaNs
#     df1[column1] = pd.to_numeric(df1[column1], errors='coerce')
#     df2[column2] = pd.to_numeric(df2[column2], errors='coerce')
#     df1.dropna(subset=[column1], inplace=True)
#     df2.dropna(subset=[column2], inplace=True)

#     if df1[column1].empty or df2[column2].empty:
#         st.error("Selected columns do not contain numeric data.")
#         return None

#     df1['Value'] = df1[column1]
#     df1['Category'] = f"{currency1} {column1}"
#     df2['Value'] = df2[column2]
#     df2['Category'] = f"{currency2} {column2}"

#     combined_df = pd.concat([df1[['EVENT_TIME', 'Value', 'Category']], df2[['EVENT_TIME', 'Value', 'Category']]], ignore_index=True)

#     # Create line chart
#     line_chart = alt.Chart(combined_df).mark_line().encode(
#         x=alt.X('utchoursminutesseconds(EVENT_TIME):T', title='Event Time',
#                 axis=alt.Axis(format='%H:%M:%S', labelFontSize=15, labelColor='white', labelAngle=-90)),
#         y=alt.Y('Value:Q', title='Values', scale=alt.Scale(zero=False)),
#         color=alt.Color('Category:N', scale=alt.Scale(domain=[df1['Category'].iloc[0], df2['Category'].iloc[0]], range=['blue', 'red'])),
#         tooltip=['EVENT_TIME:T', 'Value:Q', 'Category:N']
#     ).properties(
#         title=f"{currency1} {column1} and {currency2} {column2} Over Time",
#         background='black',
#         width=1950,
#         height=600
#     ).configure_view(
#         strokeOpacity=0
#     ).configure_axis(
#         gridColor='grey',
#         titleColor='white',
#         labelColor='white',
#         tickColor='white'
#     ).configure_title(
#         color='white',
#         fontSize=20
#     )

#     # Create histogram
#     if show_histogram:
#         histogram = alt.Chart(combined_df).mark_bar().encode(
#             x=alt.X('Value:Q', title='Values', bin=alt.Bin(maxbins=30)),
#             y='count():Q',
#             color='Category:N',
#             tooltip=['Value:Q', 'count()']
#         ).properties(
#             title=f"{currency1} {column1} and {currency2} {column2} Histogram",
#             background='black',
#             width=400,
#             height=300
#         ).configure_view(
#             strokeOpacity=0
#         ).configure_axis(
#             gridColor='grey',
#             titleColor='white',
#             labelColor='white',
#             tickColor='white'
#         ).configure_title(
#             color='white',
#             fontSize=20
#         )

#         # Concatenate line chart and histogram
#         combined_chart = alt.hconcat(line_chart, histogram)

#     else:
#         # If no histogram, return only the line chart
#         combined_chart = line_chart

#     return combined_chart

# def generate_file_processing_ui(df, selected_column, file_label, key_suffix):
#     if df is not None:
#         try:
#             selected_currency = 'USD'  # Default value
#             if 'SYMBOL' in df.columns:
#                 selected_currency = st.sidebar.selectbox('Currency', df['SYMBOL'].unique().tolist(), key=f'currency_select_{key_suffix}')

#             selected_column = st.sidebar.selectbox('Select a column', df.columns, key=f'column_select_{key_suffix}')

#             selected_start_time = selected_end_time = None
#             if 'EVENT_TIME' in df.columns:
#                 df['EVENT_TIME'] = pd.to_datetime(df['EVENT_TIME'], format='%d.%m.%y %H:%M:%S', errors='coerce')
#                 unique_times = df['EVENT_TIME'].dropna().sort_values().unique()
#                 selected_start_time = st.sidebar.selectbox("Start Time", unique_times, key=f'start_time_select_{key_suffix}')
#                 selected_end_time = st.sidebar.selectbox("End Time", unique_times, key=f'end_time_select_{key_suffix}')

#             # Add a checkbox for selecting the chart type (line chart or histogram)
#             chart_type = st.sidebar.checkbox("Show Histogram", key=f'chart_type_checkbox_{key_suffix}', value=False)

#             filtered_df = df.copy()
#             if selected_start_time and selected_end_time:
#                 filtered_df = df[(df['SYMBOL'] == selected_currency) & (df['EVENT_TIME'] >= selected_start_time) & (df['EVENT_TIME'] <= selected_end_time)]

#             if selected_column and selected_column in filtered_df.columns:
#                 max_value = filtered_df[selected_column].max()
#                 min_value = filtered_df[selected_column].min()

#                 # Check if the column is numeric
#                 if pd.api.types.is_numeric_dtype(filtered_df[selected_column]):
#                     max_value = f"{max_value:.4f}"
#                     min_value = f"{min_value:.4f}"
#                 elif pd.api.types.is_datetime64_any_dtype(filtered_df[selected_column]):
#                     min_value = min_value.strftime('%Y-%m-%d %H:%M:%S')
#                     max_value = max_value.strftime('%Y-%m-%d %H:%M:%S')
#                 else:
#                     max_value = str(max_value)
#                     min_value = str(min_value)
#                 color = "blue"
#                 font_size = "16px"
#                 st.sidebar.markdown(f"<h1 style='color: {color}; font-size: {font_size};'>Min/{selected_column}: {min_value}</h1>", unsafe_allow_html=True)
#                 st.sidebar.markdown(f"<h1 style='color: {color}; font-size: {font_size};'>Max/{selected_column}: {max_value}</h1>", unsafe_allow_html=True)

#                 if chart_type:
#                     # Display histogram
#                     histogram_fig = create_combined_chart(filtered_df, selected_column, selected_currency, 'blue', height=800, width=1000, histfunc='percent')
#                     st.plotly_chart(histogram_fig)
#                 else:
#                     # Display line chart
#                     line_chart = create_combined_chart(filtered_df, selected_column, selected_currency, None, None, None)
#                     st.altair_chart(line_chart)

#                 return filtered_df, selected_currency, selected_column, selected_start_time, selected_end_time
#         except Exception as e:
#             st.error(f"Error processing file: {e}")
#             return None, None, None, None, None
#     else:
#         st.error(f"No {file_label} file uploaded. Please upload a file.")
#         return None, None, None, None, None

# def main(selected_panel):
#     st.sidebar.title("Settings")

#     # File upload logic
#     uploaded_file_1 = st.sidebar.file_uploader("Upload FIRST CSV", type=["csv", "txt", "xlsx", "xls"], key='file_uploader_1')
#     uploaded_file_2 = st.sidebar.file_uploader("Upload SECOND CSV", type=["csv", "txt", "xlsx", "xls"], key='file_uploader_2')

#     df1 = df2 = None
#     currency_options1 = currency_options2 = []

#     if uploaded_file_1 is not None:
#         df1 = pd.read_csv(uploaded_file_1)
#         if 'SYMBOL' in df1.columns:
#             currency_options1 = df1['SYMBOL'].unique().tolist()

#     if uploaded_file_2 is not None:
#         df2 = pd.read_csv(uploaded_file_2)
#         if 'SYMBOL' in df2.columns:
#             currency_options2 = df2['SYMBOL']. unique().tolist()

#     # Extract datetime options
#     datetime_options1 = datetime_options2 = []
#     if df1 is not None:
#         df1['EVENT_TIME'] = pd.to_datetime(df1['EVENT_TIME'], errors='coerce')
#         datetime_options1 = sorted(df1['EVENT_TIME'].dropna().unique())

#     if df2 is not None:
#         df2['EVENT_TIME'] = pd.to_datetime(df2['EVENT_TIME'], errors='coerce')
#         datetime_options2 = sorted(df2['EVENT_TIME'].dropna().unique())

#     # Define variables for selected columns and currencies
#     selected_column1 = selected_column2 = currency1 = currency2 = None

#     if selected_panel == "HISTOGRAM":
#         st.write("Histogram Display")
#         if df1 is not None:
#             selected_column1 = st.sidebar.selectbox("Select a column for histogram analysis for First CSV", df1.columns, key='histogram_column1')
#             start_datetime1 = st.sidebar.selectbox("Start DateTime for First CSV", datetime_options1, format_func=lambda x: x.strftime('%Y-%m-%d %H:%M:%S'), key='start_datetime1')
#             end_datetime1 = st.sidebar.selectbox("End DateTime for First CSV", datetime_options1, format_func=lambda x: x.strftime('%Y-%m-%d %H:%M:%S'), key='end_datetime1')
#             histogram_fig1 = create_combined_chart(df1, selected_column1, 'USD', df2, selected_column2, 'EUR', show_histogram=True)
#             st.altair_chart(histogram_fig1)
#         if df2 is not None:
#             selected_column2 = st.sidebar.selectbox("Select a column for histogram analysis for Second CSV", df2.columns, key='histogram_column2')
#             start_datetime2 = st.sidebar.selectbox("Start DateTime for Second CSV", datetime_options2, format_func=lambda x: x.strftime('%Y-%m-%d %H:%M:%S'), key='start_datetime2')
#             end_datetime2 = st.sidebar.selectbox("End DateTime for Second CSV", datetime_options2, format_func=lambda x: x.strftime('%Y-%m-%d %H:%M:%S'), key='end_datetime2')

#             # Use the selected_column2, start_datetime2, and end_datetime2 in create_combined_chart function
#             histogram_fig2 = create_combined_chart(df2, selected_column2, 'EUR', df1, selected_column1, 'USD', show_histogram=True)
#             st.altair_chart(histogram_fig2)


# # ... Rest of your code for CHART and DATA ...

# if __name__ == "__main__":
#     selected_panel = st.sidebar.radio("Select Panel", ['HISTOGRAM', 'CHART', 'DATA'])
#     main(selected_panel)