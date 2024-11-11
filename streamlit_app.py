import streamlit as st
from datetime import datetime, timedelta
import pandas as pd
from plotly import express as px

st.set_page_config(page_title='Time Left', page_icon='⌚️')
st.title('⌚️ Time Left')
st.caption('Understand how much time is left and how much time has passed in the current quarter and year 📊')

todays_date = datetime.now().date()

current_quarter = (todays_date.month - 1) // 3 + 1
start_of_quarter = todays_date.replace(day=1, month=(current_quarter - 1) * 3 + 1)
start_of_year = todays_date.replace(day=1, month=1)

if current_quarter == 4:
    end_of_quarter = start_of_quarter.replace(day=1, month=1, year=start_of_quarter.year + 1) - timedelta(days=1)
else:
    end_of_quarter = start_of_quarter.replace(day=1, month=start_of_quarter.month + 3) - timedelta(days=1)
end_of_year = todays_date.replace(day=31, month=12)

days_to_end_of_quarter = (end_of_quarter - todays_date).days
days_to_end_of_year = (end_of_year - todays_date).days

days_from_start_of_quarter = (todays_date - start_of_quarter).days
days_from_start_of_year = (todays_date - start_of_year).days

days_in_quarter = (end_of_quarter - start_of_quarter).days + 1
days_in_year = (end_of_year - start_of_year).days + 1

days_left_in_quarter = days_in_quarter - days_from_start_of_quarter
days_left_in_year = days_in_year - days_from_start_of_year

pct_of_quarter = days_from_start_of_quarter / days_in_quarter
pct_of_year = days_from_start_of_year / days_in_year

pct_left_in_quarter = days_left_in_quarter / days_in_quarter
pct_left_in_year = days_left_in_year / days_in_year

with st.expander('Time Left in Quarter 🪙', expanded=True):
    df = pd.DataFrame([])
    df['Days'] = [days_from_start_of_quarter, days_left_in_quarter]
    df['Name'] = ['Days Passed', 'Days Left']
    df['Percentage'] = [pct_of_quarter, pct_left_in_quarter]
    df[' '] = ''
    df['Days and Percent'] = df['Days'].astype(str) + ' days (' + (df['Percentage'] * 100).astype(int).astype(str) + '%)'
    df['Days and Percent'] = [
        str(round(pct_of_quarter * 100)) + '% done ✅ (' + str(days_from_start_of_quarter) + 'd)',
        str(round(pct_left_in_quarter * 100)) + '% left ⏳ (' + str(days_left_in_quarter) + 'd)'
    ]

    p = px.bar(
        df, 
        y=' ', 
        x='Percentage', 
        text='Days and Percent', 
        title='Time ⏳ Left in Quarter', 
        color='Name',
        category_orders={'Name': ['Days Passed', 'Days Left']},
        orientation='h',
        height=250
    )
    p.update_xaxes(tickvals=[0, 0.25, 0.5, 0.75, 1], tickformat=',.0%')
    p.update_layout(barmode='stack', showlegend=False)
    st.plotly_chart(p, use_container_width=True)


with st.expander('Time Left in Year 📆', expanded=False):
    df = pd.DataFrame([])
    df['Days'] = [days_from_start_of_year, days_left_in_year]
    df['Name'] = ['Days Passed', 'Days Left']
    df['Percentage'] = [pct_of_year, pct_left_in_year]
    df[' '] = ''

    df['Days and Percent'] = [
        str(round(pct_of_year * 100)) + '% done ✅ (' + str(days_from_start_of_year) + 'd)',
        str(round(pct_left_in_year * 100)) + '% left ⏳ (' + str(days_left_in_year) + 'd)'
    ]

    p = px.bar(
        df, 
        y=' ', 
        x='Percentage', 
        text='Days and Percent', 
        title='Time ⏳ Left in Year', 
        color='Name',
        category_orders={'Name': ['Days Passed', 'Days Left']},
        orientation='h',
        height=250
    )
    p.update_xaxes(tickvals=[0, 0.25, 0.5, 0.75, 1], tickformat=',.0%')
    p.update_layout(barmode='stack', showlegend=False)
    st.plotly_chart(p, use_container_width=True)

st.caption(f"Today's date: `{todays_date}`, End of Quarter: `{end_of_quarter}`, End of Year: `{end_of_year}`")