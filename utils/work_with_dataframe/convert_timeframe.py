import os
import pandas as pd

def convert_chart1to5(df):
    # Преобразуем столбец 'ms' в datetime
    df['ms'] = pd.to_datetime(df['ms'])

    # Устанавливаем 'ms' в качестве индекса
    df.set_index('ms', inplace=True)

    # Агрегируем данные по пятиминутным интервалам
    df_5min = df.resample('5min').agg({
        'open': 'first',        # Первое значение 'open' в интервале
        'close': 'last',        # Последнее значение 'close' в интервале
        'high': 'max',          # Максимальное значение 'high' в интервале
        'low': 'min',           # Минимальное значение 'low' в интервале
        'vol_coin': 'sum',      # Сумма 'vol_coin' в интервале
        'volume': 'sum',        # Сумма 'volume' в интервале
        'direction': 'last',    # Последнее значение 'direction' в интервале
        'middle': 'last',       # Последнее значение 'middle' в интервале
        'x': 'last'             # Последнее значение 'x' в интервале
    }).dropna()
    df_5min['direction'] = (df_5min['open'] - df_5min['close']).apply(lambda x: 1 if x <= 0 else -1)
    df_5min['middle'] = (df_5min['high'] + df_5min['low']) / 2
    # Сбрасываем индекс, чтобы 'ms' снова стал столбцом
    df_5min.reset_index(inplace=True)
    df_5min['x'] = df_5min.index
    return df_5min


def convert_timeframe(df, timeframe, agg_rules=None, datetime_col='ms', recalc_direction=True, recalc_middle=True) -> pd.DataFrame:
    """
    Универсальная функция для агрегации временных рядов в заданный таймфрейм.
    
    Параметры:
    ----------
    df : pandas.DataFrame
        Входной DataFrame с временным рядом
    timeframe : str
        Строка интервала агрегации (например, '5min', '1H', '1D')
    agg_rules : dict, optional
        Словарь с правилами агрегации для каждого столбца.
        По умолчанию: стандартные правила для OHLCV данных
    datetime_col : str, optional
        Название столбца с датой/временем (по умолчанию 'ms')
    recalc_direction : bool, optional
        Пересчитывать ли направление свечи (по умолчанию True)
    recalc_middle : bool, optional
        Пересчитывать ли середину свечи (по умолчанию True)
    
    Возвращает:
    -----------
    pandas.DataFrame
        DataFrame с агрегированными данными
    """
    
    # Стандартные правила агрегации, если не заданы пользователем
    default_agg_rules = {
        'open': 'first',
        'close': 'last',
        'high': 'max',
        'low': 'min',
        'vol_coin': 'sum',
        'volume': 'sum',
        'direction': 'last',
        'middle': 'last',
        'x': 'last'
    }
    
    # Объединяем пользовательские правила с стандартными (пользовательские имеют приоритет)
    if agg_rules is None:
        agg_rules = default_agg_rules
    else:
        for col in default_agg_rules:
            if col not in agg_rules:
                agg_rules[col] = default_agg_rules[col]
    
    # Копируем DataFrame, чтобы не изменять исходный
    df = df.copy()
    
    # Преобразуем столбец времени в datetime, если он еще не в этом формате
    if not pd.api.types.is_datetime64_any_dtype(df[datetime_col]):
        df[datetime_col] = pd.to_datetime(df[datetime_col])
    
    # Устанавливаем временной столбец в качестве индекса
    df.set_index(datetime_col, inplace=True)
    
    # Агрегируем данные по заданному интервалу
    df_resampled = df.resample(timeframe).agg(agg_rules).dropna()
    
    # Пересчитываем дополнительные поля, если нужно
    if recalc_direction and 'open' in df_resampled and 'close' in df_resampled:
        df_resampled['direction'] = (df_resampled['close'] - df_resampled['open']).apply(
            lambda x: 1 if x >= 0 else -1)
    
    if recalc_middle and 'high' in df_resampled and 'low' in df_resampled:
        df_resampled['middle'] = (df_resampled['high'] + df_resampled['low']) / 2
    
    # Сбрасываем индекс, чтобы временной столбец снова стал обычным столбцом
    df_resampled.reset_index(inplace=True)
    
    # Обновляем индексный столбец x, если он есть в данных
    if 'x' in df_resampled:
        df_resampled['x'] = df_resampled.index
    
    return df_resampled

if __name__ == "__main__":
    # folder = 'DataForTests\DataFromMOEX'
    folder = 'DataForTests\DataFromMoexForStepTests'
    # folder = 'DataForTests\otherMOEX'
    listdir = os.listdir(folder)
    # output_folder = 'DataForTests\DataFromMOEXto5'
    output_folder = folder
    for f in listdir:
        filepath = os.path.join(folder,f)
        df = pd.read_csv(filepath)
        # df = convert_chart1to5(df)
        df = convert_timeframe(df,'15min')
        new_path = os.path.join(output_folder,'15'+f)
        df.to_csv(new_path)