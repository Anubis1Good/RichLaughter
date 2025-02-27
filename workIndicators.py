import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from Loader.BitgetLoader import bitget_loader
from utils.draw_utils import draw_lite_chart,draw_chart_channel,draw_hb_chart,draw_bollinger,draw_dynamics,draw_rails
from ForBots.Indicators.classic_indicators import *

raw_file = 'DataForTests\DataFromBitget\DOGEUSDT_1m_1739873922.csv'
period = 10
df = bitget_loader(raw_file)
df = df.iloc[:100]

df['spread'] = df['high'] - df['low']

# Вычисление среднего объема и спреда
df['avg_volume'] = df['volume'].rolling(window=20).mean()
df['avg_spread'] = df['spread'].rolling(window=20).mean()

# df = add_stochastic(df)
df = add_slice_df(df,period)
plt.subplot(2,1,1)
# df.apply(draw_hb_chart,axis=1)
# df = add_fractals(df)
plt.plot(df['avg_volume'],color='blue')
plt.subplot(2,1,2)
plt.plot(df['avg_spread'],color='green')
# print(df.tail())
# draw_chart_channel(df,'top_mean', 'bottom_mean', 'avarege_mean')

plt.show()