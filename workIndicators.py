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
df = df.iloc[:100]
df = add_donchan_channel(df,20)
# df = add_dynamic_trend_lines_extended(df,2,60)
df['up_attach'] = np.nan
df['down_attach'] = np.nan
df['up_attach'] = np.where(df['high'] == df['max_hb'], df['high'], np.nan)
period=5
df['down_attach'] = np.where(df['low'] == df['min_hb'], df['low'], np.nan)

df['start_up'] = np.where((df['high'] == df['max_hb'])&(df['high'].shift(1) != df['max_hb'].shift(1)), df['high'], np.nan)
df['end_up'] = np.where((df['high'] == df['max_hb'])&(df['high'].shift(-1) != df['max_hb'].shift(-1)), df['high'], np.nan)

df['start_down'] = np.where((df['low'] == df['min_hb'])&(df['low'].shift(1) != df['min_hb'].shift(1)), df['low'], np.nan)
df['end_down'] = np.where((df['low'] == df['min_hb'])&(df['low'].shift(-1) != df['min_hb'].shift(-1)), df['low'], np.nan)

# Шаг 2: Собираем индексы всех стартов и финишей
starts = df[~df['start_up'].isna()].index.tolist()
ends = df[~df['end_up'].isna()].index.tolist()

# Шаг 3: Сопоставляем каждый старт с ближайшим финишем после него
df['up_move'] = np.nan

for start_idx in starts:
    # Ищем все финиши после текущего старта
    possible_ends = [e for e in ends if e >= start_idx]
    
    if possible_ends:
        # Берем самый ближний финиш
        end_idx = possible_ends[0]
        df.at[start_idx, 'up_move'] = df.at[end_idx, 'high'] - df.at[start_idx, 'high']

# Шаг 4: Особый случай - старт и финиш на одном баре
same_bar = (~df['start_up'].isna()) & (~df['end_up'].isna())
df.loc[same_bar, 'up_move'] = 0

# Шаг 2: Собираем индексы всех стартов и финишей
starts_down = df[~df['start_down'].isna()].index.tolist()
ends_down = df[~df['end_down'].isna()].index.tolist()

# Шаг 3: Сопоставляем каждый старт с ближайшим финишем после него
df['down_move'] = np.nan

for start_idx in starts_down:
    # Ищем все финиши после текущего старта
    possible_ends = [e for e in ends_down if e >= start_idx]
    
    if possible_ends:
        # Берем самый ближний финиш
        end_idx = possible_ends[0]
        df.at[start_idx, 'down_move'] = df.at[start_idx, 'low'] - df.at[end_idx, 'low']

# Шаг 4: Особый случай - старт и финиш на одном баре
same_bar_down = (~df['start_down'].isna()) & (~df['end_down'].isna())
df.loc[same_bar_down, 'down_move'] = 0

# Создаем списки индексов всех точек
start_up_indexes = df[~df['start_up'].isna()].index.tolist()
end_down_indexes = df[~df['end_down'].isna()].index.tolist()

# Инициализируем новый столбец
df['down_to_up'] = np.nan

# Для каждого end_down ищем ближайший следующий start_up
for end_down_idx in end_down_indexes:
    next_starts = [s for s in start_up_indexes if s > end_down_idx]
    if next_starts:
        nearest_start_up = next_starts[0]
        df.at[end_down_idx, 'down_to_up'] = df.at[nearest_start_up, 'high'] - df.at[end_down_idx, 'low']

# TODO START FUNC
end_up_indexes = df[~df['end_up'].isna()].index.tolist()
start_down_indexes = df[~df['start_down'].isna()].index.tolist()

df['up_to_down'] = np.nan

for end_up_idx in end_up_indexes:
    next_starts = [s for s in start_down_indexes if s > end_up_idx]
    if next_starts:
        nearest_start_down = next_starts[0]
        df.at[end_up_idx, 'up_to_down'] = df.at[end_up_idx, 'high'] - df.at[nearest_start_down, 'low']
        plt.plot(
            [end_up_idx, nearest_start_down],       # X-координаты
            [df.at[end_up_idx, 'high'],             # Y-координаты
            df.at[nearest_start_down, 'low']],
            'm--'  # Стиль линии: magenta, пунктир
        )
# TODO END FUNC
# print(df[~df['up_move'].isna()])
print('totalUP:',df['up_move'].sum())
print('totalDOWN:',df['down_move'].sum())
print('totalDU:',df['down_to_up'].sum())
print('totalUD:',df['up_to_down'].sum())
period=5
# df['max_hb'] = df['high'].rolling(window=period).max().rolling(window=period).mean()

# # Нижняя полоса (минимум за последние N периодов)
# df['min_hb'] = df['low'].rolling(window=period).min().rolling(window=period).mean()

# # Средняя линия
# df['avarege'] = (df['max_hb'] + df['min_hb']) / 2
# df = add_ema(df,200)
# df = add_rsi(df,10)

for idx, row in df[~df['up_move'].isna()].iterrows():
    plt.text(idx, row['start_up'] + 0.5, f'+{row["up_move"]}', ha='center')

# df = add_slice_df(df,14)
print(df.tail())
# plt.subplot(2,1,1)
# plt.grid() 
draw_hb_chart_fast(df)
for k in 'max_hb, min_hb'.split(', '):
    plt.plot(df[k],color='r',linestyle='--')
# for k in ('up_attach','down_attach'):
#     plt.plot(df[k],color='b',)
plt.scatter(
    df.index[~df['start_up'].isna()],
    df['start_up'].dropna(),
    marker='^',
    color='violet')
plt.scatter(
    df.index[~df['end_up'].isna()],
    df['end_up'].dropna(),
    marker='v',
    color='red')

plt.scatter(
    df.index[~df['start_down'].isna()],
    df['start_down'].dropna(),
    marker='v',
    color='blue')
plt.scatter(
    df.index[~df['end_down'].isna()],
    df['end_down'].dropna(),
    marker='^',
    color='green')
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