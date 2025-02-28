import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import numpy.typing as npt
from Loader.BitgetLoader import bitget_loader
from utils.draw_utils import draw_lite_chart,draw_chart_channel,draw_hb_chart,draw_bollinger,draw_dynamics,draw_rails
# from ForBots.Indicators.classic_indicators import add_donchan_channel,add_vangerchik,add_sma, add_slice_df,add_bollinger,add_over_bb,add_attached_bb,add_big_volume,add_dynamics_ma
from strategies.test_strategies.check import check_strategy
# from strategies.work_strategies.PTA import PTA9_RAB as WS
# from strategies.work_strategies.STA_ca import STA1_LITE as WS
# from strategies.work_strategies.OGTA import OGTA3_Rails as WS
# from strategies.work_strategies.LTA import LTA_RAMEN as WS
from strategies.work_strategies.STA_ml import STAML1_XGBR2 as WS

from strategies.test_strategies.universal import universal_test_strategy as TS
raw_file = 'DataForTests\DataFromBitget\DOGEUSDT_1m_1739873922.csv'
# raw_file = 'DataForTests\DataFromBitget\DOGEUSDT_3m_1739873329.csv'
# raw_file = 'DataForTests\DataFromBitget\DOGEUSDT_5m_1739873413.csv'
# raw_file = 'DataForTests\DataFromBitget\DOGEUSDT_15m_1739873596.csv'
# raw_file = 'DataForTests\DataFromBitget\DOGEUSDT_30m_1738929225.csv'
# raw_file = 'DataForTests\DataFromBitget\DOGEUSDT_1H_1738929320.csv'
# raw_file = 'DataForTests\DataFromBitget\DOGEUSDT_4H_1738929422.csv'


df = bitget_loader(raw_file)
# df = df.iloc[0:200]
period = 50
multiplier = 0.5
symbol = "DOGEUSDT"
granularity = "1m"
slope = 4
# df = add_sma(df,period)
# df = add_donchan_channel(df,period)
# df = add_bollinger(df,period)
# df = add_over_bb(df)
# df = add_attached_bb(df)
# df = add_big_volume(df)
# df = add_dynamics_ma(df)
# df = add_slice_df(df,period)
# bot = STA1e(symbol,granularity,period=period,multiplier=multiplier,slope=slope)
# df = bot.get_test_df(df)
# bot = WS(symbol,granularity,period=period)
# bot = WS(symbol,granularity,period=period,k_period=8,d_period=3)
# bot = WS(symbol,granularity,period=period,slope=0.5)
# bot = WS(symbol,granularity,period=period,multiplier=multiplier)
bot = WS(symbol,granularity,period=period,future_steps=10)
df = bot.get_test_df(df)
# df.info()
# print(df.head())



# fee_base = 0.0004
fee_base = 0.0012
# trades,longs,shorts,closes,equity = check_strategy(df,get_action_STA1e,bot)
trades,longs,shorts,closes,equity = check_strategy(df,TS,bot)
print(trades)
fee = trades['count']*trades['open_price']*fee_base
print('fee',fee, (fee/trades['open_price'])*100)
print('total_with_fee',trades['total'] - fee, ((trades['total'] - fee)/trades['open_price'])*100)

# plt.plot(equity,color='red')



longs = np.array(longs)
shorts = np.array(shorts)
closes = np.array(closes)
equity = np.array(equity)

# draw_lite_chart(df)
df.apply(draw_hb_chart,axis=1)
# df['predicted_high_shifted'] = df['predicted_high'].shift(10)
# df['predicted_low_shifted'] = df['predicted_low'].shift(10)
# plt.plot(df['predicted_high_shifted'], label='Предсказанные максимумы', color='blue', linestyle=':')
# plt.plot(df['predicted_low_shifted'], label='Предсказанные минимумы', color='blue', linestyle=':')
# plt.plot(df['long_price'],color='green')
# plt.plot(df['short_price'],color='blue')
# plt.plot(df['stop_long'],color='yellow')
# plt.plot(df['stop_short'],color='violet')
# plt.subplot(2,1,1)
# plt.subplot(2,1,2)
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
plt.plot(df['predicted_high'], label='Предсказанные максимумы', color='green', linestyle='--')
plt.plot(df['predicted_low'], label='Предсказанные минимумы', color='red', linestyle='--')
df.to_csv('test.csv')
if len(longs.shape) > 1:
    plt.scatter(longs[:,0],longs[:,1],marker='^')
if len(shorts.shape) > 1:
    plt.scatter(shorts[:,0],shorts[:,1],marker='v')
if len(closes.shape) > 1:
    plt.scatter(closes[:,0],closes[:,1],marker='x')
plt.show()