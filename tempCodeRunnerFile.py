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