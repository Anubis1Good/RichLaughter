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