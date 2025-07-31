import streamlit as st
import pandas as pd
from load_data import load_data

players = load_data()

st.sidebar.image('images/fifa.jpg')

st.title("Find Players")

with st.container():
     form = st.form('Find Player')
country, budget, height, age = "", 0, 0, 0
with form:
     country = st.multiselect('Select A Country', options=players['country'].unique())
     budget = st.number_input("Enter Maximum Value", min_value=players['value'].min(), max_value=players['value'].max())
     height = st.slider("Enter Height", min_value=players['height'].min(), max_value=players['height'].max(), key=1)
     age = st.slider("Enter Age", min_value=players['age'].min(), max_value=players['age'].max(), key=2)
     st.form_submit_button('Submit', icon='⚽', use_container_width=True)
# st.text(f"{country}, {budget}, {height}, {age}")
import duckdb
con = duckdb.connect()
df = con.query(f'select * from players where (country in {country}) and (value <= {budget}) and (age <= {age}) and (height >= {height})').df()

st.subheader('Players You Needed to See:')
st.dataframe(df)#.iloc[:10, :])