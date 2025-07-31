import pandas as pd
import chardet as cd

with open('data/player_stats.csv', 'rb') as f:
     raw = f.read()
     result = cd.detect(raw)

player_stats = pd.read_csv('data/player_stats.csv', encoding=result['encoding'])

player_stats.dropna(axis=1, inplace=True)

print(player_stats.columns)

duplicates = player_stats.drop_duplicates(subset='player', keep='first', inplace=True)

print(duplicates)

player_stats['value'] = player_stats['value'].str.replace('$', '').str.replace('.', '').astype('int64')

# remove outliers
def remove_outliers(player_stats, column):
     q1 = player_stats[column].quantile(0.25)
     q3 = player_stats[column].quantile(0.75)
     iqr = q3 - q1
     min = q1 - 1.5 * iqr
     max = q3 + 1.5 * iqr
     player_stats = player_stats[(player_stats[column] >= min) & (player_stats[column] <= max)]

# removing outliers
for i in player_stats.select_dtypes(include=['int64', 'float64']).columns:
     remove_outliers(player_stats, i)

from sklearn.preprocessing import LabelEncoder
encoder = LabelEncoder()
player_stats['club_'] = encoder.fit_transform(player_stats['club'])
player_stats.drop(columns='club', inplace=True)
player_stats.rename(columns={'club_':'club'}, inplace=True)
from joblib import dump
dump(encoder, 'model/encoder.pkl')

player_stats.to_csv('data/cleaned.csv', index=False)