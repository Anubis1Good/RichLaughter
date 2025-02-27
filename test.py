import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import json
from utils.draw_utils import draw_lite_chart,draw_chart_channel,draw_hb_chart,draw_bollinger,draw_dynamics,draw_rails
from ForBots.Indicators.classic_indicators import add_donchan_channel,add_vangerchik,add_sma, add_slice_df,add_bollinger,add_over_bb,add_attached_bb,add_big_volume,add_dynamics_ma
df_fast = pd.read_csv('DataForTests\DataFromTicksBitget\DOGEUSDT_15m_from_ticks.csv')

multiplier = 15
period = 2
df_fast =add_donchan_channel(df_fast,period)
df_fast['cm'] = df_fast['ms'].apply(lambda ms: ms//(1000*60*multiplier))
df_fast = add_slice_df(df_fast,period)
df_fast.info()
with open('test.json') as f:
    data = json.load(f)

longs = list(data[1])
shorts = list(data[2])
closes = list(data[3])
longs = np.array(longs) - [period,0]
shorts = np.array(shorts) - [period,0]
closes = np.array(closes) - [period,0]
# equity = np.array(equity)
# def change_time(d):
#     d_0 = -1
#     try:
#         cm = d[0]//(1000*60*multiplier)
#         df_fast_slice = df_fast[df_fast['cm'] == cm]
#         d_0 = df_fast_slice.iloc[0].name + period
#     except:
#         print(d)
#         print(df_fast_slice)
#     return np.array([d_0,d[1]])

# longs = np.array(list(map(change_time,longs)))
# shorts = np.array(list(map(change_time,shorts)))
# closes = np.array(list(map(change_time,closes)))
print(longs)
df_fast.apply(draw_hb_chart,axis=1)
draw_chart_channel(df_fast)
if len(longs.shape) > 1:
    plt.scatter(longs[:,0],longs[:,1],marker='^')
if len(shorts.shape) > 1:
    plt.scatter(shorts[:,0],shorts[:,1],marker='v')
if len(closes.shape) > 1:
    plt.scatter(closes[:,0],closes[:,1],marker='x')
plt.show()