import pandas as pd

players = pd.read_csv('data/cleaned.csv')

x = players.select_dtypes(include=['int64','float64']).drop(columns=['value'])
y = players['value']

from sklearn.preprocessing import StandardScaler
scaler = StandardScaler()
scaled = scaler.fit_transform(x)
y = y/10000000

from sklearn.model_selection import train_test_split
x_train, x_test, y_train, y_test = train_test_split(scaled, y, test_size=0.3, random_state=42)

from sklearn.ensemble import RandomForestRegressor
model = RandomForestRegressor()
model.fit(x_train, y_train)

y_pred = model.predict(x_test)

from sklearn.metrics import mean_squared_error, r2_score
print(mean_squared_error(y_test, y_pred))
print(r2_score(y_test, y_pred))

from joblib import dump
dump(scaler, 'model/scaler')
dump(model, 'model/RFR.pkl')

df = pd.DataFrame()
df['y_test'] = y_test
df['y_pred'] = y_pred
print(df)