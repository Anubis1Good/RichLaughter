import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from Loader.BitgetLoader import bitget_loader
from utils.draw_utils import draw_lite_chart,draw_chart_channel,draw_hb_chart,draw_bollinger,draw_dynamics,draw_rails
from ForBots.Indicators.classic_indicators import *
from ForBots.Indicators.vsa_indicators import *


raw_file = 'DataForTests\DataFromBitget\DOGEUSDT_1m_1739873922.csv'
period = 10
df = bitget_loader(raw_file)
df = df.iloc[:200]
df = add_CDV(df)
df = add_rsi(df,14,'cdv')
df = add_slice_df(df,14)
plt.subplot(2,1,1)
df.apply(draw_hb_chart,axis=1)
plt.subplot(2,1,2)
plt.plot(df["rsi"])
plt.show()