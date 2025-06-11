import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from Loader.BitgetLoader import bitget_loader
from utils.draw_utils import draw_lite_chart,draw_chart_channel,draw_hb_chart_fast,draw_bollinger,draw_dynamics,draw_rails
from ForBots.Indicators.classic_indicators import *
from ForBots.Indicators.vsa_indicators import *
from ForBots.Indicators.rare_indicators import *
from ForBots.Indicators.pva_indicators import *
from ForBots.Indicators.van_indicators import *
from ForBots.Indicators.ml_indicators import *
from scipy.stats import linregress

raw_file = 'DataForTests\DataFromBitget\DOGEUSDT_1m_1739873922.csv'
raw_file = 'DataForTests\DataFromMOEX\MMM5_1_1749581140.csv'
# raw_file = 'DataForTests\oldMoex\SiM5_1_1745579847.csv'
period = 10
df = bitget_loader(raw_file)
df = df.iloc[-200:]
# df = df.iloc[10:510]
df = add_fractals(df,20)
up_points = df[df['fractal_up']]
df['ave_up'] = up_points['high'].rolling(window=3).mean()
df['ave_up'] = df['ave_up'].ffill()
down_points = df[df['fractal_down']]
df['ave_down'] = down_points['low'].rolling(window=3).mean()
df['ave_down'] = df['ave_down'].ffill()
# df = add_segmented_regression_from_end(df)
# df = add_dynamic_trend_lines_slope_reversed(df)

# Пример использования
# df = pd.read_csv('your_data.csv')
# print(df[['high', 'low', 'direction', 'last_extreme']].head())


# plt.subplot(2,1,1)
plt.grid() 
draw_hb_chart_fast(df)
# plt.plot(df['zigzag_line'])
# plt.plot(df['top_line'])
# plt.plot(df['bottom_line'])
# plt.plot(df['regression_line'])
# plt.plot(df['stair'])
plt.plot(df['ave_up'])
plt.scatter(up_points['x'], up_points['high'], 
            color='green', marker='^',  
            label='Fractal Up')
plt.plot(df['ave_down'])
plt.scatter(down_points['x'], down_points['low'], 
            color='blue', marker='v',  
            label='Fractal Down')
# for k in ('fractal_up','fractal_down'):
#     plt.plot(df[k])
# for k in 'max_hb, min_hb, avarege'.split(', '):
# ax1 = plt.gca()
# plt.subplot(2,1,2,sharex=ax1)
# plt.grid() 
# plt.plot(df['ami'])
# plt.plot(df['ami_filter'])
# plt.plot(df['ii'])
# plt.plot(df['market_mode'])


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
print(df.tail())
plt.show()