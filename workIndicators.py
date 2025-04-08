import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from Loader.BitgetLoader import bitget_loader
from utils.draw_utils import draw_lite_chart,draw_chart_channel,draw_hb_chart_fast,draw_bollinger,draw_dynamics,draw_rails
from ForBots.Indicators.classic_indicators import *
from ForBots.Indicators.vsa_indicators import *
from ForBots.Indicators.rare_indicators import *
from scipy.stats import linregress

raw_file = 'DataForTests\DataFromBitget\DOGEUSDT_1m_1739873922.csv'
raw_file = 'DataForTests\DataFromMOEX\MMH5_1_1739993452.csv'
period = 10
df = bitget_loader(raw_file)
# df = df.iloc[-100:]
df = df.iloc[:500]
# df['mean_volume'] = df['volume'].rolling(10).mean()
# df['top_zone'] = np.where(df['volume'] > df['mean_volume']*2,df['high'],np.nan)
# df['bottom_zone'] = np.where(df['volume'] > df['mean_volume']*2,df['low'],np.nan)
# df['top_zone'] = df['top_zone'].ffill()
# df['bottom_zone'] = df['bottom_zone'].ffill()
def add_detect_volume_zones(df, window=10, volume_multiplier=1.5, spread_threshold=1.2):
    """
    Определяет зоны больших баров по объему и спреду
    :param df: DataFrame с колонками ['high', 'low', 'close', 'volume']
    :param window: окно для скользящего среднего
    :param volume_multiplier: во сколько раз объем должен превышать средний
    :param spread_threshold: порог для спреда (в стандартных отклонениях)
    :return: DataFrame с добавленными колонками зон
    """
    # Рассчет базовых показателей
    df['mean_volume'] = df['volume'].rolling(window).mean()
    df['volume_std'] = df['volume'].rolling(window).std()
    df['spread'] = df['high'] - df['low']
    df['mean_spread'] = df['spread'].rolling(window).mean()
    df['spread_std'] = df['spread'].rolling(window).std()
    
    # Комбинированные условия для значимых баров
    volume_condition = df['volume'] > (df['mean_volume'] + volume_multiplier * df['volume_std'])
    spread_condition = df['spread'] > (df['mean_spread'] + spread_threshold * df['spread_std'])
    df['big_spred'] = np.where(spread_condition,True,False)
    # Определение зон
    df['big_bar'] = volume_condition & spread_condition
    df['top_zone'] = np.where(df['big_bar'], df['high'], np.nan)
    df['bottom_zone'] = np.where(df['big_bar'], df['low'], np.nan)
    
    # Заполнение зон вперед с "затуханием"
    df['top_zone'] = df['top_zone'].ffill()
    df['bottom_zone'] = df['bottom_zone'].ffill()
    
    # Дополнительные метрики
    df['zone_width'] = df['top_zone'] - df['bottom_zone']
    df['mid_zone'] = (df['top_zone'] + df['bottom_zone']) / 2
    
    return df
df = add_detect_volume_zones(df)
# df = add_donchan_channel(df,20)

# df = add_slice_df(df,14)
print(df.tail())
# plt.subplot(2,1,1)
# plt.grid() 
draw_hb_chart_fast(df)
plt.plot(df['top_zone'],color='r')
plt.plot(df['bottom_zone'],color='b')

plt.scatter(df[df['big_spred']].index, 
            df[df['big_spred']]['high'], 
            color='lime', marker='^',  label='Широкий спред (High)')
plt.scatter(df[df['big_spred']].index, 
            df[df['big_spred']]['low'], 
            color='red', marker='v',  label='Широкий спред (Low)')
# ax1 = plt.gca()
# plt.subplot(2,1,2,sharex=ax1)
# plt.grid() 
# for k in ('regression_slope',):
#     plt.plot(df[k])
# for k in ( 'regression_line','upper_channel','lower_channel'):
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