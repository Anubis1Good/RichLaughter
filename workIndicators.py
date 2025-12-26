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
from scipy.stats import linregress

# raw_file = 'DataForTests\DataFromBitget\DOGEUSDT_1m_1739873922.csv'
# raw_file = 'DataForTests\DataFromMOEX\MMM5_1_1749581140.csv'
# raw_file = 'DataForTests\DataFromMoexFast\\5IMOEXF_1_1752761086.csv'
raw_file = 'DataForTests\DataMoexFut5P\_5IMOEXF_1_1766374056.parquet'
# raw_file = 'DataForTests\oldMoex\SiM5_1_1745579847.csv'
period = 10
df = simple_load_df(raw_file)
# df = df.iloc[-200:]
# df = df.iloc[10:510]


df = add_sma(df)

for i in range(1,5):
    df['top_'+str(i)] = df['sma'] + df['close'] * i * 0.002
    df['bot_'+str(i)] = df['sma'] - df['close'] * i * 0.002

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
use_sublot2 = False

if plot:
    if use_sublot2:
        plt.subplot(2,1,1)
    plt.grid() 
    draw_hb_chart_fast(df)

    for col in df.columns.to_list():
        if 'top_' in col:
            plt.plot(df[col],color='green')
        if 'bot_' in col:
            plt.plot(df[col],color='pink')
    plt.plot(df['sma'])
    # plt.plot(df['upper_channel'])
    # plt.plot(df['ave_up'])
    # plt.plot(df['ave_down'])
    # plt.plot(df['max_hb'])
    # plt.plot(df['min_hb'])
    # plt.plot(df['stop_up'])
    # plt.plot(df['stop_down'])
    # plt.plot(df['lower_channel'])
    # plt.plot(df['sma'])
    # plt.plot(df['top_mean'])
    # plt.plot(df['bottom_mean'])
    # plt.plot(df['top_pd'])
    # plt.plot(df['bottom_pd'])
    # plt.plot(df['stair'])
    # plt.plot(df['hbzz'])
    # plt.plot(df['lbzz'])
    # plt.plot(df['zigzag'])
    # plt.plot(df['lsl'])
    # plt.plot(df['ssl'])
    # plt.plot(df['bzp1'], linestyle=':',color='g')
    # plt.plot(df['bzp2'], linestyle='-.',color='g')
    # plt.plot(df['bzp3'], linestyle=':',color='b')
    # plt.plot(df['bzp4'], linestyle='-.',color='b')
    # plt.plot(df['zp1'], linestyle=':',color='g')
    # plt.plot(df['zp2'], linestyle='-.',color='g')
    # plt.plot(df['zp3'], linestyle=':',color='b')
    # plt.plot(df['zp4'], linestyle='-.',color='b')
    # plt.plot(df['target'], linestyle='--',color='r')
    # plt.plot(df['btarget'], linestyle='--',color='r')
    # plt.plot(df['mzp'], linestyle='--',color='#ff00ff')

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
    if use_sublot2:
        ax1 = plt.gca()
        plt.subplot(2,1,2,sharex=ax1)
        plt.grid() 
    # plt.plot(df['dir_ma'])
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