import pandas as pd
import numpy as np
import sqlite3
# df = pd.read_csv('DataForTests\otherMOEX\SBERF_search_problems.csv', sep=',', header=0, index_col=0)
# df['Объем'] = np.where(df['Операция'] == 'Продажа',df['Объем'],-df['Объем'])
# df.info()
# print(df['Цена'].head())
# df['first_volume'] = df.groupby('Инструмент')['Объем'].transform('first')
# df['total'] = df['Объем'] - df['first_volume']
# # print(df_1)
# print(df.head())
# print(df.tail())
# df_2 = df.groupby('Инструмент')['Объем'].sum()
# print(df_2)
# print(df_2-df.groupby('Инструмент')['Кол-во'].sum()*2)

# q = '''
# SELECT * FROM history_positions
# WHERE robot_id = 198
#   AND ticker_id = 7
#   AND open_timestamp BETWEEN '2025-12-25 00:00:00' AND '2025-12-28 23:59:59'
# '''

# conn = sqlite3.connect('dbs\\test_MOEX_FUT.db')
# df = pd.read_sql_query(q,conn)
# df.info()
# print(df[['open_timestamp','close_timestamp','direction','open_price','close_price','result']])
# print(df['result'].sum())