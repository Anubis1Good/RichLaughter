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
raw_file = 'DataForTests\DataFromMoexFast\MMM5_1_1749581140.csv'
# raw_file = 'DataForTests\oldMoex\SiM5_1_1745579847.csv'
period = 10
df = bitget_loader(raw_file)
df = df.iloc[-200:]
# df = df.iloc[10:510]



df = add_dzz_picks(df,method='mean',n_std=3)

df = add_dzz_level_channel(df)
# p1v = p1['high'].diff()
# p1i = p1.index.to_series().diff()
# delta_zzt = p1v / p1i
# df['delta_zzt'] = delta_zzt.shift(1) * p1i

# df['delta_zzti'] = p1i.interpolate(method='linear')
# df['delta_zzb'] = p2['low'].diff()
# df['cur_high'] = p1['high']
# df['cur_high'] = df['cur_high'].ffill()
# df['delta_zzt'] = df['delta_zzt'].ffill()
# df['delta_zzti'] = df['delta_zzti'].ffill()
# df['delta_zzt1'] = df['delta_zzt'] * df['delta_zzti']
# df['delta_zzb'] = df['delta_zzb'].ffill()
# df['line1'] = (df['cur_high'] + df['delta_zzt']).interpolate(method='linear')
# df['line1'] = df['cur_high'] + df['delta_zzt1']
# df['line2'] = df['zigzag'] + df['delta_zzb']
# print(df.iloc[:-50].head())
# Пример использования
# df = pd.read_csv('your_data.csv')
# print(df[['high', 'low', 'direction', 'last_extreme']].head())


# plt.subplot(2,1,1)
plt.grid() 
draw_hb_chart_fast(df)
# plt.plot(df['zigzag_line'])
plt.plot(df['upper_channel'])
plt.plot(df['lower_channel'])
# plt.plot(df['line2'])
# plt.plot(df['bottom_line'])
# plt.plot(df['regression_line'])
# plt.plot(df['stair'])
# plt.plot(df['trend'])
plt.plot(df['zigzag'])
# plt.plot(df['stair_up'])
# df['points'] = np.where((df['zigzag_direction'] != df['zigzag_direction'].shift(1)), df['middle'], np.nan)

# points = df[~pd.isna(df['points'])]
# print(points)
# plt.scatter(points.index,points['middle'])
plt.scatter(df.index, df['zigzag_peaks'], color='red', label='Peaks')
# for k in ('fractal_up','fractal_down'):
#     plt.plot(df[k])
# for k in 'max_hb, min_hb, avarege'.split(', '):
# ax1 = plt.gca()
# plt.subplot(2,1,2,sharex=ax1)
# plt.grid() 
# plt.plot(df['delta_zz'])
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