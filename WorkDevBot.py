import sys
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import numpy.typing as npt
from time import time
from Loader.BitgetLoader import bitget_loader
from utils.work_with_dataframe.convert_timeframe import convert_timeframe
from utils.draw_utils import draw_lite_chart,draw_chart_channel,draw_hb_chart,draw_bollinger,draw_dynamics,draw_rails,draw_hb_chart_fast
# from ForBots.Indicators.classic_indicators import add_donchan_channel,add_vangerchik,add_sma, add_slice_df,add_bollinger,add_over_bb,add_attached_bb,add_big_volume,add_dynamics_ma
from strategies.test_strategies.check import check_strategy,check_strategy_v3_LSC,check_strategy_v4,check_strategy_v5,check_strategy_realistic_v1
from strategies.work_strategies.HelpTA import get_rws
# from strategies.work_strategies.PTA import PTA2_DDCrWork as WS
# from strategies.work_strategies.PTAX import PTA10_WIZARD as WS
# from strategies.work_strategies.PTAXX import PTA23_ULTIMATUM as WS
# from strategies.work_strategies.STA_ca import STA3_LITE as WS
# from strategies.work_strategies.GLTA import GLTA2_ALPHA as WS
# from strategies.work_strategies.GLTA import GLTA2_BETA as WS
# from strategies.work_strategies.GLTA import GLTA2_GAMMA as WS
# from strategies.work_strategies.OGTA import OGTA7_PARADOX as WS
# from strategies.work_strategies.LTA import LTA_CC as WS
# from strategies.work_strategies.LTA2 import LTA2_DRG as WS
# from strategies.work_strategies.PSTA0 import PSTA6_SHERIFF as WS
from strategies.work_strategies.VSAT import VSAT1_b as WS
# from strategies.work_strategies.PSTA0 import PSTA8_ as WS
# from strategies.work_strategies.MTA import MTA_LORD as WS
# from strategies.work_strategies.STA_ml2 import STAML2a_PHENOMENON as WS
# from strategies.work_strategies.STA_ml import STAML1_XGBR2_DC as WS
# from strategies.work_strategies.STA_rl import STARL1_HELPGOD as WS
# from strategies.work_strategies.experiments import ExpBot as WS


# raw_file = 'DataForTests\DataFromMoexForStepTests\EDU5_1_1753990596.csv'
raw_file = 'DataForTests\DataFromMoexForStepTests\MMU5_1_1753990575.csv'


longs = []
shorts = []
closes = []
start = time()

df = bitget_loader(raw_file)
df = convert_timeframe(df,'5min')
period = 20
multiplier = 2
symbol = "DOGEUSDT"
granularity = "5m"
close_2330 = True
close_2330 = False
slope = 4
# bot = WS(symbol,granularity,'e',1,100,7,10,10,40,10,0)
# WS = get_rws(WS)
print(WS)
bot = WS(symbol,granularity,'e',1)
# bot = WS(symbol,granularity,'e',1,22,4,1.99)
# bot = WS(symbol,granularity,'e',1,20,10,'LP_1752352674.json')
# bot = WS(symbol,granularity,'e',1,25,9,12,'QGA20_beta2_001.json')
# bot = WS(symbol,granularity,'e',1,30,100,30,60,30,50,'LP_1752353219.json')
# bot = WS(symbol,granularity,'e',1,30,100,30,60,30,50,policy='BP_1751841463.6270704.json')
# trades,equity3,equity_fee = check_strategy_v5(df.copy(),bot,close_2330=True)
# print(trades)
# trades,equity1,equity_fee,longs1,shorts1,closes1 = check_strategy_v4(df.copy(),bot)
# print(trades)
# print(trades)
# trades,equity,equity_fee = check_strategy_v5(df,bot)
# conf = (20,55,12,25,20)
# bot = WS(symbol,granularity,"usdt-futures",1,*conf)
# df = df.iloc[-50:]
# df = bot.get_test_df(df)
# df.info()
# print(df.tail()['chop'])
# print(time() - start)
# sys.exit()



# fee_base = 0.0004
# fee_base = 0.0012
fee_base = 0.0002
df = bot.preprocessing(df)
# trades,equity,equity_fee,longs,shorts,closes= check_strategy_v3_LSC(df.copy(),bot,fee_base,close_2330=True)
trades,equity,equity_fee,longs,shorts,closes= check_strategy_realistic_v1(df.copy(),bot,fee_base,close_2330=close_2330)
# trades,longs,shorts,closes,equity = check_strategy(df,get_action_STA1e,bot)
# trades,equity2,equity_fee = check_strategy_v3(df,bot,fee_base)
# print(trades)
# trades,longs,shorts,closes,equity = check_strategy(df,TS,bot)
print(trades)
# try:
#     fee = trades['count']*trades['open_price']*fee_base
#     print('fee',fee, (fee/trades['open_price'])*100)
#     print('total_with_fee',trades['total'] - fee, ((trades['total'] - fee)/trades['open_price'])*100)
# except:
#     print('НЕТ СДЕЛОК!')



# longs = np.array(longs)
# shorts = np.array(shorts)
# closes = np.array(closes)
# equity = np.array(equity)

# print(longs.shape,longs1.shape)
# print(shorts.shape,shorts1.shape)
# print(closes.shape,closes1.shape)

see_equity = True
see_equity = False
if see_equity:
    plt.plot(equity,color='red')
    plt.plot(equity_fee,color='blue')
    # plt.plot(equity1,color='blue')
    # plt.plot(equity2,color='green')
    # plt.plot(equity3,color='yellow')

    pass
else:
    # plt.subplot(2,1,1)
    # plt.subplot(3,1,1)
    plt.grid() 
    # plt.plot(df['close'])
    draw_hb_chart_fast(df)
    plt.plot(df['zigzag'])
    plt.plot(df['lsl'])
    plt.plot(df['ssl'])
    # plt.plot(df['btarget'], linestyle='--',color='r')
    # draw_bollinger(df)
    # plt.plot(df['stair'])
    # plt.plot(df['stair_s'])
    # plt.plot(df['top_kvas'])
    # if len(longs1.shape) > 1:
    #     plt.scatter(longs1[:,0]-period-1,longs1[:,1],marker='h',color='green',s=100)
    # if len(shorts1.shape) > 1:
    #     plt.scatter(shorts1[:,0]-period-1,shorts1[:,1],marker='8',color='green',s=100)
    # if len(closes1.shape) > 1:
    #     plt.scatter(closes1[:,0]-period-1,closes1[:,1],marker='s',color='green',s=100)
    if len(longs.shape) > 1:
        plt.scatter(longs[:,0],longs[:,1],marker='^',color='black')
    if len(shorts.shape) > 1:
        plt.scatter(shorts[:,0],shorts[:,1],marker='v',color='black')
    if len(closes.shape) > 1:
        plt.scatter(closes[:,0],closes[:,1],marker='x',color='black')
    # for k in 'max_hb, min_hb, avarege'.split(', '):
    # # for k in 'max_hb, min_hb'.split(', '):
    # # for k in 'top_buff, bottom_buff'.split(', '):
    # for k in ('smab', 'bbub','bbdb','mub','mdb'):
    #     plt.plot(df[k],color='r',linestyle='--')
    # for k in ('stair','top_line','bottom_line'):
    # for k in ('bbu', 'bbd', 'sma'):
    #     plt.plot(df[k],color='b',linestyle=':')
    # plt.plot(df['top_zone'],color='r')
    # plt.plot(df['bottom_zone'],color='b')

    # plt.scatter(
    # df.index[~df['end_up'].isna()],
    # df['end_up'].dropna(),
    # marker='v',
    # color='red')
    # plt.scatter(
    # df.index[~df['end_down'].isna()],
    # df['end_down'].dropna(),
    # marker='^',
    # color='green')
    # plt.plot(df['bbu'],linestyle='--')
    # for k in ('bbd','sma'):
    #     plt.plot(df[k])
    # ax1 = plt.gca()
    # # plt.subplot(2,1,2,sharex=ax1)
    # plt.subplot(3,1,2,sharex=ax1)
    # plt.grid() 
    # 'ema_1','ema_2','macd','signal_line'
    # plt.plot(df['macd'],color='red')
    # plt.plot(df['signal_line'],color='blue')
    # plt.plot(df['rsi'])
    # for k in ('chop',):
    #     plt.plot(df[k])
    # draw_lite_chart(df)
    
    # plt.subplot(3,1,1)
    # # df.apply(draw_hb_chart,axis=1)
    # draw_hb_chart_fast(df)
    # for k in ('stop_long','stop_short','ema'):
    #     plt.plot(df[k])
    # ax1 = plt.gca()
    # plt.subplot(2,1,2,sharex=ax1)
    # plt.grid() 
    # plt.plot(df['rsi'])
    # plt.axhline(70)
    # plt.axhline(30)
    # plt.subplot(3,1,3,sharex=ax1)
    # plt.grid() 
    # plt.plot(df['adx'],color='blue')
    # plt.plot(df['rsi_tw'],color='red')
    # plt.axhline(40)
    # for k in ( 'sma','sma2','smab'):
    #     plt.plot(df[k])
    # # ax2 = plt.gca()
    # # plt.plot()
    # # plt.subplot(3,1,3,sharex=ax2)
    # # plt.grid() 
    # # for k in ('rsi',):
    # #     plt.plot(df[k])
    # # plt.axhline(75)
    # # plt.axhline(25)
    # plt.tight_layout() 

    # plt.subplot(2,1,2)
    # plt.plot(df['macd'],color='b')
    # plt.plot(df['signal_line'],color='red')
    # plt.plot(df['predicted_high'],color='b')
    # plt.plot(df['predicted_low'],color='violet')
    # plt.plot(df['predicted_middle'],color='black')
    # plt.plot(df['support'], color='b', linestyle='--', label='Поддержка')
    # plt.plot(df['resistance'], color='b', linestyle='--', label='Сопротивление')
    # df['predicted_high_shifted'] = df['predicted_high'].shift(10)
    # df['predicted_low_shifted'] = df['predicted_low'].shift(10)
    # plt.plot(df['varma_forecast'], label='Предсказанные максимумы', color='blue', linestyle=':')
    # print(df['varma_forecast'])
    # plt.plot(df['arima_forecast_low'], label='Предсказанные минимумы', color='blue', linestyle=':')
    # plt.plot(df['arima_forecast_high'], label='Предсказанные минимумы', color='violet', linestyle=':')
    # plt.plot(df['recent_min'],color='green')
    # plt.plot(df['recent_max'],color='blue')
    # plt.plot(df['stop_long'],color='yellow')
    # plt.plot(df['stop_short'],color='violet')
    # plt.plot(df.iloc[:100]['dynamics_ma']
    # draw_bollinger(df)
    # plt.plot(df['sma2'])
    # draw_dynamics(df)
    # draw_rails(df)
    # plt.plot(df['top_buff'],color='green')
    # plt.plot(df['bottom_buff'],color='green')
    # draw_chart_channel(df,'top_mean', 'bottom_mean', 'avarege_mean')
    # df.info()
    # print(df.head())
    # draw_chart_channel(df)
    # plt.plot(df['predicted_high'], label='Предсказанные максимумы', color='blue', linestyle='--')
    # plt.plot(df['predicted_low'], label='Предсказанные минимумы', color='red', linestyle='--')
    df.to_csv('test.csv')

print(time() - start)
plt.show()