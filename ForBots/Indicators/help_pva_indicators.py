import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def get_all_enter_exit_DC(df, kind_top, kind_bottom):
    """all_starts,all_ends"""
    # 1. Находим ВСЕ возможные точки входа и выхода (как в оригинале)
    all_starts = np.where(
        (df['high'] >= df[kind_top].shift(1)) & 
        (df['high'].shift(1) < df[kind_top].shift(2)),
        df[kind_top].shift(1), 
        np.nan
    )
    
    all_ends = np.where(
        (df['low'] <= df[kind_bottom].shift(1)) & 
        (df['low'].shift(1) > df[kind_bottom].shift(2)),
        df[kind_bottom].shift(1), 
        np.nan
    )
    return all_starts,all_ends

def get_all_lup(df,kind_top,kind_bottom):
    all_starts = np.where((df['high'].shift(1) >= df[kind_top].shift(1))&(df['high'] < df[kind_top]), df['high'], np.nan)
    all_ends = np.where((df['low'].shift(1) <= df[kind_bottom].shift(1))&(df['low'] > df[kind_bottom]), df['low'], np.nan)
    return all_starts,all_ends

def add_touch_signals(df,all_starts,all_ends, id):
    """
    Полный аналог add_enter_exit, но с touch_{id} (1 для входа, -1 для выхода).
    Условия и логика фильтрации идентичны оригиналу.
    """
    touch_col = 'touch_' + id
    df[touch_col] = np.nan  # Изначально все значения NaN

    # 2. Фильтруем сигналы, чтобы они чередовались
    last_signal = None
    for i in range(len(df)):
        current_start = all_starts[i]
        current_end = all_ends[i]

        if last_signal is None:
            if not np.isnan(current_start):
                df.loc[df.index[i], touch_col] = 1  # Вход
                last_signal = 'start'
            elif not np.isnan(current_end):
                df.loc[df.index[i], touch_col] = -1  # Выход
                last_signal = 'end'
            continue

        if last_signal == 'start' and not np.isnan(current_end):
            df.loc[df.index[i], touch_col] = -1
            last_signal = 'end'
        elif last_signal == 'end' and not np.isnan(current_start):
            df.loc[df.index[i], touch_col] = 1
            last_signal = 'start'

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



