import pandas as pd
import numpy as np

def add_crisis_remora(df: pd.DataFrame, volatility_period=20, trend_period=50,quantile=75):
    """
    Добавляет колонку 'crisis_remora' в DataFrame.
    Crisis Remora сигнализирует о кризисах на основе волатильности и тренда.
    Порог волатильности — 25-й квантиль.
    
    :param df: DataFrame с колонкой 'close'
    :param volatility_period: Период для расчета волатильности (по умолчанию 20)
    :param trend_period: Период для трендового фильтра (по умолчанию 50)
    :return: DataFrame с добавленной колонкой 'crisis_remora'
    """
    # Вычисляем волатильность (стандартное отклонение)
    df['volatility'] = df['close'].rolling(window=volatility_period).std()
    
    # Вычисляем 25-й квантиль волатильности
    df['volatility_threshold'] = df['volatility'].rolling(window=volatility_period).quantile(quantile/100)
    
    # Вычисляем трендовый фильтр (скользящая средняя)
    df['trend'] = df['close'].rolling(window=trend_period).mean()
    
    # Генерация сигналов
    df['crisis_remora'] = np.where(
        (df['volatility'] > df['volatility_threshold']) & (df['close'] < df['trend']),  # Условие для кризиса
        1,  # Сигнал кризиса
        0   # Нет сигнала
    )
    
    # Заполняем NaN значения в начале DataFrame
    df['crisis_remora'] = df['crisis_remora'].fillna(0)
    
    return df

def add_vix(df: pd.DataFrame, period=20):
    """
    Добавляет колонку 'vix' в DataFrame.
    VIX рассчитывается как историческая волатильность.
    
    :param df: DataFrame с колонкой 'close'
    :param period: Период для расчета волатильности (по умолчанию 20)
    :return: DataFrame с добавленной колонкой 'vix'
    """
    # Вычисляем историческую волатильность (стандартное отклонение логарифмических изменений)
    log_returns = np.log(df['close'] / df['close'].shift(1))
    df['vix'] = log_returns.rolling(window=period).std() * np.sqrt(252)  # Годовая волатильность
    return df

def add_adaptive_channel(df: pd.DataFrame, period=20):
    """
    Добавляет колонки 'upper_band', 'lower_band', 'middle_band' в DataFrame.
    Адаптивный канал строится на основе исторической волатильности (VIX) и стандартного отклонения.
    
    :param df: DataFrame с колонкой 'close'
    :param period: Период для расчета волатильности, скользящей средней и стандартного отклонения (по умолчанию 20)
    :return: DataFrame с добавленными колонками 'upper_band', 'lower_band', 'middle_band'
    """
    # Вычисляем историческую волатильность (VIX)
    log_returns = np.log(df['close'] / df['close'].shift(1))
    df['vix'] = log_returns.rolling(window=period).std() * np.sqrt(252)  # Годовая волатильность
    
    # Нормализуем волатильность (приводим к диапазону 0–1)
    df['vix_normalized'] = (df['vix'] - df['vix'].rolling(window=period).min()) / \
                           (df['vix'].rolling(window=period).max() - df['vix'].rolling(window=period).min())
    
    # Вычисляем центральную линию (скользящая средняя)
    df['middle_band'] = df['close'].rolling(window=period).mean()
    
    # Вычисляем стандартное отклонение цен закрытия
    std_dev = df['close'].rolling(window=period).std()
    
    # Вычисляем верхнюю и нижнюю границы с использованием стандартного отклонения
    df['upper_band'] = df['middle_band'] + (std_dev * df['vix_normalized'])
    df['lower_band'] = df['middle_band'] - (std_dev * df['vix_normalized'])
    
    return df

def add_std_dev(df: pd.DataFrame, period=20):
    """
    Добавляет колонку 'std_dev' в DataFrame.
    
    :param df: DataFrame с колонкой 'close'
    :param period: Период для расчета стандартного отклонения (по умолчанию 20)
    :return: DataFrame с добавленной колонкой 'std_dev'
    """
    df['std_dev'] = df['close'].rolling(window=period).std()
    return df

def add_zigzag(df: pd.DataFrame, threshold=0.1, min_distance=10):
    """
    Добавляет колонку 'zigzag' в DataFrame.
    ZigZag рисует линии от минимумов к максимумам и наоборот.
    
    :param df: DataFrame с колонками 'high', 'low'
    :param threshold: Минимальное процентное изменение для формирования экстремума (по умолчанию 0.1%)
    :param min_distance: Минимальное расстояние между экстремумами в барах (по умолчанию 10)
    :return: DataFrame с добавленной колонкой 'zigzag'
    """
    # Инициализация переменных
    zigzag = np.nan * np.zeros(len(df))
    last_peak_idx = 0
    last_trough_idx = 0
    last_peak_price = df['high'].iloc[0]
    last_trough_price = df['low'].iloc[0]
    direction = None  # Направление: 1 (вверх), -1 (вниз)
    
    for i in range(1, len(df)):
        high = df['high'].iloc[i]
        low = df['low'].iloc[i]
        
        # Проверяем, является ли текущая точка максимумом
        if high > last_peak_price * (1 + threshold / 100):
            if i - last_peak_idx >= min_distance:
                # Рисуем линию от последнего минимума к текущему максимуму
                if direction == -1:
                    zigzag[last_trough_idx:i] = np.linspace(last_trough_price, high, i - last_trough_idx)
                last_peak_idx = i
                last_peak_price = high
                direction = 1
        
        # Проверяем, является ли текущая точка минимумом
        if low < last_trough_price * (1 - threshold / 100):
            if i - last_trough_idx >= min_distance:
                # Рисуем линию от последнего максимума к текущему минимуму
                if direction == 1:
                    zigzag[last_peak_idx:i] = np.linspace(last_peak_price, low, i - last_peak_idx)
                last_trough_idx = i
                last_trough_price = low
                direction = -1
    
    # Заполняем последний отрезок ZigZag
    if direction == 1:
        zigzag[last_peak_idx:] = last_peak_price
    elif direction == -1:
        zigzag[last_trough_idx:] = last_trough_price
    
    df['zigzag'] = zigzag
    return df

def add_chaikin_volatility(df: pd.DataFrame, ema_period=10, change_period=10):
    """
    Добавляет колонку 'chaikin_volatility' в DataFrame.
    
    :param df: DataFrame с колонками 'high', 'low'
    :param ema_period: Период для EMA (по умолчанию 10)
    :param change_period: Период для расчета изменения (по умолчанию 10)
    :return: DataFrame с добавленной колонкой 'chaikin_volatility'
    """
    # Вычисляем разницу между максимумом и минимумом
    df['range'] = df['high'] - df['low']
    
    # Вычисляем EMA разницы
    df['ema_range'] = df['range'].ewm(span=ema_period, adjust=False).mean()
    
    # Вычисляем изменение волатильности
    df['chaikin_volatility'] = (df['ema_range'] - df['ema_range'].shift(change_period)) / df['ema_range'].shift(change_period) * 100
    
    return df



def add_trend_lines(df: pd.DataFrame, min_points=2, num_lines=3):
    """
    Добавляет колонки 'trend_line_up_combined' и 'trend_line_down_combined' в DataFrame.
    Трендовые линии строятся на основе ключевых экстремумов и заканчиваются на последнем экстремуме.
    Верхние и нижние линии объединяются отдельно, а пропуски заполняются интерполяцией.
    
    :param df: DataFrame с колонками 'high', 'low'
    :param min_points: Минимальное количество точек для построения трендовой линии (по умолчанию 2)
    :param num_lines: Количество трендовых линий (по умолчанию 3)
    :return: DataFrame с добавленными колонками 'trend_line_up_combined', 'trend_line_down_combined'
    """
    # Инициализация переменных
    for i in range(1, num_lines + 1):
        df[f'trend_line_up_{i}'] = np.nan  # Восходящие трендовые линии
        df[f'trend_line_down_{i}'] = np.nan  # Нисходящие трендовые линии
    df['trend_line_up_combined'] = np.nan  # Объединенная верхняя линия
    df['trend_line_down_combined'] = np.nan  # Объединенная нижняя линия

    # Поиск ключевых минимумов для восходящего тренда
    lows = df['low'].values
    trend_up_points = []
    for i in range(1, len(lows) - 1):
        if lows[i] < lows[i - 1] and lows[i] < lows[i + 1]:  # Локальный минимум
            trend_up_points.append((i, lows[i]))
    
    # Построение нескольких восходящих трендовых линий
    if len(trend_up_points) >= min_points:
        step = len(trend_up_points) // num_lines  # Разделяем экстремумы на группы
        for i in range(num_lines):
            start = i * step
            end = (i + 1) * step if i < num_lines - 1 else len(trend_up_points)
            group = trend_up_points[start:end]
            if len(group) >= min_points:
                x = np.array([p[0] for p in group])
                y = np.array([p[1] for p in group])
                coeffs = np.polyfit(x, y, 1)  # Линейная регрессия
                # Линия заканчивается на последнем экстремуме
                line_values = np.polyval(coeffs, np.arange(group[0][0], group[-1][0] + 1))
                df.loc[group[0][0]:group[-1][0], f'trend_line_up_{i + 1}'] = line_values
    
    # Поиск ключевых максимумов для нисходящего тренда
    highs = df['high'].values
    trend_down_points = []
    for i in range(1, len(highs) - 1):
        if highs[i] > highs[i - 1] and highs[i] > highs[i + 1]:  # Локальный максимум
            trend_down_points.append((i, highs[i]))
    
    # Построение нескольких нисходящих трендовых линий
    if len(trend_down_points) >= min_points:
        step = len(trend_down_points) // num_lines  # Разделяем экстремумы на группы
        for i in range(num_lines):
            start = i * step
            end = (i + 1) * step if i < num_lines - 1 else len(trend_down_points)
            group = trend_down_points[start:end]
            if len(group) >= min_points:
                x = np.array([p[0] for p in group])
                y = np.array([p[1] for p in group])
                coeffs = np.polyfit(x, y, 1)  # Линейная регрессия
                # Линия заканчивается на последнем экстремуме
                line_values = np.polyval(coeffs, np.arange(group[0][0], group[-1][0] + 1))
                df.loc[group[0][0]:group[-1][0], f'trend_line_down_{i + 1}'] = line_values
    
    # Объединение верхних линий
    upper_lines = [df[f'trend_line_up_{i}'] for i in range(1, num_lines + 1)]
    df['trend_line_up_combined'] = pd.DataFrame(upper_lines).mean(skipna=True)
    
    # Объединение нижних линий
    lower_lines = [df[f'trend_line_down_{i}'] for i in range(1, num_lines + 1)]
    df['trend_line_down_combined'] = pd.DataFrame(lower_lines).mean(skipna=True)
    
    # Заполнение пропусков с помощью интерполяции
    df['trend_line_up_combined'] = df['trend_line_up_combined'].interpolate(method='linear')
    df['trend_line_down_combined'] = df['trend_line_down_combined'].interpolate(method='linear')
    
    return df

def calculate_atr(df: pd.DataFrame, period=14):
    """
    Вычисляет средний истинный диапазон (ATR) для DataFrame.
    
    :param df: DataFrame с колонками 'high', 'low', 'close'
    :param period: Период для расчета ATR (по умолчанию 14)
    :return: Series с значениями ATR
    """
    df['prev_close'] = df['close'].shift(1)
    df['tr1'] = df['high'] - df['low']
    df['tr2'] = np.abs(df['high'] - df['prev_close'])
    df['tr3'] = np.abs(df['low'] - df['prev_close'])
    df['tr'] = df[['tr1', 'tr2', 'tr3']].max(axis=1)
    df['atr'] = df['tr'].rolling(window=period).mean()
    return df['atr']

def calculate_supertrend(df: pd.DataFrame, atr_period=10, multiplier=3):
    """
    Вычисляет индикатор SuperTrend для DataFrame.
    
    :param df: DataFrame с колонками 'high', 'low', 'close'
    :param atr_period: Период для расчета ATR (по умолчанию 10)
    :param multiplier: Множитель для ATR (по умолчанию 3)
    :return: DataFrame с добавленными колонками 'supertrend', 'direction'
    """
    # Вычисляем ATR
    df['atr'] = calculate_atr(df, period=atr_period)
    
    # Вычисляем базовые линии (верхняя и нижняя)
    df['upper_band'] = (df['high'] + df['low']) / 2 + multiplier * df['atr']
    df['lower_band'] = (df['high'] + df['low']) / 2 - multiplier * df['atr']
    
    # Инициализация переменных
    df['supertrend'] = np.nan
    df['direction'] = 1  # 1 для восходящего тренда, -1 для нисходящего
    
    # Расчет SuperTrend
    for i in range(1, len(df)):
        # Определяем направление тренда
        if df['close'].iloc[i - 1] > df['upper_band'].iloc[i - 1]:
            df.loc[df.index[i], 'direction'] = -1
        elif df['close'].iloc[i - 1] < df['lower_band'].iloc[i - 1]:
            df.loc[df.index[i], 'direction'] = 1
        
        # Определяем значение SuperTrend
        if df['direction'].iloc[i] == 1:
            df.loc[df.index[i], 'supertrend'] = df['lower_band'].iloc[i]
        else:
            df.loc[df.index[i], 'supertrend'] = df['upper_band'].iloc[i]
    
    # Удаляем временные колонки
    df.drop(columns=['prev_close', 'tr1', 'tr2', 'tr3', 'tr', 'upper_band', 'lower_band'], inplace=True)
    
    return df

def calculate_zigzag(df: pd.DataFrame, threshold=0.0005):
    """
    Вычисляет индикатор ZigZag для DataFrame.
    
    :param df: DataFrame с колонкой 'close'
    :param threshold: Порог изменения цены для построения ZigZag (по умолчанию 1%)
    :return: DataFrame с добавленной колонкой 'zigzag'
    """
    df['zigzag'] = np.nan
    last_extreme = df['close'].iloc[0]
    last_extreme_index = 0
    
    for i in range(1, len(df)):
        current_price = df['close'].iloc[i]
        change = abs(current_price - last_extreme) / last_extreme
        
        if change >= threshold:
            df.loc[df.index[last_extreme_index], 'zigzag'] = last_extreme
            df.loc[df.index[i], 'zigzag'] = current_price
            last_extreme = current_price
            last_extreme_index = i
    
    return df