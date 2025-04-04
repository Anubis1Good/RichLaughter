import sys
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
bot_id = 140
# start = str(date.today() - timedelta(days=2))
# end = None

# print(df.head())
db_path = 'dbs/test_MOEX_FUT.db'


# 2. Загрузка сделок из базы данных
def load_trades(db_path, bot_id, ticker):
    conn = sqlite3.connect(db_path)
    query = '''
    SELECT hp.open_timestamp, hp.close_timestamp, hp.open_price, hp.close_price, 
           hp.direction as dir_pos, hp.result, hp.fee, hp.result_fee, t.name as ticker
    FROM history_positions hp
    JOIN tickers t ON hp.ticker_id = t.id
    WHERE hp.robot_id = ? AND t.name = ?
    ORDER BY hp.open_timestamp
    '''
    df_trades = pd.read_sql(query, conn, params=(bot_id, ticker))
    conn.close()
    
    # Конвертируем timestamp в datetime
    df_trades['open_timestamp'] = pd.to_datetime(df_trades['open_timestamp'])
    df_trades['close_timestamp'] = pd.to_datetime(df_trades['close_timestamp'])
    
    df_trades['open_timestamp'] = df_trades['open_timestamp'].dt.floor('min')
    df_trades['close_timestamp'] = df_trades['close_timestamp'].dt.floor('min')

    return df_trades

df_trades = load_trades(db_path, bot_id, ticker)
if df_trades.empty:
    print('нет сделок')
    sys.exit(0)
start = df_trades['open_timestamp'].min().date()
end = df_trades['close_timestamp'].max().date()
df = download_moex(ticker,1,start=start,end=end,board=board,market=market,engine=engine)
df = create_df(df)
# df = df.set_index('ms')  # Устанавливаем время как индекс
# df.index = pd.to_datetime(df.index)
df['ms'] = pd.to_datetime(df['ms'])

df = df.merge(
    df_trades[['open_timestamp', 'open_price','dir_pos']],
    left_on='ms',
    right_on='open_timestamp',
    how='left'
)
df = df.merge(
    df_trades[['close_timestamp', 'close_price']],
    left_on='ms',
    right_on='close_timestamp',
    how='left'
)

df['dir_pos'] = np.where(~pd.isna(df['close_price'])&(pd.isna(df['open_price'])), 0, df['dir_pos'])

df['dir_pos'] = df['dir_pos'].ffill()

df['longs'] = np.where((df['dir_pos'] == 1)&(df['dir_pos'].shift(1) != 1), df['open_price'], np.nan)

df['longs'] = np.where((df['dir_pos'] != 1)&(df['dir_pos'].shift(1) == 1), df['close_price'], df['longs'])

mask = (df['dir_pos'] == 1) | (df['dir_pos'].shift(1) == 1)
df.loc[mask, 'longs'] = df.loc[mask, 'longs'].interpolate(method='linear')

df['shorts'] = np.where((df['dir_pos'] == -1)&(df['dir_pos'].shift(1) != -1), df['open_price'], np.nan)

df['shorts'] = np.where((df['dir_pos'] != -1)&(df['dir_pos'].shift(1) == -1), df['close_price'], df['shorts'])

mask = (df['dir_pos'] == -1) | (df['dir_pos'].shift(1) == -1)
df.loc[mask, 'shorts'] = df.loc[mask, 'shorts'].interpolate(method='linear')

# print(df[~pd.isna(df['longs'])])
# df.info()
# sys.exit(0)

draw_hb_chart_fast(df)
# Фильтруем данные для сделок на покупку (dir_pos == 1)
# Покупки (dir_pos == 1)
buy_open = df[(~df['open_price'].isna()) & (df['dir_pos'] == 1)]
buy_close = df[(~df['close_price'].isna()) & (df['dir_pos'].shift(1) == 1)]

# Продажи (dir_pos == -1)
sell_open = df[(~df['open_price'].isna()) & (df['dir_pos'] == -1)]
sell_close = df[(~df['close_price'].isna()) & (df['dir_pos'].shift(1) == -1)]

# Маркеры открытия
plt.scatter(
    buy_open.index, buy_open['open_price'],
    marker='^', color='green',  label='Покупка (открытие)'
)
plt.scatter(
    sell_open.index, sell_open['open_price'],
    marker='v', color='red',  label='Продажа (открытие)'
)

# Маркеры закрытия
plt.scatter(
    buy_close.index, buy_close['close_price'],
    marker='x', color='blue',  label='Закрытие (покупка)'
)
plt.scatter(
    sell_close.index, sell_close['close_price'],
    marker='x', color='purple',  label='Закрытие (продажа)'
)

plt.plot(df['longs'],linestyle='--',color='g')
plt.plot(df['shorts'],linestyle='--',color='b')

plt.show()