import sys
import os
import sqlite3
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from request_functions.download_moex import download_moex,create_df
from utils.draw_utils import draw_hb_chart_fast
board = "RFUD"
market = "forts"
engine= "futures"
ticker = 'MMM5'
ticker = 'CRM5'
# ticker = 'SiM5'
bot_id = 73
granularity = '1'
# start = str(date.today() - timedelta(days=2))
# end = None

# print(df.head())
db_path = 'dbs/test_MOEX_FUT.db'


# 2. Загрузка сделок из базы данных
def load_trades(db_path, bot_id, ticker):
    conn = sqlite3.connect(db_path)
    query = '''
        SELECT 
            hp.robot_id,
            hp.close_timestamp,
            hp.result_fee,
            SUM(hp.result_fee) OVER (
                PARTITION BY hp.robot_id 
                ORDER BY hp.close_timestamp 
                ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
            ) AS cumulative_return
        FROM 
            history_positions hp
        JOIN tickers t ON hp.ticker_id = t.id
        WHERE hp.robot_id = ? AND t.name = ?
        ORDER BY 
            hp.close_timestamp;
    '''
    df_trades = pd.read_sql(query, conn, params=(bot_id, ticker))
    conn.close()
    
    return df_trades

conn = sqlite3.connect(db_path)
cursor = conn.cursor()
query = '''
    SELECT 
        id,
        name
    FROM 
        robots
    WHERE granularity=?

'''
cursor.execute(query, (granularity,))
robots = cursor.fetchall()
conn.close()

folder_img = './TestOtTrades/cumulative_results_plots/AllTime/'
if not os.path.exists(folder_img):
    os.makedirs(folder_img)
    print('...')
for bot_id,name in robots:
    df_trades = load_trades(db_path, bot_id, ticker)
    if df_trades.empty:
        print(name,'нет сделок')
        continue


    plt.plot(df_trades['cumulative_return'])
    filepath = os.path.join(folder_img,ticker+'__'+name+'.png')
    plt.savefig(filepath)
    plt.close()