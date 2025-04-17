import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from Loader.BitgetLoader import bitget_loader
from utils.draw_utils import draw_lite_chart,draw_chart_channel,draw_hb_chart_fast,draw_bollinger,draw_dynamics,draw_rails
from ForBots.Indicators.classic_indicators import *
from ForBots.Indicators.vsa_indicators import *
from ForBots.Indicators.rare_indicators import *
from scipy.stats import linregress

raw_file = 'DataForTests\DataFromBitget\DOGEUSDT_1m_1739873922.csv'
raw_file = 'DataForTests\DataFromMOEX\MMM5_1_1744615735.csv'
period = 10
df = bitget_loader(raw_file)
df = df.iloc[-200:]
# df = df.iloc[10:500]


import numpy as np
import pandas as pd

def add_hl_stair_fast(df: pd.DataFrame, n=3, period=20):
    df = df.copy()
    high = df['high'].values
    low = df['low'].values

    # Предварительные расчеты
    spread = high - low
    threshold_break = pd.Series(spread).rolling(period).mean().fillna(0).values * n

    # Инициализация массивов
    size = len(df)
    last_dir = np.ones(size, dtype=np.int8)
    last_high = np.zeros(size)
    last_low = np.zeros(size)

    # Начальные значения
    last_high[0] = high[0]
    last_low[0] = low[0]

    # Основной цикл
    for i in range(1, size):
        current_dir = last_dir[i-1]
        current_high = last_high[i-1]
        current_low = last_low[i-1]
        th = threshold_break[i]
        h = high[i]
        l = low[i]

        if current_dir == 1:
            new_high = max(h, current_high)
            if l <= (new_high - th):
                current_dir = -1
                new_low = l
            else:
                new_low = current_low
        else:
            new_low = min(l, current_low)
            if h >= (new_low + th):
                current_dir = 1
                new_high = h
            else:
                new_high = current_high

        last_dir[i] = current_dir
        last_high[i] = new_high
        last_low[i] = new_low

    # Отмечаем точки разворота
    dir_changes = np.diff(last_dir, prepend=0) != 0
    df['stair'] = np.where(dir_changes, np.where(last_dir == -1, high, low), np.nan)
    
    # Заполняем значения вперед
    df['stair'] = df['stair'].ffill()
    return df



# Пример использования
# df = pd.read_csv('your_data.csv')
df = add_hl_stair_fast(df, n=5)
df['stair_s'] = df['stair'].rolling(100).mean()
# print(df[['high', 'low', 'direction', 'last_extreme']].head())


print(df.tail())
# plt.subplot(2,1,1)
draw_hb_chart_fast(df)
plt.plot(df['stair'])
plt.plot(df['stair_s'])
# plt.plot(df['last_high'])
# plt.plot(df['last_low'])
# for k in ('fractal_up_high', 
#         'fractal_down_low',
#         'fractal_up_middle',
#         'fractal_down_middle',
#         'fractal_middle'):
#     plt.plot(df[k])
# for k in 'max_hb, min_hb, avarege'.split(', '):
# ax1 = plt.gca()
# plt.subplot(2,1,2,sharex=ax1)
# plt.plot(df['regression_angle'])
# # plt.plot(df['li'])
# plt.plot(df['market_mode'])

# plt.grid() 

# for k in ( 'trend_up','trend_down'):
# # for k in 'PP, R1, R2, S1, S2'.split(', '):
# #     plt.plot(df[k],color='g')
# for k in 'max_hb, min_hb, avarege'.split(', '):
#     plt.plot(df[k],color='b')
# for k in df.columns:
#     if  'zigzag' in k:
#         plt.plot(df[k])
# for k in 'trend_up_slope, trend_down_slope'.split(', '):
# for k in ('regression_slope',):
# plt.plot(df['rsi'])
plt.show()