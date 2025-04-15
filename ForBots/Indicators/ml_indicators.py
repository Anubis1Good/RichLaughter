import numpy as np
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