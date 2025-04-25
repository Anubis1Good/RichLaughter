import numpy as np
import pandas as pd
from math import atan, degrees
from scipy.spatial.distance import cdist

def add_find_similar_pattern(
    df, 
    window=20,
    metric='correlation',
    forecast_length=30
):
    """
    Находит похожий паттерн с учетом относительного изменения цены.
    Возвращает прогноз, масштабированный к текущему уровню цены.
    """
    close_prices = df['close'].values
    
    # 1. Текущий паттерн (последние `window` баров)
    current_pattern = close_prices[-window:]
    current_mean = np.mean(current_pattern)
    current_std = np.std(current_pattern)
    
    # 2. Нормализация текущего паттерна (Z-score)
    current_norm = (current_pattern - current_mean) / current_std if current_std != 0 else current_pattern * 0
    
    # 3. Поиск в истории (исключая последние `window + forecast_length` баров)
    history = close_prices[:-(window + forecast_length)]
    distances = []
    patterns = []
    
    for i in range(len(history) - window - forecast_length):
        past_pattern = history[i:i + window]
        future_prices = history[i + window:i + window + forecast_length]
        
        # Нормализация исторического паттерна
        past_mean = np.mean(past_pattern)
        past_std = np.std(past_pattern)
        past_norm = (past_pattern - past_mean) / past_std if past_std != 0 else past_pattern * 0
        
        # Расчет расстояния
        if metric == 'correlation':
            corr = np.corrcoef(current_norm, past_norm)[0, 1]
            distance = 1 - corr
        elif metric == 'mse':
            distance = np.mean((current_norm - past_norm) ** 2)
        elif metric == 'cosine':
            distance = cdist([current_norm], [past_norm], 'cosine')[0][0]
        else:
            raise ValueError("Метрика должна быть 'correlation', 'mse' или 'cosine'")
        
        distances.append(distance)
        patterns.append((i, past_pattern, future_prices, past_mean, past_std))
    
    # 4. Находим лучший паттерн
    best_idx = np.argmin(distances)
    best_match_idx, best_past, best_future, best_mean, best_std = patterns[best_idx]
    
    # 5. Масштабируем прогноз к текущему уровню цены
    scale = current_std / best_std if best_std != 0 else 1
    forecast = (best_future - best_mean) * scale + current_mean
    
    # 6. Записываем результаты
    df['similar_pattern'] = np.nan
    df.loc[df.index[best_match_idx:best_match_idx + window], 'similar_pattern'] = best_past
    
    df['forecast'] = np.nan
    # Важно: используем только существующие индексы!
    if len(df) >= forecast_length:
        df.loc[df.index[-forecast_length:], 'forecast'] = forecast[:forecast_length]
    else:
        df.loc[df.index[-len(forecast):], 'forecast'] = forecast[:len(df)]
    
    # Канал прогноза
    df['forecast_high'] = df['forecast'].rolling(window=5, min_periods=1).max()
    df['forecast_low'] = df['forecast'].rolling(window=5, min_periods=1).min()
    
    return df

def add_find_similar_pattern_lite(
    df, 
    window=20, 
    lookback=1000, 
    metric='correlation',
    forecast_length=30
):
    """
    add 'forecast_high'  'forecast_low'  'per_fs'
    Находит похожий паттерн и добавляет к последнему бару:
    - forecast_high: максимум прогноза.
    - forecast_low: минимум прогноза.
    "Метрика должна быть 'correlation', 'mse' или 'cosine'"
    """
    close_prices = df['close'].values
    
    # Проверка данных
    if len(df) < window + forecast_length:
        df['forecast_high'] = np.nan
        df['forecast_low'] = np.nan
        df['per_fs'] = np.nan
        return df
    
    # Корректировка lookback
    lookback = min(lookback, len(close_prices) - (window + forecast_length))
    history = close_prices[-lookback - window - forecast_length : - (window + forecast_length)]
    
    # Текущий паттерн (нормализованный)
    current_pattern = close_prices[-window:]
    current_mean = np.mean(current_pattern)
    current_std = np.std(current_pattern)
    current_norm = (current_pattern - current_mean) / current_std if current_std != 0 else current_pattern * 0
    
    # Поиск похожего паттерна
    best_distance = float('inf')
    best_future = None
    
    for i in range(len(history) - window - forecast_length):
        past_pattern = history[i:i + window]
        future_prices = history[i + window:i + window + forecast_length]
        
        past_mean = np.mean(past_pattern)
        past_std = np.std(past_pattern)
        past_norm = (past_pattern - past_mean) / past_std if past_std != 0 else past_pattern * 0
        
        if metric == 'correlation':
            corr = np.corrcoef(current_norm, past_norm)[0, 1]
            distance = 1 - corr
        elif metric == 'mse':
            distance = np.mean((current_norm - past_norm) ** 2)
        elif metric == 'cosine':
            distance = cdist([current_norm], [past_norm], 'cosine')[0][0]
        else:
            raise ValueError("Метрика должна быть 'correlation', 'mse' или 'cosine'")
        
        if distance < best_distance:
            best_distance = distance
            best_future = future_prices
            best_past_mean = past_mean
            best_past_std = past_std
    
    if best_future is None:
        df['forecast_high'] = np.nan
        df['forecast_low'] = np.nan
        df['per_fs'] = np.nan
        return df
    
    # Масштабируем прогноз
    scale = current_std / best_past_std if best_past_std > 1e-8 else 1.0
    forecast = (best_future - best_past_mean) * scale + current_mean
    
    # Записываем только highs/lows в последний бар
    df.loc[df.index[-1], 'forecast_high'] = np.max(forecast)
    df.loc[df.index[-1], 'forecast_low'] = np.min(forecast)
    epsilon = 1e-8  # Маленькое значение для стабильности
    df['per_fs'] = (((df['forecast_high'] - df['forecast_low']) / (df['forecast_high'] + epsilon)) * 100).round(2)
    return df




def add_linear_regression(df: pd.DataFrame, 
                         period: int = 20, 
                         price_col: str = 'close') -> pd.DataFrame:
    """
    'regression_line'
    'regression_angle'
    Добавляет в DataFrame:
    1. Угол наклона линейной регрессии (в градусах)
    2. Значение линии регрессии на последней свече окна
    
    :param df: Исходный DataFrame с ценами
    :param period: Размер окна для расчета
    :param price_col: Название колонки с ценами
    :return: Модифицированный DataFrame
    """
    # Создаем колонки для результатов
    df = df.copy()
    df['regression_angle'] = np.nan
    df['regression_line'] = np.nan
    
    # Предварительные расчеты
    x = np.arange(period)
    x_sum = x.sum()
    x2_sum = (x**2).sum()
    denominator = period * x2_sum - x_sum**2
    
    # Основной цикл расчета
    for i in range(period-1, len(df)):
        window = df[price_col].iloc[i-period+1:i+1]
        if len(window) != period:
            continue
            
        y = window.values
        y_sum = y.sum()
        xy = np.dot(x, y)
        
        # Расчет коэффициентов регрессии
        if denominator != 0:
            a = (period * xy - x_sum * y_sum) / denominator
        else:
            a = 0.0
            
        b = (y_sum - a * x_sum) / period
        
        # Запись результатов
        df.loc[df.index[i], 'regression_angle'] = degrees(atan(a))
        df.loc[df.index[i], 'regression_line'] = a * (period-1) + b
    
    # Заполнение пропусков
    df['regression_line'] = df['regression_line'].ffill()
    df['regression_angle'] = df['regression_angle'].ffill()
    
    return df

def add_linear_regression_last_row(df: pd.DataFrame, 
                                  period: int = 20, 
                                  price_col: str = 'close') -> pd.DataFrame:
    """
    Добавляет значения линейной регрессии ТОЛЬКО ДЛЯ ПОСЛЕДНЕЙ СТРОКИ.
    
    :param df: Исходный DataFrame с ценами
    :param period: Размер окна для расчета
    :param price_col: Название колонки с ценами
    :return: Модифицированный DataFrame
    """
    df = df.copy()
    
    # Создаем колонки, если их нет
    if 'regression_angle' not in df.columns:
        df['regression_angle'] = np.nan
    if 'regression_line' not in df.columns:
        df['regression_line'] = np.nan
    
    # Проверка достаточности данных
    if len(df) < period:
        return df
    
    # Берем последние period значений
    window = df[price_col].iloc[-period:]
    if len(window) != period:
        return df
    
    # Формулы линейной регрессии
    x = np.arange(period)
    x_sum = x.sum()
    y_sum = window.sum()
    xy = np.dot(x, window.values)
    denominator = period * (x**2).sum() - x_sum**2
    
    if denominator != 0:
        a = (period * xy - x_sum * y_sum) / denominator
    else:
        a = 0.0
        
    b = (y_sum - a * x_sum) / period
    
    # Расчет значений для последней строки
    angle = degrees(np.arctan(a))
    last_value = a * (period-1) + b
    
    # Обновляем только последнюю строку
    df.loc[df.index[-1], 'regression_angle'] = angle
    df.loc[df.index[-1], 'regression_line'] = last_value
    
    return df