import streamlit as st
import numpy as np
import pandas as pd 
import plotly.express as px

st.set_page_config(layout="wide")
st.image('aime.png', width=250)

df = pd.read_excel("data.xlsx", sheet_name="Data Entry")
df = df.loc[:, ~df.columns.str.contains('^Unnamed')]
pop = pd.read_excel("data.xlsx", sheet_name="Pop")
df.Date = pd.to_datetime(df.Date)
df = df[df['Date']< (pd.to_datetime("today") + pd.DateOffset(days=5))]

states = ['Malaysia','Johor','Kedah','Kelantan','Melaka','NS','Pahang','Penang','Perak','Perlis','Sarawak','Sabah','Selangor','Terengganu','KL','Putrajaya','Labuan']

df = df.drop(states,1)

st.title('Daily Vaccine Dose Usages and Information')


for state in states:
    
    state_1st_dose_daily = state + ' 1st dose daily'
    state_2nd_dose_daily = state + ' 2nd dose daily'
    
    state_1st_dose = state + ' 1st dose'
    state_2nd_dose = state + ' 2nd dose'
    
    state_1st_dose_daily_7d_avg = state + ' 1st dose daily 7d average'
    state_2nd_dose_daily_7d_avg = state + ' 2nd dose daily 7d average'
    
    state_1st_dose_daily_7d_avg_100k = state + ' 1st dose daily 7d average per 100k'
    state_2nd_dose_daily_7d_avg_100k = state + ' 2nd dose daily 7d average per 100k'
    
    
    df[state_1st_dose_daily] = df.loc[:,state_1st_dose]-df.loc[:,state_1st_dose].shift(1)
    df[state_2nd_dose_daily] = df.loc[:,state_2nd_dose]-df.loc[:,state_2nd_dose].shift(1) 
    
    df[state_1st_dose_daily_7d_avg] = df[state_1st_dose_daily].rolling(window=7).mean()
    df[state_2nd_dose_daily_7d_avg] = df[state_2nd_dose_daily].rolling(window=7).mean()
    
    df[state_1st_dose_daily_7d_avg_100k] = df[state_1st_dose_daily_7d_avg] / int(pop[state]) * 100000
    df[state_2nd_dose_daily_7d_avg_100k] = df[state_2nd_dose_daily_7d_avg] / int(pop[state]) * 100000

st.dataframe(df)

st.title('Charts')

variable = df.columns.tolist()
variable.remove('Date')
df_long = pd.melt(df, id_vars=['Date'], value_vars= variable)   

col1, col2 = st.beta_columns(2)

with col1:
    state_option = st.selectbox('Select the State',('Malaysia','Johor','Kedah','Kelantan','Melaka','NS','Pahang','Penang','Perak','Perlis','Sarawak','Sabah','Selangor','Terengganu','KL','Putrajaya','Labuan'))

    state_1st_dose_daily = state_option + ' 1st dose daily'
    state_2nd_dose_daily = state_option + ' 2nd dose daily'

    state_1st_dose = state_option + ' 1st dose'
    state_2nd_dose = state_option + ' 2nd dose'

    state_1st_dose_daily_7d_avg = state_option + ' 1st dose daily 7d average'
    state_2nd_dose_daily_7d_avg = state_option + ' 2nd dose daily 7d average'

    state_1st_dose_daily_7d_avg_100k = state_option + ' 1st dose daily 7d average per 100k'
    state_2nd_dose_daily_7d_avg_100k = state_option + ' 2nd dose daily 7d average per 100k'

    filter_list = [state_1st_dose_daily, state_2nd_dose_daily, state_1st_dose, state_2nd_dose, state_1st_dose_daily_7d_avg, state_2nd_dose_daily_7d_avg, state_1st_dose_daily_7d_avg_100k, state_2nd_dose_daily_7d_avg_100k]
    results = df_long[df_long.variable.isin(filter_list)] 
    fig = px.line(results, x="Date", y="value", color="variable", title='1st and 2nd Dose Information', 
                labels=dict(value="Value"), template="none",
                width=1200, height=700)
    fig.update_layout(legend=dict(
        yanchor="top",
        y=0.99,
        xanchor="left",
        x=0.01))

    st.plotly_chart(fig,use_container_width=True)

with col2: 
    state_option2 = st.selectbox('Select the State',('Malaysia','Johor','Kedah','Kelantan','Melaka','NS','Pahang','Penang','Perak','Perlis','Sarawak','Sabah','Selangor','Terengganu','KL','Putrajaya','Labuan'), key = "new")

    state_1st_dose_daily = state_option2 + ' 1st dose daily'
    state_2nd_dose_daily = state_option2 + ' 2nd dose daily'

    state_1st_dose = state_option2 + ' 1st dose'
    state_2nd_dose = state_option2 + ' 2nd dose'

    state_1st_dose_daily_7d_avg = state_option2 + ' 1st dose daily 7d average'
    state_2nd_dose_daily_7d_avg = state_option2 + ' 2nd dose daily 7d average'

    state_1st_dose_daily_7d_avg_100k = state_option2 + ' 1st dose daily 7d average per 100k'
    state_2nd_dose_daily_7d_avg_100k = state_option2 + ' 2nd dose daily 7d average per 100k'

    filter_list = [state_1st_dose_daily, state_2nd_dose_daily, state_1st_dose, state_2nd_dose, state_1st_dose_daily_7d_avg, state_2nd_dose_daily_7d_avg, state_1st_dose_daily_7d_avg_100k, state_2nd_dose_daily_7d_avg_100k]
    results = df_long[df_long.variable.isin(filter_list)] 
    fig2 = px.line(results, x="Date", y="value", color="variable", title='1st and 2nd Dose Information', 
                labels=dict(value="Value"), template="none",
                width=1200, height=700)
    fig2.update_layout(legend=dict(
        yanchor="top",
        y=0.99,
        xanchor="left",
        x=0.01))
    st.plotly_chart(fig2,use_container_width=True)

st.write("The data used in this project is contributed by [Dr. Arvinder Singh HS](https://my.linkedin.com/in/drasinghr)")


