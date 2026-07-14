import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from utils.work_with_dataframe.load_df import simple_load_df
from utils.draw_utils import draw_lite_chart,draw_chart_channel,draw_hb_chart_fast,draw_bollinger,draw_dynamics,draw_rails
from ForBots.Indicators.classic_indicators import *
from ForBots.Indicators.vsa_indicators import *
from ForBots.Indicators.rare_indicators import *
from ForBots.Indicators.pva_indicators import *
from ForBots.Indicators.van_indicators import *
from ForBots.Indicators.ml_indicators import *
from ForBots.Indicators.mult_indicators import *
from scipy.stats import linregress


raw_file = 'DataForTests\DataMoexStockP\ROSN_1_1783336759.parquet'

period = 10
df = simple_load_df(raw_file)
# df = df.iloc[-200:]
# df = df.iloc[10:510]

# df['spred'] = df['high'] - df['low']
# df['impuls'] = df['spred'].rolling(20).mean()
# df['flow'] = (df['impuls']*df['direction']).rolling(20).sum()
df.info()


# df = add_dzz_peaks(df,period=10,n_std=5)
# df = add_dzz_peaks(df,period=10,n_std=5,drop_last=False)



# df = add_mean_dzz_peaks(df)
# df = add_plusdelta_dzz_peaks(df)
# df = add_exp_plusdelta_dzz_peaks(df)
# df = add_pattern18_dzz_czd(df)
# Вычисляем текущий диапазон
# df = add_stop_loss_p18czd(df)
# df = add_rsi(df)

# df = add_quantile_params(df,100)
# df = add_sma(df)
# df = add_donchan_channel(df)
# df = add_integrity_index(df)
# df = add_stable_ma_direction(df)
print(df.tail(10))
# df.info()


plot = True
# plot = False
use_sublot2 = True
# use_sublot2 = False

if plot:
    if use_sublot2:
        plt.subplot(2,1,1)
    plt.grid() 
    draw_hb_chart_fast(df)

    # for col in df.columns.to_list():
    #     if 'top_' in col:
    #         plt.plot(df[col],color='green')
    #     if 'bot_' in col:
    #         plt.plot(df[col],color='pink')


    if use_sublot2:
        ax1 = plt.gca()
        plt.subplot(2,1,2,sharex=ax1)
        plt.grid() 

    # plt.plot(df['flow'],color='r')
    # plt.hl
    # plt.plot(df['signal_line'],color='b')
    # plt.plot(df['cum_dvsai'])
    # plt.plot(df['ma_cdv1'])
    # plt.plot(df['ma_cdv2'])
    # plt.plot(df['crysis_index'],color='g')
    # plt.plot(df['rsi'],color='r')
    # plt.plot(df['ii'])
    # plt.plot(df['rsi'])
    # plt.plot(df['top_q'])
    # plt.plot(df['bottom_q'])

    # plt.bar(df.index.to_series(),df['dvsai'])
    # plt.plot(df['chaikin_volatility'],color='red')
    # plt.plot(df['spred'],color='red')
    # plt.plot(df['spred_max'],color='blue')
    # plt.plot(df['spred_ma'],color='green')
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
    df.to_csv('test.csv')
    plt.show()