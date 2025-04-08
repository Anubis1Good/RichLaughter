import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from time import time
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
df = add_donchan_channel(df,20)
start = time()
# def add_enter_exit(df, kind_enter, kind_exit, id):
#     # 1. Находим ВСЕ возможные точки
#     df['start_' + id] = np.where(
#         (df['high'] >= df[kind_enter].shift(1)) & 
#         (df['high'].shift(1) < df[kind_enter].shift(2)),
#         df[kind_enter].shift(1), 
#         np.nan
#     )
    
#     df['end_' + id] = np.where(
#         (df['low'] <= df[kind_exit].shift(1)) & 
#         (df['low'].shift(1) > df[kind_exit].shift(2)),
#         df[kind_exit].shift(1), 
#         np.nan
#     )
#     return df

# def add_filter_enter_exit(df,id):
#     # 2. Фильтруем чередующиеся сигналы
#     last_signal = None
#     for i in range(len(df)):
#         current_start = df.loc[df.index[i], 'start_' + id]
#         current_end = df.loc[df.index[i], 'end_' + id]

#         if last_signal is None:
#             if not pd.isna(current_start):
#                 last_signal = 'start'
#             elif not pd.isna(current_end):
#                 last_signal = 'end'
#             else:
#                 df.loc[df.index[i], 'start_' + id] = np.nan
#                 df.loc[df.index[i], 'end_' + id] = np.nan
#             continue

#         if last_signal == 'start' and not pd.isna(current_end):
#             last_signal = 'end'
#         elif last_signal == 'end' and not pd.isna(current_start):
#             last_signal = 'start'
#         else:
#             df.loc[df.index[i], 'start_' + id] = np.nan
#             df.loc[df.index[i], 'end_' + id] = np.nan

#     return df
def get_all_enter_exit(df, kind_enter, kind_exit):
    """all_starts,all_ends"""
    # 1. Находим ВСЕ возможные точки входа и выхода (как в оригинале)
    all_starts = np.where(
        (df['high'] >= df[kind_enter].shift(1)) & 
        (df['high'].shift(1) < df[kind_enter].shift(2)),
        df[kind_enter].shift(1), 
        np.nan
    )
    
    all_ends = np.where(
        (df['low'] <= df[kind_exit].shift(1)) & 
        (df['low'].shift(1) > df[kind_exit].shift(2)),
        df[kind_exit].shift(1), 
        np.nan
    )
    return all_starts,all_ends

def add_touch_signals(df, all_starts, all_ends, id):
    """
    Оптимизированная версия функции с векторизованными операциями.
    Возвращает столбец touch_{id} с чередующимися сигналами 1 (вход) и -1 (выход).
    """
    touch_col = 'touch_' + id
    df[touch_col] = np.nan
    
    # Создаем временные массивы
    signals = pd.Series(np.nan, index=df.index)
    last_signal = None
    
    # Векторизованные условия
    start_mask = ~np.isnan(all_starts)
    end_mask = ~np.isnan(all_ends)
    
    # Итерация по индексам с сохранением состояния
    for idx in df.index:
        if last_signal is None:
            if start_mask[idx]:
                signals[idx] = 1
                last_signal = 'start'
            elif end_mask[idx]:
                signals[idx] = -1
                last_signal = 'end'
        elif last_signal == 'start' and end_mask[idx]:
            signals[idx] = -1
            last_signal = 'end'
        elif last_signal == 'end' and start_mask[idx]:
            signals[idx] = 1
            last_signal = 'start'
    
    df[touch_col] = signals
    return df

def calculate_changes(df, id):
    """
    Оптимизированная версия функции для расчета изменений между сигналами.
    Возвращает DataFrame с колонками change_long_{id} и change_short_{id}.
    """
    touch_col = f'touch_{id}'
    df[f'change_long_{id}'] = np.nan
    df[f'change_short_{id}'] = np.nan
    
    # Получаем массивы numpy для более быстрого доступа
    signals = df[touch_col].values
    close_prices = df['close'].values
    index = df.index
    
    # Временные переменные
    last_signal = None
    last_signal_idx = -1
    last_signal_type = None
    
    for i in range(len(df)):
        current_signal = signals[i]
        
        if np.isnan(current_signal):
            continue
            
        if last_signal is None:
            last_signal = current_signal
            last_signal_idx = i
            last_signal_type = 'short' if current_signal == 1 else 'long'
            continue
            
        # Длинная позиция: 1 → -1
        if last_signal == 1 and current_signal == -1:
            entry_price = close_prices[last_signal_idx]
            exit_price = close_prices[i]
            df.at[index[i], f'change_short_{id}'] = entry_price - exit_price
            last_signal_type = None
            
        # Короткая позиция: -1 → 1
        elif last_signal == -1 and current_signal == 1:
            exit_price = close_prices[last_signal_idx]
            entry_price = close_prices[i]
            df.at[index[i], f'change_long_{id}'] = entry_price - exit_price
            last_signal_type = None
            
        last_signal = current_signal
        last_signal_idx = i
        last_signal_type = 'short' if current_signal == 1 else 'long'
    
    # Обработка последнего незавершенного сигнала
    if last_signal_type == 'long' and len(df) > 0:
        entry_price = close_prices[last_signal_idx]
        last_close = close_prices[-1]
        df.at[index[-1], f'change_long_{id}'] = last_close - entry_price
        
    elif last_signal_type == 'short' and len(df) > 0:
        exit_price = close_prices[last_signal_idx]
        last_close = close_prices[-1]
        df.at[index[-1], f'change_short_{id}'] = exit_price - last_close
    
    return df

def calculate_cumulative_changes(df, id):
    """
    Добавляет кумулятивные суммы для change_long и change_short
    
    Параметры:
        df: DataFrame с данными
        id: идентификатор сигнала (например '0' для touch_0)
        
    Возвращает:
        DataFrame с новыми столбцами cum_long_{id} и cum_short_{id}
    """
    # Создаем кумулятивные суммы, игнорируя NaN
    df[f'cum_long_{id}'] = df[f'change_long_{id}'].cumsum().ffill()
    df[f'cum_short_{id}'] = df[f'change_short_{id}'].cumsum().ffill()
    
    return df

def plot_touch_signals(df, id):
    touch_col = f'touch_{id}'
    if touch_col not in df.columns:
        raise ValueError(f"Столбец {touch_col} не найден!")

    # Входы (1)
    plt.scatter(
        df.index[df[touch_col] == 1],
        df.loc[df[touch_col] == 1, 'high'],
        marker='v',
        color='violet',
        label='Enter (1)'
    )
    
    # Выходы (-1)
    plt.scatter(
        df.index[df[touch_col] == -1],
        df.loc[df[touch_col] == -1, 'low'],
        marker='^',
        color='red',
        label='Exit (-1)'
    )
def get_all_lup(df,kind_top,kind_bottom):
    all_starts = np.where(
        (df['high'] >= df[kind_top].shift(1)) & 
        (df['high'].shift(1) < df[kind_top].shift(2)),
        df[kind_top].shift(1), 
        np.nan
    )
    all_ends = np.where((df['low'].shift(1) <= df[kind_bottom].shift(1))&(df['low'] > df[kind_bottom]), df['low'], np.nan)
    return all_starts,all_ends

all_starts,all_ends = get_all_lup(df,'avarege','min_hb')
# all_starts,all_ends = get_all_enter_exit(df,'max_hb','min_hb')
df = add_touch_signals(df,all_starts,all_ends,'0')
df = calculate_changes(df,'0')
df = calculate_cumulative_changes(df,'0')

df['sma_cl'] = df['cum_long_0'].diff().rolling(60).mean()
df['sma_cs'] = df['cum_short_0'].diff().rolling(60).mean()
print(df.tail())
draw_hb_chart_fast(df)
for k in 'max_hb, min_hb'.split(', '):
    plt.plot(df[k],color='r',linestyle='--')
plot_touch_signals(df,'0')
# plt.scatter(
#     df.index[~df['start_0'].isna()],
#     df['start_0'].dropna(),
#     marker='v',
#     color='violet')
# plt.scatter(
#     df.index[~df['end_0'].isna()],
#     df['end_0'].dropna(),
#     marker='^',
#     color='red')

print('Time:',time()-start)
plt.show()