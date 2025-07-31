import pandas as pd
import streamlit as st

@st.cache_data
def load_data():
     players = pd.read_csv('data/cleaned.csv')
     return players

@st.cache_data
def model_training_prediction():
     players = load_data()
     x = players.select_dtypes(include=['int64','float64']).drop(columns=['value'])
     # x = players.select_dtypes(include=['int64','float64']).drop(columns=['value'])
     y = players['value']

     from sklearn.preprocessing import StandardScaler
     scaler = StandardScaler()
     x_scaled = scaler.fit_transform(x)
     y_scaled = y/10000000

     from sklearn.model_selection import train_test_split
     x_train, x_test, y_train, y_test = train_test_split(x_scaled, y_scaled, test_size=0.3, random_state=42)

     from sklearn.ensemble import RandomForestRegressor
     model = RandomForestRegressor()
     model.fit(x_train, y_train)

     y_pred = model.predict(x_test)

     from joblib import dump
     dump(scaler, 'model/scaler.pkl')
     dump(model, 'model/RFR.pkl')

     return x_scaled, y_scaled, x_train, x_test, y_train, y_test, y_pred, x.columns