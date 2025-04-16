import numpy as np
import pandas as pd
def add_van_zigzag(df, period=7):
    # Создаем копию DataFrame и сбрасываем индекс
    df = df.copy(deep=True).reset_index(drop=True)
    n = len(df)
    
    # Предварительный расчет экстремумов
    df['swing_high'] = df['high'].rolling(window=period+1, min_periods=1).max()
    df['swing_low'] = df['low'].rolling(window=period+1, min_periods=1).min()
    
    # Инициализация массивов
    zigzag = np.full(n, np.nan)
    zigzag_high = np.full(n, np.nan)
    zigzag_low = np.full(n, np.nan)
    
    # Получаем сырые массивы значений
    high_values = df['high'].values
    low_values = df['low'].values
    swing_high_values = df['swing_high'].values
    swing_low_values = df['swing_low'].values
    
    # Основные переменные состояния
    trend_dir = 0
    last_swing_index = -1
    last_swing_price = np.nan
    
    for idx in range(2*period, n):
        high = high_values[idx]
        low = low_values[idx]
        
        # Проверка экстремумов с учетом погрешности
        is_swing_high = np.isclose(high, swing_high_values[idx], atol=1e-5)
        is_swing_low = np.isclose(low, swing_low_values[idx], atol=1e-5)

        if not is_swing_high and not is_swing_low:
            continue

        # Логика обновления зигзага
        if trend_dir == 1 and is_swing_high and high >= last_swing_price:
            _update_zigzag(zigzag, zigzag_high, idx, high, last_swing_index)
            last_swing_index, last_swing_price = idx, high
            
        elif trend_dir == -1 and is_swing_low and low <= last_swing_price:
            _update_zigzag(zigzag, zigzag_low, idx, low, last_swing_index)
            last_swing_index, last_swing_price = idx, low
            
        elif trend_dir <= 0 and is_swing_high:
            trend_dir = 1
            zigzag[idx] = zigzag_high[idx] = high
            last_swing_index, last_swing_price = idx, high
            
        elif trend_dir >= 0 and is_swing_low:
            trend_dir = -1
            zigzag[idx] = zigzag_low[idx] = low
            last_swing_index, last_swing_price = idx, low

    # Добавляем результаты в DataFrame
    df['zigzag'] = zigzag
    df['zigzag_high'] = zigzag_high
    df['zigzag_low'] = zigzag_low
    df['zigzag_line'] = _interpolate_zigzag(zigzag)
    
    # Удаление начальных/конечных NaN
    return _trim_nan(df)

# Вспомогательные функции
def _update_zigzag(zigzag, target_arr, idx, value, last_idx):
    if last_idx != -1:
        zigzag[last_idx] = np.nan
        target_arr[last_idx] = np.nan
    zigzag[idx] = target_arr[idx] = value

def _interpolate_zigzag(zigzag):
    line = np.full_like(zigzag, np.nan)
    points = np.where(~np.isnan(zigzag))[0]
    
    for i in range(len(points)-1):
        start, end = points[i], points[i+1]
        line[start:end+1] = np.linspace(zigzag[start], zigzag[end], end-start+1)
    
    return line

def _trim_nan(df):
    first_valid = df['zigzag'].first_valid_index()
    last_valid = df['zigzag'].last_valid_index()
    
    if first_valid is not None and last_valid is not None:
        cols = ['zigzag', 'zigzag_line', 'zigzag_high', 'zigzag_low']
        df.loc[:first_valid, cols] = np.nan
        df.loc[last_valid+1:, cols] = np.nan
    
    return df