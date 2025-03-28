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
raw_file = 'DataForTests\DataFromMOEX\MMH5_1_1739993452.csv'
period = 10
df = bitget_loader(raw_file)
df = df.iloc[-50:]
# df = add_dynamic_trend_lines_slope_reversed(df,2,200)
df = add_segmented_regression_from_end(df,60,1)
# df = add_dynamic_trend_lines_extended(df,2,60)
# df = add_donchan_channel(df,10)
# df = add_linear_regression_channel(df,100)
# def calculate_regression(values):
#     x = range(len(values))  # Создаем массив индексов
#     slope, intercept, _, _, _ = linregress(x, values)
#     return slope * x[-1] + intercept  # Возвращаем значение на последней точке

# Применяем линейную регрессию к скользящему окну
# df['regression_middle'] = df['close'].rolling(window=period).apply(calculate_regression, raw=True)
# Верхняя полоса (максимум за последние N периодов)
period=5
# df['max_hb'] = df['high'].rolling(window=period).max().rolling(window=period).mean()

# # Нижняя полоса (минимум за последние N периодов)
# df['min_hb'] = df['low'].rolling(window=period).min().rolling(window=period).mean()

# # Средняя линия
# df['avarege'] = (df['max_hb'] + df['min_hb']) / 2
# df = add_ema(df,200)
# df = add_rsi(df,10)
df = add_slice_df(df,14)
print(df.tail())
plt.subplot(2,1,1)
plt.grid() 
draw_hb_chart_fast(df)
for k in ( 'upper_channel',):
    plt.plot(df[k],color='r',linestyle='--')
for k in ( 'lower_channel',):
    plt.plot(df[k],color='b',linestyle='--')
ax1 = plt.gca()
plt.subplot(2,1,2,sharex=ax1)
plt.grid() 
for k in ('regression_slope',):
    plt.plot(df[k])
# for k in ( 'regression_line','upper_channel','lower_channel'):
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