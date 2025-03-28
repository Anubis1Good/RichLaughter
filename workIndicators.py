import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from Loader.BitgetLoader import bitget_loader
from utils.draw_utils import draw_lite_chart,draw_chart_channel,draw_hb_chart_fast,draw_bollinger,draw_dynamics,draw_rails
from ForBots.Indicators.classic_indicators import *
from ForBots.Indicators.vsa_indicators import *
from ForBots.Indicators.rare_indicators import *

raw_file = 'DataForTests\DataFromBitget\DOGEUSDT_1m_1739873922.csv'
period = 10
df = bitget_loader(raw_file)
# df = df.iloc[:200]
df = add_donchan_channel(df,10)
# Верхняя полоса (максимум за последние N периодов)
period=5
# df['max_hb'] = df['high'].rolling(window=period).max().rolling(window=period).mean()

# # Нижняя полоса (минимум за последние N периодов)
# df['min_hb'] = df['low'].rolling(window=period).min().rolling(window=period).mean()

# # Средняя линия
# df['avarege'] = (df['max_hb'] + df['min_hb']) / 2
df = add_ema(df,200)
df = add_rsi(df,10)
df = add_slice_df(df,14)
print(df.tail())
plt.subplot(2,1,1)
plt.grid() 
draw_hb_chart_fast(df)
for k in ('ema',):
    plt.plot(df[k],color='r',linestyle='--')
# for k in 'PP, R1, R2, S1, S2'.split(', '):
#     plt.plot(df[k],color='g')
for k in 'max_hb, min_hb, avarege'.split(', '):
    plt.plot(df[k],color='b')
# for k in df.columns:
#     if  'zigzag' in k:
#         plt.plot(df[k])
ax1 = plt.gca()
plt.subplot(2,1,2,sharex=ax1)
plt.grid() 

plt.plot(df['rsi'])
plt.show()