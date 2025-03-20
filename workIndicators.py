import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from Loader.BitgetLoader import bitget_loader
from utils.draw_utils import draw_lite_chart,draw_chart_channel,draw_hb_chart,draw_bollinger,draw_dynamics,draw_rails
from ForBots.Indicators.classic_indicators import *
from ForBots.Indicators.vsa_indicators import *
from ForBots.Indicators.rare_indicators import *

raw_file = 'DataForTests\DataFromBitget\DOGEUSDT_1m_1739873922.csv'
period = 10
df = bitget_loader(raw_file)
df = df.iloc[:200]
df = calculate_zigzag(df)
# df = add_adaptive_channel(df)
df = add_slice_df(df,14)
print(df.tail())
plt.subplot(2,1,1)
df.apply(draw_hb_chart,axis=1)
for k in df.columns:
    if  'zigzag' in k:
        plt.plot(df[k])
plt.subplot(2,1,2)
# plt.plot(df[ 'chaikin_volatility'])
plt.show()