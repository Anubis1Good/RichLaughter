import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from Loader.BitgetLoader import bitget_loader
from utils.draw_utils import draw_lite_chart,draw_chart_channel,draw_hb_chart_fast,draw_bollinger,draw_dynamics,draw_rails
from ForBots.Indicators.classic_indicators import *
from ForBots.Indicators.vsa_indicators import *
from ForBots.Indicators.rare_indicators import *
from ForBots.Indicators.pva_indicators import *
from scipy.stats import linregress

raw_file = 'DataForTests\DataFromBitget\DOGEUSDT_1m_1739873922.csv'
raw_file = 'DataForTests\DataFromMOEX\MMM5_1_1744615735.csv'
period = 10
df = bitget_loader(raw_file)
# df = df.iloc[-500:]
# df = df.iloc[10:500]

df = add_donchan_channel(df)


    





# Пример использования
# df = pd.read_csv('your_data.csv')
df = add_assessment_motion_index(df)
# print(df[['high', 'low', 'direction', 'last_extreme']].head())


print(df.tail())
plt.subplot(2,1,1)
plt.grid() 
draw_hb_chart_fast(df)
# plt.plot(df['top_line'])
# plt.plot(df['bottom_line'])
# plt.plot(df['center_line'])
# for k in ('fractal_up_high', 
#         'fractal_down_low',
#         'fractal_up_middle',
#         'fractal_down_middle',
#         'fractal_middle'):
for k in 'max_hb, min_hb, avarege'.split(', '):
    plt.plot(df[k])
ax1 = plt.gca()
plt.subplot(2,1,2,sharex=ax1)
plt.grid() 
plt.plot(df['ami'])
plt.plot(df['ami_filter'])
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
plt.show()