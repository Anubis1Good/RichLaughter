from request_functions.download_moex import download_moex,create_df
from datetime import date, timedelta
from utils.work_with_dataframe.convert_timeframe import convert_chart1to5
from ForBots.Indicators.classic_indicators import add_vodka_channel,add_rsi,add_rsi_tw,add_stochastic,add_cci,add_williams_r,add_mfi,add_awesome_oscillator,add_roc,add_ultimate_oscillator,add_cmo,add_keltner_channel,add_parabolic_sar,add_volume_profile,add_rvi,add_macd,add_adx
from ForBots.Indicators.vsa_indicators import add_real_vsa_stop_action,add_vsa_stop_action,add_simple_stop_action,add_aggressive_stop_action,add_balanced_stop_action
import pandas as pd
import matplotlib.pyplot as plt
from utils.draw_utils import draw_lite_chart,draw_chart_channel,draw_hb_chart
today = date.today()

# Вычитаем один день, чтобы получить вчерашнюю дату
yesterday = str(today - timedelta(days=3))
ticker = 'MMM5'
board = "RFUD"
market = "forts"
engine= "futures"

# ticker = 'GMKN'
# board = "TQBR"
# market: str = "shares"
# engine: str = "stock"
df = download_moex(ticker,1,yesterday,board=board,market=market,engine=engine)
df = create_df(df)
df = add_aggressive_stop_action(df)

df.info()
# df = convert_chart1to5(df)
# df = add_vodka_channel(df,7)
df.info()
# print(df.head())
print(df.tail())
dfw = df.iloc[-300:-200]
plt.subplot(2,1,1)
dfw.apply(draw_hb_chart,axis=1)

# for kind in ( 'poc', 'value_area_high', 'value_area_low'):
#     plt.plot(df.iloc[-100:][kind])
plt.subplot(2,1,2)
for kind in ('sa_signal' ,):
    plt.plot(dfw[kind])
# plt.plot(dfw['adx'])
# plt.subplot(3,1,3)
# plt.plot(dfw['rsi'],color='r')
# plt.plot(df.iloc[-100:]['rsi_tw'],color='b')
# plt.plot(dfw['rvi'],color='green',linestyle='dotted')
# plt.plot(dfw['%k'],color='blue',linestyle='dotted')
# plt.plot(dfw['%d'],color='green',linestyle='dotted')
# plt.axhline(70)
# plt.axhline(30)
plt.show()
