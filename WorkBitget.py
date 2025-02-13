import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import numpy.typing as npt
from Loader.BitgetLoader import bitget_loader
from utils.draw_utils import draw_lite_chart,draw_chart_channel,draw_hb_chart,draw_bollinger
from ForBots.Indicators.classic_indicators import add_donchan_channel,add_vangerchik,add_sma, add_slice_df,add_bollinger,add_over_bb,add_attached_bb,add_big_volume,add_dynamics_ma
from strategies.test_strategies.check import check_strategy
from strategies.test_strategies.PTA import get_action_PTA2_BDDC,get_action_PTA2_BVGC
from strategies.work_strategies.STA_ca import STA1e
from strategies.test_strategies.STA_ca import get_action_STA1e
raw_file = 'DataForTests\DataFromBitget\DOGEUSDT1738854997.csv'
# raw_file = 'DataForTests\DataFromBitget\DOGEUSDT_5m_1738928707.csv'
# raw_file = 'DataForTests\DataFromBitget\DOGEUSDT_15m_1738929100.csv'
# raw_file = 'DataForTests\DataFromBitget\DOGEUSDT_30m_1738929225.csv'
# raw_file = 'DataForTests\DataFromBitget\DOGEUSDT_1H_1738929320.csv'
# raw_file = 'DataForTests\DataFromBitget\DOGEUSDT_4H_1738929422.csv'


df = bitget_loader(raw_file)
# df = df.iloc[0:200]
period = 20
multiplier = 2
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
bot = STA1e(symbol,granularity,period=period,multiplier=multiplier,slope=slope)
df = bot.get_test_df(df)
# df.info()
# print(df.head())


# df = add_donchan_channel(df,15)
# df = add_donchan_channel(df,30)
# df = add_donchan_channel(df,60)
# df = add_vangerchik(df)
# fee_base = 0.0004
fee_base = 0.0012
trades,longs,shorts,closes,equity = check_strategy(df,get_action_STA1e,bot)
print(trades)
fee = trades['count']*trades['open_price']*fee_base
print(fee, (fee/trades['open_price'])*100)
print(trades['total'] - fee, ((trades['total'] - fee)/trades['open_price'])*100)
# plt.plot(equity,color='red')

# trades,longs,shorts,closes,equity = check_strategy(df,get_action_PTA2_BDDC)
# print(trades)
# fee = trades['count']*trades['open_price']*fee_base
# print(fee, (fee/trades['open_price'])*100)
# print(trades['total'] - fee, ((trades['total'] - fee)/trades['open_price'])*100)
# # print(equity)
# plt.plot(equity,color='blue')

longs = np.array(longs)
shorts = np.array(shorts)
closes = np.array(closes)
equity = np.array(equity)

# draw_lite_chart(df)
df.apply(draw_hb_chart,axis=1)
draw_bollinger(df)
# plt.subplot(2,1,1)
# plt.plot(df.iloc[:100]['sma'])
# plt.subplot(2,1,2)
# plt.plot(df.iloc[:100]['dynamics_ma'])

# draw_chart_channel(df)
plt.scatter(longs[:,0],longs[:,1],marker='^')
plt.scatter(shorts[:,0],shorts[:,1],marker='v')
plt.scatter(closes[:,0],closes[:,1],marker='x')
plt.show()