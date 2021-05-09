import streamlit as st
import numpy as np
import pandas as pd 
import plotly.express as px
from datetime import datetime

st.set_page_config(layout="wide")
st.image('aime.png', width=150)

st.title("Malaysia")

state = ['Johor',	'Kedah',	'Kelantan',	'Melaka',	'NS'	,'Pahang',	'Penang',	'Perak',	'Perlis',	'Sarawak',	'Sabah'	,'Selangor',	'Terengganu',	'KL',	'Putrajaya',	'Labuan',	'Malaysia']
state_pop =[3776600,	2193900,	1904900,	936900,	1135900	,1682200,	1783600,	2518600,	255000,	2828700,	3907500,	6569500	,1259000,	1773900,108900,	99600	,32700000]


df = pd.read_excel("data_Arvinder.xlsx", sheet_name="Sheet1")
df = df.loc[:, ~df.columns.str.contains('^Unnamed')] 
df.Date = pd.to_datetime(df.Date)
df = df[df['Date']< (pd.to_datetime("today") + pd.DateOffset(days=3))]

df_s2 = pd.read_excel("data_Arvinder.xlsx", sheet_name="Sheet2")
df_s2 = df_s2.loc[:, ~df_s2.columns.str.contains('^Unnamed')] 
df_s2.Date = pd.to_datetime(df_s2.Date)
df_s2 = df_s2[df_s2['Date']< (pd.to_datetime("today") + pd.DateOffset(days=3))]

state = ['Johor',	'Kedah',	'Kelantan',	'Melaka',	'NS'	,'Pahang',	'Penang',	'Perak',	'Perlis',	'Sarawak',	'Sabah'	,'Selangor',	'Terengganu',	'KL',	'Putrajaya',	'Labuan',	'Malaysia']
state_pop =[3776600,	2193900,	1904900,	936900,	1135900	,1682200,	1783600,	2518600,	255000,	2828700,	3907500,	6569500	,1259000,	1773900,108900,	99600	,32700000]

df_new = df[['Date', 'Malaysia daily new vaccinated', 'Daily 1st dose','Daily 2nd dose', 'Malaysia Daily New Cases', 'Malaysia Daily New Active Cases','Malaysia Daily New Death','Malaysia per 100k vaccinated (7d average)','Malaysia Daily New Death 2020', 'Malaysia Daily New Cases 2020']]

df_new = df_new.copy()

df_new['Malaysia per 1m Daily 1st Dose'] = df_new.loc[:,'Daily 1st dose']/32700000 * 1000000
df_new['Malaysia per 1m Daily 2nd Dose'] = df_new.loc[:,'Daily 2nd dose']/32700000 * 1000000
df_new['Malaysia per 1m New Cases'] = df_new.loc[:,'Malaysia Daily New Cases']/32700000 * 1000000
df_new['Malaysia per 1m New Active Cases'] = df_new.loc[:,'Malaysia Daily New Active Cases']/32700000 * 1000000
df_new['Malaysia per 1m New Death'] = df_new.loc[:,'Malaysia Daily New Death']/32700000 * 1000000
df_new['Malaysia per 1m New Vaccinated'] = df_new.loc[:,'Malaysia daily new vaccinated']/32700000 * 1000000 
df_new['Malaysia per 1m New Vaccinated'] = df_new['Malaysia per 1m New Vaccinated'].shift(periods=14)
df_new['Malaysia per 1m New Cases 2020'] = df_new.loc[:,'Malaysia Daily New Cases 2020']/32700000 * 1000000 
df_new['Malaysia per 1m New Death 2020'] = df_new.loc[:,'Malaysia Daily New Death 2020']/32700000 * 1000000

df_new['Malaysia per 1m Daily 1st Dose (7d average)'] = df_new['Malaysia per 1m Daily 1st Dose'].rolling(window=7).mean()
df_new['Malaysia per 1m Daily 2nd Dose (7d average)'] = df_new['Malaysia per 1m Daily 2nd Dose'].rolling(window=7).mean()
df_new['Malaysia per 1m New Cases (7d average)'] = df_new['Malaysia per 1m New Cases'].rolling(window=7).mean()
df_new['Malaysia per 1m New Active Cases (7d average)'] = df_new['Malaysia per 1m New Active Cases'].rolling(window=7).mean()
df_new['Malaysia per 1m New Death (7d average)'] = df_new['Malaysia per 1m New Death'].rolling(window=7).mean() 
df_new['Malaysia per 1m New Vaccinated (7d average)'] = df_new['Malaysia per 1m New Vaccinated'].rolling(window=7).mean() 
df_new['Malaysia per 1m New Cases 2020 (7d average)'] = df_new['Malaysia per 1m New Cases 2020'].rolling(window=7).mean() 
df_new['Malaysia per 1m New Death 2020 (7d average)'] = df_new['Malaysia per 1m New Death 2020'].rolling(window=7).mean() 

variable = ['Date',
 'Malaysia per 1m Daily 1st Dose (7d average)',
 'Malaysia per 1m Daily 2nd Dose (7d average)',
 'Malaysia per 1m New Cases (7d average)',
 'Malaysia per 1m New Active Cases (7d average)',
 'Malaysia per 1m New Death (7d average)',
 'Malaysia per 1m New Vaccinated (7d average)',
 'Malaysia per 1m New Cases 2020 (7d average)',
 'Malaysia per 1m New Death 2020 (7d average)']
variable.remove('Date')
df_long = pd.melt(df_new, id_vars=['Date'], value_vars= variable)
df_long.columns=['Date','Variables','Count']
df_long['Log(Count)'] = np.log(df_long.Count) 

fig1 = px.line(df_long, x="Date", y="Count", color="Variables", title='Malaysia per 1m Daily New Cases, Death, Vaccinated (7d average)', 
            labels=dict(value="Count"), template="none", width=1200, height=700)
fig1.update_layout(legend=dict(
        yanchor="top",
        y=0.99,
        xanchor="left",
        x=0.01))
st.plotly_chart(fig1,use_container_width=True)


fig2 = px.line(df_long, x="Date", y="Log(Count)", color="Variables", title='Malaysia per 1m Daily New Cases, Death, Vaccinated (Log 7d average)', 
            labels=dict(value="Log(Count)"), template="none", width=1200, height=600)
fig2.update_layout(legend=dict(
        font = dict(size = 10, color = "black"),
        yanchor="top",
        y=0.99,
        xanchor="left",
        x=0.01))
st.plotly_chart(fig2,use_container_width=True)

st.title("State")

State_name = st.selectbox('Select the State',('Johor','Kedah','Kelantan','Melaka','NS','Pahang','Penang','Perak','Perlis','Sarawak','Sabah','Selangor','Terengganu','KL','Putrajaya','Labuan'), key = "new")

df_State = df[['Date', State_name + ' daily vaccinated']]
df_State_s2 = df_s2[['Date',State_name, 'Death in ' + State_name ]]
df_State_final = pd.merge(df_State, df_State_s2, on=['Date']) 

df_State_final[State_name + ' per 100K New Cases'] = df_State_final.loc[:, State_name]/ state_pop[state.index(State_name)] * 100000
df_State_final[State_name + ' per 100K New Death'] = df_State_final.loc[:,'Death in '+ State_name]/state_pop[state.index(State_name)] * 100000
df_State_final[State_name + ' per 100K New Vaccinated'] = df_State_final.loc[:, State_name + ' daily vaccinated']/state_pop[state.index(State_name)] * 100000
df_State_final[State_name + ' per 100K New Vaccinated'] = df_State_final[State_name + ' per 100K New Vaccinated'].shift(periods=14)


df_State_final[State_name + ' per 100K New Cases (7d average)'] = df_State_final[State_name + ' per 100K New Cases'].rolling(window=7).mean()
df_State_final[State_name + ' per 100K New Death (7d average)'] = df_State_final[State_name + ' per 100K New Death'].rolling(window=7).mean()
df_State_final[State_name + ' per 100K New Vaccinated (7d average)'] = df_State_final[State_name + ' per 100K New Vaccinated'].rolling(window=7).mean()

variable = ['Date',
            State_name +' daily vaccinated', State_name, 'Death in '+ State_name,
            State_name +' per 100K New Cases', State_name+ ' per 100K New Death',
            State_name +' per 100K New Cases (7d average)',
            State_name +' per 100K New Death (7d average)',
            State_name +' per 100K New Vaccinated (7d average)']
variable.remove('Date')
df_long_State = pd.melt(df_State_final, id_vars=['Date'], value_vars= variable)
df_long_State.columns=['Date','Variables','Count'] 
df_long_State['Log(Count)'] = np.log(df_long_State.Count)

fig_state = px.line(df_long_State, x="Date", y="Count", color="Variables", title=State_name + ' per 1m Daily New Cases, Death, Vaccinated (7d average)', 
            labels=dict(value="Count"), template="none", width=1200, height=800)
fig_state.update_layout(legend=dict(
        yanchor="top",
        y=0.99,
        xanchor="left",
        x=0.01))
st.plotly_chart(fig_state,use_container_width=True)

fig_state_log = px.line(df_long_State, x="Date", y="Log(Count)", color="Variables", title=State_name + ' per 1m Daily New Cases, Death, Vaccinated (Log 7d average)', 
            labels=dict(value="Log(Count)"), template="none", width=1200, height=800)
fig_state_log.update_layout(legend=dict(
        yanchor="top",
        y=0.99,
        xanchor="left",
        x=0.01))
st.plotly_chart(fig_state_log,use_container_width=True)