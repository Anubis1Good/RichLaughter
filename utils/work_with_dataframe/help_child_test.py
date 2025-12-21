import pandas as pd
import numpy as np

def get_child_candles(df:pd.DataFrame,x):
    candels = []
    df = df.copy()
    df = df.reset_index(drop=True)
    for i,row in df.iterrows():
        if i == 0:
            candel = row
            candel['x'] = x
        else:
            candel['close'] = row['close']
            candel['volume'] += row['volume']
            candel['high'] = max(candel['high'],row['high'])
            candel['low'] = min(candel['low'],row['low'])
            candel['middle'] = (candel['high'] + candel['low']) / 2
            candel['direction'] = 1 if candel['open'] < candel['close'] else -1
        candels.append(candel.copy())
    # print('gcc',len(candels))
    return candels

def convert_datetime_CT(series,datetime_col='ms'):
    """
    Умное преобразование временного ряда в datetime для ChildTest.
    Определяет формат автоматически: timestamp (мс/с) или строки.
    """
    # Проверяем, является ли серия уже datetime
    if pd.api.types.is_datetime64_any_dtype(series):
        return series
        
    # Пробуем определить, являются ли данные числовыми (timestamp)
    if pd.api.types.is_numeric_dtype(series):
        # Определяем масштаб: если числа очень большие (>1e12) - это мс, иначе - секунды
        sample_value = series.iloc[0] if len(series) > 0 else 0
        if sample_value > 1e12:  # Это миллисекунды
            return pd.to_datetime(series, unit='ms')
        else:  # Это секунды
            return pd.to_datetime(series, unit='s')
    else:
        # Пробуем преобразовать строки стандартным методом
        try:
            return pd.to_datetime(series)
        except:
            # Если не получается, пробуем парсить как timestamp в строковом формате
            try:
                return pd.to_datetime(series.astype(np.int64), unit='ms')
            except:
                raise ValueError(f"Не удалось преобразовать столбец {datetime_col} в datetime")