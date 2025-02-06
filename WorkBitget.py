import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import numpy.typing as npt
from Loader.BitgetLoader import bitget_loader
from utils.draw_utils import draw_lite_chart,draw_chart_channel
from ForBots.Indicators.classic_indicators import add_donchan_channel,add_vangerchik
from strategies.test_strategies.check import check_strategy
from strategies.test_strategies.PTA import get_action_PTA2_BDDC,get_action_PTA2_BVGC
raw_file = 'DataForTests\DataFromBitget\DOGEUSDT1738854997.csv'


df = bitget_loader(raw_file)
# df = df.iloc[0:200]
# df.info()
df = add_donchan_channel(df,15)
df = add_vangerchik(df)

trades,longs,shorts,closes,equity = check_strategy(df,get_action_PTA2_BVGC)
print(trades)

longs = np.array(longs)
shorts = np.array(shorts)
closes = np.array(closes)
equity = np.array(equity)

# draw_lite_chart(df)
# draw_chart_channel(df)
# plt.scatter(longs[:,0],longs[:,1],marker='^')
# plt.scatter(shorts[:,0],shorts[:,1],marker='v')
# plt.scatter(closes[:,0],closes[:,1],marker='x')
plt.plot(equity,color='red')
trades,longs,shorts,closes,equity = check_strategy(df,get_action_PTA2_BDDC)
plt.plot(equity,color='blue')
print(trades)
plt.show()