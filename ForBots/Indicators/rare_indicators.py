import pandas as pd
import numpy as np
from sklearn.cluster import KMeans

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

# CHECK THIS
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

#USE THIS
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


# MY_reserv
def add_dynamic_trend_lines_slope(df: pd.DataFrame, min_points=2, divider=60):
    """
    Исправленная версия с обработкой ошибок размерности
    """
    # Создаем копию DataFrame для работы
    result_df = df.copy()
    num_lines = max(len(result_df.index) // divider, 1)
    
    # 1. Подготовка всех колонок заранее
    new_columns = {
        **{f'trend_line_up_{i}': np.nan for i in range(1, num_lines + 1)},
        **{f'trend_line_down_{i}': np.nan for i in range(1, num_lines + 1)},
        **{f'slope_up_{i}': np.nan for i in range(1, num_lines + 1)},
        **{f'slope_down_{i}': np.nan for i in range(1, num_lines + 1)},
        'trend_up_combined': np.nan,
        'trend_down_combined': np.nan,
        'trend_up_slope': np.nan,
        'trend_down_slope': np.nan,
        'trend_mean_slope': np.nan
    }
    
    # Создаем временный DataFrame для новых данных
    trend_data = pd.DataFrame(new_columns, index=result_df.index)
    
    # 2. Поиск экстремумов с проверкой границ
    def find_extremes(values, mode='min'):
        extremes = []
        for i in range(1, len(values) - 1):
            if mode == 'min':
                if values[i] < values[i-1] and values[i] < values[i+1]:
                    extremes.append(i)
            else:
                if values[i] > values[i-1] and values[i] > values[i+1]:
                    extremes.append(i)
        return extremes
    
    up_points = find_extremes(result_df['low'].values, 'min')
    down_points = find_extremes(result_df['high'].values, 'max')

    # 3. Обработка восходящих трендов с проверкой диапазона
    if len(up_points) >= min_points:
        step = max(len(up_points) // num_lines, 1)
        
        for line_num in range(num_lines):
            start = line_num * step
            end = (line_num + 1) * step if line_num < num_lines - 1 else len(up_points)
            group = up_points[start:end]
            
            if len(group) >= min_points:
                x = np.array(group)
                y = result_df['low'].iloc[group].values
                
                # Добавляем проверку на уникальность точек
                if len(np.unique(x)) < min_points:
                    continue
                
                try:
                    coeffs = np.polyfit(x, y, 1)
                    slope = coeffs[0]
                    
                    line_start = group[0]
                    line_end = group[-1]
                    
                    # Проверяем корректность диапазона
                    if line_start >= len(trend_data) or line_end >= len(trend_data):
                        continue
                    
                    # Вычисляем значения с проверкой длины
                    x_range = np.arange(line_start, line_end + 1)
                    if len(x_range) == 0:
                        continue
                        
                    line_values = np.polyval(coeffs, x_range)
                    
                    # Присваиваем значения через .loc с явным указанием индексов
                    trend_data.loc[trend_data.index[line_start:line_end+1], f'trend_line_up_{line_num+1}'] = line_values
                    trend_data.loc[trend_data.index[line_start:line_end+1], f'slope_up_{line_num+1}'] = slope
                    
                except (TypeError, np.linalg.LinAlgError) as e:
                    continue

    # 4. Аналогичная обработка для нисходящих трендов
    if len(down_points) >= min_points:
        step = max(len(down_points) // num_lines, 1)
        
        for line_num in range(num_lines):
            start = line_num * step
            end = (line_num + 1) * step if line_num < num_lines - 1 else len(down_points)
            group = down_points[start:end]
            
            if len(group) >= min_points:
                x = np.array(group)
                y = result_df['high'].iloc[group].values
                
                if len(np.unique(x)) < min_points:
                    continue
                
                try:
                    coeffs = np.polyfit(x, y, 1)
                    slope = coeffs[0]
                    
                    line_start = group[0]
                    line_end = group[-1]
                    
                    if line_start >= len(trend_data) or line_end >= len(trend_data):
                        continue
                    
                    x_range = np.arange(line_start, line_end + 1)
                    if len(x_range) == 0:
                        continue
                        
                    line_values = np.polyval(coeffs, x_range)
                    
                    trend_data.loc[trend_data.index[line_start:line_end+1], f'trend_line_down_{line_num+1}'] = line_values
                    trend_data.loc[trend_data.index[line_start:line_end+1], f'slope_down_{line_num+1}'] = slope
                    
                except (TypeError, np.linalg.LinAlgError) as e:
                    continue

    # 5. Объединение линий с проверкой наличия колонок
    up_cols = [col for col in trend_data.columns if col.startswith('trend_line_up_')]
    down_cols = [col for col in trend_data.columns if col.startswith('trend_line_down_')]
    
    if up_cols:
        trend_data['trend_up_combined'] = trend_data[up_cols].mean(axis=1)
    if down_cols:
        trend_data['trend_down_combined'] = trend_data[down_cols].mean(axis=1)
    
    # 6. Заполнение slope с обработкой NaN
    for i in range(1, num_lines + 1):
        up_col = f'slope_up_{i}'
        down_col = f'slope_down_{i}'
        
        if up_col in trend_data.columns:
            mask = ~trend_data[up_col].isna()
            trend_data.loc[mask, 'trend_up_slope'] = trend_data.loc[mask, up_col]
        
        if down_col in trend_data.columns:
            mask = ~trend_data[down_col].isna()
            trend_data.loc[mask, 'trend_down_slope'] = trend_data.loc[mask, down_col]

    # 7. Интерполяция и расчет среднего slope
    for col in ['trend_up_combined', 'trend_down_combined', 'trend_up_slope', 'trend_down_slope']:
        if col in trend_data.columns:
            trend_data[col] = trend_data[col].interpolate(method='linear')
    trend_data['trend_up_slope'] = np.tanh(trend_data['trend_up_slope'])
    trend_data['trend_down_slope'] = np.tanh(trend_data['trend_down_slope'])

    if 'trend_up_slope' in trend_data.columns and 'trend_down_slope' in trend_data.columns:
        trend_data['trend_mean_slope'] = (trend_data['trend_up_slope'] + trend_data['trend_down_slope']) / 2

    # 8. Объединение с исходными данными
    result_cols = [
        'trend_up_combined',
        'trend_down_combined',
        'trend_up_slope',
        'trend_down_slope',
        'trend_mean_slope'
    ]
    
    # Выбираем только существующие колонки
    result_cols = [col for col in result_cols if col in trend_data.columns]
    
    result_df = pd.concat([result_df, trend_data[result_cols]], axis=1)
    
    return result_df

# MY
# Norm, but it's have strange things
def add_dynamic_trend_lines_slope_reversed(df: pd.DataFrame, min_points=2, divider=60):
    """
    'trend_up_combined','trend_down_combined','trend_mean_slope'
    Версия с поиском трендовых линий в обратном порядке (от конца к началу)
    """
    # Создаем копию DataFrame для работы
    result_df = df.copy()
    num_lines = max(len(result_df.index) // divider, 1)
    
    # 1. Подготовка всех колонок заранее
    new_columns = {
        **{f'trend_line_up_{i}': np.nan for i in range(1, num_lines + 1)},
        **{f'trend_line_down_{i}': np.nan for i in range(1, num_lines + 1)},
        **{f'slope_up_{i}': np.nan for i in range(1, num_lines + 1)},
        **{f'slope_down_{i}': np.nan for i in range(1, num_lines + 1)},
        'trend_up_combined': np.nan,
        'trend_down_combined': np.nan,
        'trend_up_slope': np.nan,
        'trend_down_slope': np.nan,
        'trend_mean_slope': np.nan
    }
    
    # Создаем временный DataFrame для новых данных
    trend_data = pd.DataFrame(new_columns, index=result_df.index)
    
    # 2. Поиск экстремумов с проверкой границ (в обратном порядке)
    def find_extremes(values, mode='min'):
        extremes = []
        for i in range(len(values)-2, 0, -1):  # Идем от конца к началу
            if mode == 'min':
                if values[i] < values[i-1] and values[i] < values[i+1]:
                    extremes.append(i)
            else:
                if values[i] > values[i-1] and values[i] > values[i+1]:
                    extremes.append(i)
        return extremes
    
    up_points = find_extremes(result_df['low'].values, 'min')
    down_points = find_extremes(result_df['high'].values, 'max')

    # 3. Обработка восходящих трендов с проверкой диапазона (в обратном порядке)
    if len(up_points) >= min_points:
        step = max(len(up_points) // num_lines, 1)
        
        for line_num in range(num_lines):
            start = line_num * step
            end = (line_num + 1) * step if line_num < num_lines - 1 else len(up_points)
            group = up_points[start:end]
            
            if len(group) >= min_points:
                x = np.array(group)
                y = result_df['low'].iloc[group].values
                
                # Добавляем проверку на уникальность точек
                if len(np.unique(x)) < min_points:
                    continue
                
                try:
                    coeffs = np.polyfit(x, y, 1)
                    slope = coeffs[0]
                    
                    line_start = group[-1]  # Берем последнюю точку как начало (так как идем в обратном порядке)
                    line_end = group[0]    # Берем первую точку как конец
                    
                    # Проверяем корректность диапазона
                    if line_start >= len(trend_data) or line_end >= len(trend_data):
                        continue
                    
                    # Вычисляем значения с проверкой длины
                    x_range = np.arange(line_start, line_end + 1) if line_start < line_end else np.arange(line_end, line_start + 1)
                    if len(x_range) == 0:
                        continue
                        
                    line_values = np.polyval(coeffs, x_range)
                    
                    # Присваиваем значения через .loc с явным указанием индексов
                    if line_start < line_end:
                        trend_data.loc[trend_data.index[line_start:line_end+1], f'trend_line_up_{line_num+1}'] = line_values
                        trend_data.loc[trend_data.index[line_start:line_end+1], f'slope_up_{line_num+1}'] = slope
                    else:
                        trend_data.loc[trend_data.index[line_end:line_start+1], f'trend_line_up_{line_num+1}'] = line_values[::-1]
                        trend_data.loc[trend_data.index[line_end:line_start+1], f'slope_up_{line_num+1}'] = slope
                    
                except (TypeError, np.linalg.LinAlgError) as e:
                    continue

    # 4. Аналогичная обработка для нисходящих трендов (в обратном порядке)
    if len(down_points) >= min_points:
        step = max(len(down_points) // num_lines, 1)
        
        for line_num in range(num_lines):
            start = line_num * step
            end = (line_num + 1) * step if line_num < num_lines - 1 else len(down_points)
            group = down_points[start:end]
            
            if len(group) >= min_points:
                x = np.array(group)
                y = result_df['high'].iloc[group].values
                
                if len(np.unique(x)) < min_points:
                    continue
                
                try:
                    coeffs = np.polyfit(x, y, 1)
                    slope = coeffs[0]
                    
                    line_start = group[-1]  # Берем последнюю точку как начало
                    line_end = group[0]    # Берем первую точку как конец
                    
                    if line_start >= len(trend_data) or line_end >= len(trend_data):
                        continue
                    
                    x_range = np.arange(line_start, line_end + 1) if line_start < line_end else np.arange(line_end, line_start + 1)
                    if len(x_range) == 0:
                        continue
                        
                    line_values = np.polyval(coeffs, x_range)
                    
                    if line_start < line_end:
                        trend_data.loc[trend_data.index[line_start:line_end+1], f'trend_line_down_{line_num+1}'] = line_values
                        trend_data.loc[trend_data.index[line_start:line_end+1], f'slope_down_{line_num+1}'] = slope
                    else:
                        trend_data.loc[trend_data.index[line_end:line_start+1], f'trend_line_down_{line_num+1}'] = line_values[::-1]
                        trend_data.loc[trend_data.index[line_end:line_start+1], f'slope_down_{line_num+1}'] = slope
                    
                except (TypeError, np.linalg.LinAlgError) as e:
                    continue

    # Остальная часть функции остается без изменений
    # 5. Объединение линий с проверкой наличия колонок
    up_cols = [col for col in trend_data.columns if col.startswith('trend_line_up_')]
    down_cols = [col for col in trend_data.columns if col.startswith('trend_line_down_')]
    
    if up_cols:
        trend_data['trend_up_combined'] = trend_data[up_cols].mean(axis=1)
    if down_cols:
        trend_data['trend_down_combined'] = trend_data[down_cols].mean(axis=1)
    
    # 6. Заполнение slope с обработкой NaN
    for i in range(1, num_lines + 1):
        up_col = f'slope_up_{i}'
        down_col = f'slope_down_{i}'
        
        if up_col in trend_data.columns:
            mask = ~trend_data[up_col].isna()
            trend_data.loc[mask, 'trend_up_slope'] = trend_data.loc[mask, up_col]
        
        if down_col in trend_data.columns:
            mask = ~trend_data[down_col].isna()
            trend_data.loc[mask, 'trend_down_slope'] = trend_data.loc[mask, down_col]

    # 7. Интерполяция и расчет среднего slope
    for col in ['trend_up_combined', 'trend_down_combined', 'trend_up_slope', 'trend_down_slope']:
        if col in trend_data.columns:
            trend_data[col] = trend_data[col].interpolate(method='linear')
    trend_data['trend_up_slope'] = np.tanh(trend_data['trend_up_slope'])
    trend_data['trend_down_slope'] = np.tanh(trend_data['trend_down_slope'])

    if 'trend_up_slope' in trend_data.columns and 'trend_down_slope' in trend_data.columns:
        trend_data['trend_mean_slope'] = (trend_data['trend_up_slope'] + trend_data['trend_down_slope']) / 2

    # 8. Объединение с исходными данными
    result_cols = [
        'trend_up_combined',
        'trend_down_combined',
        'trend_up_slope',
        'trend_down_slope',
        'trend_mean_slope'
    ]
    
    # Выбираем только существующие колонки
    result_cols = [col for col in result_cols if col in trend_data.columns]
    
    result_df = pd.concat([result_df, trend_data[result_cols]], axis=1)
    
    return result_df

# Work
def add_dynamic_trend_lines_slope2(df: pd.DataFrame, min_points=2, divider=60):
    """
    Строит линейные регрессии на каждые divider баров для экстремумов
    """
    result_df = df.copy()
    
    # 1. Подготовка всех колонок заранее
    # Мы не знаем заранее сколько будет линий, поэтому будем добавлять их динамически
    result_df['trend_up_combined'] = np.nan
    result_df['trend_down_combined'] = np.nan
    result_df['trend_up_slope'] = np.nan
    result_df['trend_down_slope'] = np.nan
    result_df['trend_mean_slope'] = np.nan
    
    # 2. Поиск экстремумов с проверкой границ
    def find_extremes(values, mode='min'):
        extremes = []
        for i in range(1, len(values) - 1):
            if mode == 'min':
                if values[i] < values[i-1] and values[i] < values[i+1]:
                    extremes.append(i)
            else:
                if values[i] > values[i-1] and values[i] > values[i+1]:
                    extremes.append(i)
        return extremes
    
    up_points = find_extremes(result_df['low'].values, 'min')
    down_points = find_extremes(result_df['high'].values, 'max')

    # 3. Обработка восходящих трендов - строим регрессию на каждом отрезке divider баров
    for i in range(0, len(result_df), divider):
        segment_end = min(i + divider, len(result_df))
        
        # Находим экстремумы в текущем сегменте
        segment_up_points = [p for p in up_points if i <= p < segment_end]
        
        if len(segment_up_points) >= min_points:
            x = np.array(segment_up_points)
            y = result_df['low'].iloc[segment_up_points].values
                
            if len(np.unique(x)) >= min_points:
                try:
                    coeffs = np.polyfit(x, y, 1)
                    slope = coeffs[0]
                    
                    # Вычисляем значения линии для всего сегмента
                    x_range = np.arange(i, segment_end)
                    line_values = np.polyval(coeffs, x_range)
                    
                    # Записываем значения
                    result_df.loc[result_df.index[i:segment_end], 'trend_up_combined'] = line_values
                    result_df.loc[result_df.index[i:segment_end], 'trend_up_slope'] = slope
                    
                except (TypeError, np.linalg.LinAlgError) as e:
                    continue

    # 4. Аналогичная обработка для нисходящих трендов
    for i in range(0, len(result_df), divider):
        segment_end = min(i + divider, len(result_df))
        
        segment_down_points = [p for p in down_points if i <= p < segment_end]
        
        if len(segment_down_points) >= min_points:
            x = np.array(segment_down_points)
            y = result_df['high'].iloc[segment_down_points].values
                
            if len(np.unique(x)) >= min_points:
                try:
                    coeffs = np.polyfit(x, y, 1)
                    slope = coeffs[0]
                    
                    x_range = np.arange(i, segment_end)
                    line_values = np.polyval(coeffs, x_range)
                    
                    result_df.loc[result_df.index[i:segment_end], 'trend_down_combined'] = line_values
                    result_df.loc[result_df.index[i:segment_end], 'trend_down_slope'] = slope
                    
                except (TypeError, np.linalg.LinAlgError) as e:
                    continue

    # 5. Интерполяция и расчет среднего slope
    for col in ['trend_up_combined', 'trend_down_combined', 'trend_up_slope', 'trend_down_slope']:
        result_df[col] = result_df[col].interpolate(method='linear')
    
    # Применяем tanh к slope для нормализации
    result_df['trend_up_slope'] = np.tanh(result_df['trend_up_slope'])
    result_df['trend_down_slope'] = np.tanh(result_df['trend_down_slope'])
    result_df['trend_mean_slope'] = (result_df['trend_up_slope'] + result_df['trend_down_slope']) / 2

    return result_df

def add_regression_with_std_channels(df: pd.DataFrame, window=60, std_dev=1.0, min_points=5):
    """
    'regression_line','upper_channel','lower_channel','regression_slope','residual_std'
    Строит линейную регрессию по close и добавляет каналы стандартных отклонений
    
    Параметры:
        df - DataFrame с ценами
        window - размер окна для построения регрессии (в барах)
        std_dev - количество стандартных отклонений для каналов
        min_points - минимальное количество точек для построения регрессии
    """
    result_df = df.copy()
    
    # Создаем колонки для результатов
    result_df['regression_line'] = np.nan
    result_df['upper_channel'] = np.nan
    result_df['lower_channel'] = np.nan
    result_df['regression_slope'] = np.nan
    result_df['residual_std'] = np.nan
    
    # Проходим по всему DataFrame с заданным окном
    for i in range(window, len(result_df)):
        window_slice = result_df.iloc[i-window:i]
        close_prices = window_slice['close'].values
        
        # Проверяем, что у нас достаточно точек
        if len(close_prices) < min_points:
            continue
            
        x = np.arange(len(close_prices))
        
        try:
            # Строим линейную регрессию
            coeffs = np.polyfit(x, close_prices, 1)
            slope = coeffs[0]
            intercept = coeffs[1]
            
            # Вычисляем предсказанные значения
            y_pred = np.polyval(coeffs, x)
            
            # Вычисляем остатки и стандартное отклонение
            residuals = close_prices - y_pred
            current_std = np.std(residuals)
            
            # Записываем значения для последнего бара в окне
            result_df.at[result_df.index[i], 'regression_line'] = y_pred[-1]
            result_df.at[result_df.index[i], 'upper_channel'] = y_pred[-1] + std_dev * current_std
            result_df.at[result_df.index[i], 'lower_channel'] = y_pred[-1] - std_dev * current_std
            result_df.at[result_df.index[i], 'regression_slope'] = slope
            result_df.at[result_df.index[i], 'residual_std'] = current_std
            
        except (TypeError, np.linalg.LinAlgError) as e:
            continue
    
    # Интерполируем пропущенные значения для визуализации
    result_df['regression_line'] = result_df['regression_line'].interpolate(method='linear')
    result_df['upper_channel'] = result_df['upper_channel'].interpolate(method='linear')
    result_df['lower_channel'] = result_df['lower_channel'].interpolate(method='linear')
    
    # Рассчитываем нормализованный наклон
    result_df['norm_slope'] = np.tanh(result_df['regression_slope'])
    
    return result_df

def add_dynamic_trend_lines_extended(df: pd.DataFrame, min_points=2, divider=60):
    """
    Полностью оптимизированная версия без фрагментации DataFrame
    """
    # Создаем копию DataFrame для работы
    result_df = df.copy()
    num_lines = max(len(result_df.index) // divider, 1)
    
    # 1. Подготовка: создаем все необходимые колонки в одном новом DataFrame
    new_data = {}
    
    # Колонки для трендовых линий
    for i in range(1, num_lines + 1):
        new_data[f'trend_line_up_{i}'] = np.nan
        new_data[f'trend_line_down_{i}'] = np.nan
        new_data[f'slope_up_{i}'] = np.nan
        new_data[f'slope_down_{i}'] = np.nan
    
    # Основные результирующие колонки
    new_data.update({
        'trend_up_combined': np.nan,
        'trend_down_combined': np.nan,
        'trend_up_slope': np.nan,
        'trend_down_slope': np.nan
    })
    
    # Создаем новый DataFrame с нужными колонками
    trend_data = pd.DataFrame(new_data, index=result_df.index)
    
    # 2. Находим все экстремумы заранее
    def find_extremes(values, mode='min'):
        extremes = []
        for i in range(1, len(values) - 1):
            if mode == 'min':
                if values[i] < values[i-1] and values[i] < values[i+1]:
                    extremes.append(i)
            else:
                if values[i] > values[i-1] and values[i] > values[i+1]:
                    extremes.append(i)
        return extremes
    
    up_points = find_extremes(result_df['low'].values, 'min')
    down_points = find_extremes(result_df['high'].values, 'max')

    # 3. Обработка восходящих трендов
    if len(up_points) >= min_points:
        step = max(len(up_points) // num_lines, 1)
        
        for line_num in range(num_lines):
            start = line_num * step
            end = (line_num + 1) * step if line_num < num_lines - 1 else len(up_points)
            group = up_points[start:end]
            
            if len(group) >= min_points:
                x = np.array(group)
                y = result_df['low'].iloc[group].values
                coeffs = np.polyfit(x, y, 1)
                
                # Определяем диапазон до следующего тренда
                line_start = group[0]
                next_start = up_points[end] if end < len(up_points) else len(result_df)
                
                # Вычисляем значения для всей линии
                x_range = np.arange(line_start, next_start)
                line_values = np.polyval(coeffs, x_range)
                
                # Заполняем данные
                trend_data.loc[line_start:next_start-1, f'trend_line_up_{line_num+1}'] = line_values
                trend_data.loc[line_start:next_start-1, f'slope_up_{line_num+1}'] = coeffs[0]

    # 4. Обработка нисходящих трендов (аналогично)
    if len(down_points) >= min_points:
        step = max(len(down_points) // num_lines, 1)
        
        for line_num in range(num_lines):
            start = line_num * step
            end = (line_num + 1) * step if line_num < num_lines - 1 else len(down_points)
            group = down_points[start:end]
            
            if len(group) >= min_points:
                x = np.array(group)
                y = result_df['high'].iloc[group].values
                coeffs = np.polyfit(x, y, 1)
                
                line_start = group[0]
                next_start = down_points[end] if end < len(down_points) else len(result_df)
                
                x_range = np.arange(line_start, next_start)
                line_values = np.polyval(coeffs, x_range)
                
                trend_data.loc[line_start:next_start-1, f'trend_line_down_{line_num+1}'] = line_values
                trend_data.loc[line_start:next_start-1, f'slope_down_{line_num+1}'] = coeffs[0]

    # 5. Объединение линий
    up_cols = [f'trend_line_up_{i}' for i in range(1, num_lines+1)]
    down_cols = [f'trend_line_down_{i}' for i in range(1, num_lines+1)]
    
    trend_data['trend_up_combined'] = trend_data[up_cols].mean(axis=1)
    trend_data['trend_down_combined'] = trend_data[down_cols].mean(axis=1)
    
    # 6. Заполнение slope последней активной линии
    for i in range(1, num_lines+1):
        # Для восходящих
        mask = ~trend_data[f'slope_up_{i}'].isna()
        trend_data.loc[mask, 'trend_up_slope'] = trend_data.loc[mask, f'slope_up_{i}']
        
        # Для нисходящих
        mask = ~trend_data[f'slope_down_{i}'].isna()
        trend_data.loc[mask, 'trend_down_slope'] = trend_data.loc[mask, f'slope_down_{i}']

    # 7. Удаление временных колонок
    cols_to_keep = [
        'trend_up_combined',
        'trend_down_combined',
        'trend_up_slope',
        'trend_down_slope'
    ]
    
    # 8. Объединяем с исходными данными
    result_df = pd.concat([result_df, trend_data[cols_to_keep]], axis=1)
    
    return result_df



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


def add_segmented_regression(df: pd.DataFrame, divider=60, std_dev=1.0, min_points=5):
    """
    'regression_line','upper_channel','lower_channel''regression_slope'
    Строит независимые линейные регрессии на каждом участке длиной divider баров
    с каналами стандартного отклонения
    
    Параметры:
        df - DataFrame с ценами
        divider - длина участка для каждой регрессии (в барах)
        std_dev - количество стандартных отклонений для каналов
        min_points - минимальное количество точек для построения регрессии
    """
    result_df = df.copy()
    
    # Создаем колонки для результатов
    result_df['regression_line'] = np.nan
    result_df['upper_channel'] = np.nan
    result_df['lower_channel'] = np.nan
    result_df['regression_slope'] = np.nan
    
    # Разбиваем данные на сегменты по divider баров
    for i in range(0, len(result_df), divider):
        segment_start = i
        segment_end = min(i + divider, len(result_df))
        segment = result_df.iloc[segment_start:segment_end]
        
        # Проверяем, что в сегменте достаточно точек
        if len(segment) < min_points:
            continue
            
        x = np.arange(len(segment))
        close_prices = segment['close'].values
        
        try:
            # Строим линейную регрессию для сегмента
            coeffs = np.polyfit(x, close_prices, 1)
            slope = coeffs[0]
            intercept = coeffs[1]
            
            # Вычисляем предсказанные значения и стандартное отклонение
            y_pred = np.polyval(coeffs, x)
            residuals = close_prices - y_pred
            current_std = np.std(residuals)
            
            # Заполняем значения для всего сегмента
            result_df.loc[result_df.index[segment_start:segment_end], 'regression_line'] = y_pred
            result_df.loc[result_df.index[segment_start:segment_end], 'upper_channel'] = y_pred + std_dev * current_std
            result_df.loc[result_df.index[segment_start:segment_end], 'lower_channel'] = y_pred - std_dev * current_std
            result_df.loc[result_df.index[segment_start:segment_end], 'regression_slope'] = slope
            
        except (TypeError, np.linalg.LinAlgError) as e:
            continue
    
    # Рассчитываем нормализованный наклон
    result_df['norm_slope'] = np.tanh(result_df['regression_slope'])
    
    return result_df

# Тема
def add_segmented_regression_from_end(df: pd.DataFrame, divider=60, std_dev=1.0, min_points=5):
    """
    'regression_line','upper_channel','lower_channel','regression_slope'
    Строит независимые линейные регрессии на каждом участке длиной divider баров,
    начиная с конца датафрейма, с каналами стандартного отклонения
    
    Параметры:
        df - DataFrame с ценами
        divider - длина участка для каждой регрессии (в барах)
        std_dev - количество стандартных отклонений для каналов
        min_points - минимальное количество точек для построения регрессии
    """
    result_df = df.copy()
    
    # Создаем колонки для результатов
    result_df['regression_line'] = np.nan
    result_df['upper_channel'] = np.nan
    result_df['lower_channel'] = np.nan
    result_df['regression_slope'] = np.nan
    
    # Идем с конца датафрейма к началу
    for i in range(len(result_df), 0, -divider):
        segment_end = i
        segment_start = max(0, i - divider)
        segment = result_df.iloc[segment_start:segment_end]
        
        # Проверяем, что в сегменте достаточно точек
        if len(segment) < min_points:
            continue
            
        x = np.arange(len(segment))
        close_prices = segment['close'].values
        
        try:
            # Строим линейную регрессию для сегмента
            coeffs = np.polyfit(x, close_prices, 1)
            slope = coeffs[0]
            intercept = coeffs[1]
            
            # Вычисляем предсказанные значения и стандартное отклонение
            y_pred = np.polyval(coeffs, x)
            residuals = close_prices - y_pred
            current_std = np.std(residuals)
            
            # Заполняем значения для всего сегмента
            result_df.loc[result_df.index[segment_start:segment_end], 'regression_line'] = y_pred
            result_df.loc[result_df.index[segment_start:segment_end], 'upper_channel'] = y_pred + std_dev * current_std
            result_df.loc[result_df.index[segment_start:segment_end], 'lower_channel'] = y_pred - std_dev * current_std
            result_df.loc[result_df.index[segment_start:segment_end], 'regression_slope'] = slope
            
        except (TypeError, np.linalg.LinAlgError) as e:
            continue
    
    # Рассчитываем нормализованный наклон
    result_df['norm_slope'] = np.tanh(result_df['regression_slope'])
    
    return result_df