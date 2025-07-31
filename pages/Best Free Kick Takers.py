import pandas as pd
import streamlit as st
import duckdb as db
from load_data import load_data

con = db.connect()

players = load_data()

st.sidebar.image('images/ron.jpg')

with st.container():
     st.markdown('### Adjust the Accuracy below and Press Submit')
     st.text('The Players with Free Kick Accuracy higher than wht you selected will be displayed here.')
     form = st.form(key='Best fk')
     with form:
          acc_min = st.slider('Select the __Minimum__ free kick takers accuracy: ', min_value=players['fk_acc'].min(), max_value=players['fk_acc'].max(), key=1)
          acc_max = st.slider('Select the __Maximum__ free kick takers accuracy: ', min_value=players['fk_acc'].min(), max_value=players['fk_acc'].max(),key=2)
          st.form_submit_button('Submit', use_container_width=True)
     if acc_min<=acc_max:
          df = con.execute(f'select * from players where fk_acc >= {acc_min} and fk_acc <= {acc_max}').df()
          st.markdown('The Players with ___Free Kick Accuracy___ >= as you selected above: ')
          df.sort_values(by='fk_acc', ascending=False, inplace=True)
          st.dataframe(df.iloc[:10, :].reset_index().drop(columns=['index']))
     else:
          st.error('Please select _free kick accuracy_ according to the criteria: _min. accuracy <= max. accuracy_')
