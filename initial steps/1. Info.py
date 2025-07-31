import pandas as pd
import chardet

with open('data/player_stats.csv', 'rb') as f:
     raw = f.read()
     result = chardet.detect(raw)

player_stats = pd.read_csv('data/player_stats.csv', encoding=result['encoding'])

print(player_stats.describe())

print(player_stats.isnull().sum())