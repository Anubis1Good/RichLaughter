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

# raw_file = 'DataForTests\DataFromBitget\DOGEUSDT_1m_1739873922.csv'
# raw_file = 'DataForTests\DataFromMOEX\MMM5_1_1749581140.csv'
raw_file = 'DataForTests\DataFromMoexFast\\5MMU5_1_1752761082.csv'
# raw_file = 'DataForTests\oldMoex\SiM5_1_1745579847.csv'
period = 10
df = bitget_loader(raw_file)
df = df.iloc[-200:]
# df = df.iloc[10:510]

# df['down_diff'] = df['low'] - df['sma']
# df = add_dzz_peaks(df,period=10)
df = add_fractals(df,10)

# df = add_plus_delta_fc(df,10)
df = add_exp_pdfc(df,10)
# df = add_chaikin_volatility(df)
# df = add_analys_dzz(df)
print(df.tail(10))
# df.info()


plot = True
# plot = False
if plot:
    plt.subplot(2,1,1)
    plt.grid() 
    draw_hb_chart_fast(df)
    # plt.plot(df['upper_channel'])
    plt.plot(df['pdf_up'])
    plt.plot(df['pdf_down'])
    # plt.plot(df['lower_channel'])
    # plt.plot(df['top_line'])
    # plt.plot(df['bottom_line'])
    # plt.plot(df['regression_line'])
    # plt.plot(df['stair'])
    # plt.plot(df['trend'])
    # plt.plot(df['zigzag'])
    # plt.plot(df['stair_up'])
    # df['points'] = np.where((df['zigzag_direction'] != df['zigzag_direction'].shift(1)), df['middle'], np.nan)

    # points = df[~pd.isna(df['points'])]
    # print(points)
    # plt.scatter(points.index,points['middle'])
    # plt.scatter(df.index, df['zigzag_peaks'], color='red', label='Peaks')
    # for k in ('fractal_up','fractal_down'):
    # for k in (('max_hb', 'min_hb', 'avarege')):
    #     plt.plot(df[k])
    # for k in 'max_hb, min_hb, avarege'.split(', '):

    ax1 = plt.gca()
    plt.subplot(2,1,2,sharex=ax1)
    plt.grid() 
    # plt.bar(df.index.to_series(),df['dvsai'])
    # plt.plot(df['chaikin_volatility'],color='red')
    # plt.plot(df['dvsaid'],color='red')
    # plt.plot(df['cum_dvsai'])
    # plt.plot(df['ma_cdv1'])
    # plt.plot(df['ma_cdv2'])
    # plt.plot()
    # plt.plot(df['bottom_mean'])
    # plt.plot(df['trend'])
    # plt.plot(df['trend_sma'])
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
    
    plt.show()