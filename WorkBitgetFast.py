import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import numpy.typing as npt
from time import time
from Loader.BitgetLoader import bitget_loader
from utils.draw_utils import draw_lite_chart,draw_chart_channel,draw_hb_chart,draw_bollinger,draw_dynamics,draw_rails
# from ForBots.Indicators.classic_indicators import add_donchan_channel,add_vangerchik,add_sma, add_slice_df,add_bollinger,add_over_bb,add_attached_bb,add_big_volume,add_dynamics_ma
from strategies.test_strategies.check import check_strategy
# from strategies.work_strategies.PTA import PTA4_WLISICA as WS
from strategies.work_strategies.PTAX import PTA10_WIZARD as WS
# from strategies.work_strategies.STA_ca import STA1_LITE as WS
# from strategies.work_strategies.OGTA import OGTA4_DOG as WS
# from strategies.work_strategies.LTA import LTA_PIN as WS
# from strategies.work_strategies.MTA import MTA_LORD as WS
# from strategies.work_strategies.STA_ml import STAML1_XGBR2_DC as WS
# from strategies.work_strategies.STA_rl import STARL1_HELPGOD as WS
# from strategies.work_strategies.experiments import ExpBot as WS

from strategies.test_strategies.universal import vector_test_strategy as TS
raw_file = 'DataForTests\DataFromBitget\DOGEUSDT_1m_1739873922.csv'
# raw_file = 'DataForTests\oldBitget\DOGEUSDT_1m_1741087742_big.csv'
# raw_file = 'DataForTests\DataFromTicksBitget\DOGEUSDT_1m_from_ticks.csv'
# raw_file = 'DataForTests\DataFromBitget\DOGEUSDT_3m_1739873329.csv'
# raw_file = 'DataForTests\DataFromBitget\DOGEUSDT_5m_1739873413.csv'
# raw_file = 'DataForTests\DataFromBitget\DOGEUSDT_15m_1739873596.csv'
# raw_file = 'DataForTests\DataFromBitget\DOGEUSDT_30m_1738929225.csv'
# raw_file = 'DataForTests\oldBitget\DOGEUSDT_1H_1739872800.csv'
# raw_file = 'DataForTests\oldBitget\DOGEUSDT_4H_1739873240.csv'

start = time()

df = bitget_loader(raw_file)
# df = df.iloc[0:200]
period = 7
multiplier = 2
symbol = "DOGEUSDT"
granularity = "5m"



def analyze_trades(df):
    # Предполагаем, что у вас есть столбцы:
    # 'position' - текущая позиция (1 long, -1 short, 0 flat)
    # 'profit' - прибыль/убыток по сделке
    
    # Определяем моменты входа/выхода
    df['trade_opened'] = df['position'].diff().fillna(0).ne(0)
    df['trade_direction'] = df['position'].where(df['trade_opened'], 0)
    
    # Считаем сделки
    total_trades = df['trade_opened'].sum() // 2  # Каждая сделка - вход+выход
    profitable_trades = df.groupby((df['trade_direction'].ne(0).cumsum())['profit'].sum() > 0).sum()
    
    print(f"Всего сделок: {total_trades}")
    print(f"Прибыльных: {profitable_trades} ({profitable_trades/total_trades:.1%})")
    print(f"Средняя прибыль: {df[df['position'].ne(0)]['profit'].mean():.4f}")
    print(f"Макс. профит: {df['profit'].max():.4f}")
    print(f"Макс. убыток: {df['profit'].min():.4f}")

conf = (20,55,12,25,20)
bot = WS(symbol,granularity,"usdt-futures",1,*conf)

df = bot.get_test_df(df)
df = TS(df,bot)
df.info()
# df.info()
print(df.head())





# fee_base = 0.0004
fee_base = 0.0012
# trades,longs,shorts,closes,equity = check_strategy(df,get_action_STA1e,bot)
# trades,longs,shorts,closes,equity = check_strategy(df,TS,bot)
# print(trades)
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

see_equity = True
see_equity = False
if see_equity:
    # plt.plot(equity,color='red')
    pass
else:
    # draw_lite_chart(df)
    # plt.subplot(2,1,1)
    plt.subplot(3,1,1)
    df.apply(draw_hb_chart,axis=1)
    # if len(longs.shape) > 1:
    #     plt.scatter(longs[:,0],longs[:,1],marker='^',color='violet')
    # if len(shorts.shape) > 1:
    #     plt.scatter(shorts[:,0],shorts[:,1],marker='v',color='violet')
    # if len(closes.shape) > 1:
    #     plt.scatter(closes[:,0],closes[:,1],marker='x',color='violet')
    for k in ('ema_1','ema_2'):
        plt.plot(df[k])
    ax1 = plt.gca()
    plt.subplot(3,1,2,sharex=ax1)
    for k in ('macd','signal_line'):
        plt.plot(df[k])
    ax2 = plt.gca()
    plt.plot()
    plt.subplot(3,1,3,sharex=ax2)
    # plt.axhline(75)
    # plt.axhline(25)
    # for k in ('rsi_tw','adx'):
    for k in ('pos',):
        plt.plot(df[k])
    plt.tight_layout() 

#     # plt.subplot(2,1,2)
#     # plt.plot(df['macd'],color='b')
#     # plt.plot(df['signal_line'],color='red')
#     # plt.plot(df['predicted_high'],color='b')
#     # plt.plot(df['predicted_low'],color='violet')
#     # plt.plot(df['predicted_middle'],color='black')
#     # plt.plot(df['support'], color='b', linestyle='--', label='Поддержка')
#     # plt.plot(df['resistance'], color='b', linestyle='--', label='Сопротивление')
#     # df['predicted_high_shifted'] = df['predicted_high'].shift(10)
#     # df['predicted_low_shifted'] = df['predicted_low'].shift(10)
#     # plt.plot(df['varma_forecast'], label='Предсказанные максимумы', color='blue', linestyle=':')
#     # print(df['varma_forecast'])
#     # plt.plot(df['arima_forecast_low'], label='Предсказанные минимумы', color='blue', linestyle=':')
#     # plt.plot(df['arima_forecast_high'], label='Предсказанные минимумы', color='violet', linestyle=':')
#     # plt.plot(df['recent_min'],color='green')
#     # plt.plot(df['recent_max'],color='blue')
#     # plt.plot(df['stop_long'],color='yellow')
#     # plt.plot(df['stop_short'],color='violet')
#     # plt.plot(df.iloc[:100]['dynamics_ma']
#     # draw_bollinger(df)
#     # plt.plot(df['sma2'])
#     # draw_dynamics(df)
#     # draw_rails(df)
#     # plt.plot(df['top_buff'],color='green')
#     # plt.plot(df['bottom_buff'],color='green')
#     # draw_chart_channel(df,'top_mean', 'bottom_mean', 'avarege_mean')
#     # df.info()
#     # print(df.head())
#     # draw_chart_channel(df)
#     # plt.plot(df['predicted_high'], label='Предсказанные максимумы', color='blue', linestyle='--')
#     # plt.plot(df['predicted_low'], label='Предсказанные минимумы', color='red', linestyle='--')
#     df.to_csv('test.csv')

print(time() - start)
plt.show()