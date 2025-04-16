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
# df = df.iloc[-500:]

def add_kvas_channel(df:pd.DataFrame,period=20):
    df['delta_p'] = (df['close'] - df['close'].shift(period))
    df['top_kvas'] = df['high'].rolling(period).max() + df['delta_p']
    df['low_kvas'] = df['low'].rolling(period).min() + df['delta_p']
    return df

def add_kefir_channel(df:pd.DataFrame,period=20):
    df['delta_p'] = df['close'] - df['close'].shift(period)
    df['delta_t'] = df['delta_p'].shift(period).rolling(period).max()
    df['delta_l'] = df['delta_p'].shift(period).rolling(period).min()
    df['top_kefir'] = df['high'].rolling(period).max() + df['delta_t']
    df['low_kefir'] = df['low'].rolling(period).min() + df['delta_l']
    return df



# Пример использования
# df = add_kvas_channel(df,10)
df = add_kefir_channel(df,10)


print(df.tail())
# plt.subplot(2,1,1)
draw_hb_chart_fast(df)
# plt.plot(df['top_kvas'])
# plt.plot(df['low_kvas'])
plt.plot(df['top_kefir'])
plt.plot(df['low_kefir'])
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