import pandas as pd 

raw_file = 'DataForTests\DataFromBitget\DOGEUSDT_5m_1754235321.csv'
df = pd.read_csv(raw_file)
df['ms'] = pd.to_datetime(df['ms'], unit='ms')
# Если нужен строковый формат (не datetime)
df['ms'] = df['ms'].dt.strftime('%Y-%m-%d %H:%M:%S')
df = df.drop('Unnamed: 0',axis=1)
df.info()
print(df.head())
print(df.tail())
df.to_csv('DataForTests\DataFromBitget\DOGEUSDT_5m_100000.csv')