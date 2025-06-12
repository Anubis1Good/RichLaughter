import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from Loader.BitgetLoader import bitget_loader
from utils.draw_utils import draw_lite_chart,draw_chart_channel,draw_hb_chart_fast,draw_bollinger,draw_dynamics,draw_rails
from ForBots.Indicators.classic_indicators import *
from ForBots.Indicators.vsa_indicators import *
from ForBots.Indicators.rare_indicators import *
from ForBots.Indicators.pva_indicators import *
from ForBots.Indicators.van_indicators import *
from ForBots.Indicators.ml_indicators import *
from scipy.stats import linregress

raw_file = 'DataForTests\DataFromBitget\DOGEUSDT_1m_1739873922.csv'
raw_file = 'DataForTests\DataFromMOEX\MMM5_1_1749581140.csv'
# raw_file = 'DataForTests\oldMoex\SiM5_1_1745579847.csv'
period = 10
df = bitget_loader(raw_file)
df = df.iloc[-200:]
# df = df.iloc[10:510]

import pandas as pd
import numpy as np

def dynamic_zigzag(df, source='high_low', n_std=1.5, method='std', period=20):
    """
    ZigZag с динамическим reversal на основе волатильности
    
    Параметры:
    df - DataFrame с колонками: high, low, close
    source - 'high_low' (по экстремумам) или 'close' (по ценам закрытия)
    n_std - множитель для std или среднего (1.5 по умолчанию)
    method - 'std' (стандартное отклонение) или 'mean' (средний диапазон)
    period - период для расчета волатильности
    """
    df = df.copy()
    
    # Проверка на достаточное количество данных
    if len(df) < period:
        raise ValueError(f"Недостаточно данных. Требуется минимум {period} баров")
    
    # Выбор источника данных
    if source == 'high_low':
        prices = df[['high', 'low']].values
    elif source == 'close':
        prices = df[['close', 'close']].values
    else:
        raise ValueError("source должен быть 'high_low' или 'close'")
    
    highs = prices[:, 0]
    lows = prices[:, 1]
    size = len(df)
    
    # Расчет динамического порога разворота
    if method == 'std':
        rolling_std = df['close'].rolling(period).std().bfill()
        reversal_values = rolling_std * n_std
    elif method == 'mean':
        ranges = df['high'] - df['low']
        reversal_values = ranges.rolling(period).mean().bfill() * n_std
    else:
        raise ValueError("method должен быть 'std' или 'mean'")
    
    # Инициализация массивов
    zz = np.full(size, np.nan)
    direction = np.zeros(size, dtype=np.int8)  # 1=up, -1=down
    
    # Начальные условия (используем первые доступные значения)
    first_valid = max(1, period-1)  # Первый валидный индекс после заполнения rolling
    direction[:first_valid] = 1
    last_pivot = highs[first_valid]
    last_pivot_idx = first_valid
    zz[first_valid] = last_pivot
    
    for i in range(first_valid+1, size):
        high = highs[i]
        low = lows[i]
        reversal = reversal_values.iloc[i]  # Используем iloc для безопасного доступа
        
        if direction[i-1] == 1:  # Предыдущее направление - вверх
            # Обновляем максимум
            if high > last_pivot:
                zz[last_pivot_idx] = np.nan  # Удаляем старый максимум
                last_pivot = high
                last_pivot_idx = i
                zz[i] = last_pivot
            
            # Проверяем разворот
            threshold = last_pivot - reversal
            if low <= threshold:
                direction[i] = -1
                last_pivot = low
                last_pivot_idx = i
                zz[i] = last_pivot
            else:
                direction[i] = 1
                
        else:  # Предыдущее направление - вниз
            # Обновляем минимум
            if low < last_pivot:
                zz[last_pivot_idx] = np.nan  # Удаляем старый минимум
                last_pivot = low
                last_pivot_idx = i
                zz[i] = last_pivot
            
            # Проверяем разворот
            threshold = last_pivot + reversal
            if high >= threshold:
                direction[i] = 1
                last_pivot = high
                last_pivot_idx = i
                zz[i] = last_pivot
            else:
                direction[i] = -1
    
    # Соединяем точки линиями
    zz_final = np.full(size, np.nan)
    start_idx = None
    start_val = np.nan
    
    for i in range(size):
        if not np.isnan(zz[i]):
            if start_idx is not None:
                # Линейная интерполяция между точками
                zz_final[start_idx:i+1] = np.linspace(start_val, zz[i], i - start_idx + 1)
            start_idx = i
            start_val = zz[i]
    
    df['zigzag'] = zz_final
    df['zigzag_direction'] = direction
    df['reversal_threshold'] = reversal_values
    return df

df = dynamic_zigzag(df,method='mean',n_std=3)

# Пример использования
# df = pd.read_csv('your_data.csv')
# print(df[['high', 'low', 'direction', 'last_extreme']].head())


# plt.subplot(2,1,1)
plt.grid() 
draw_hb_chart_fast(df)
# plt.plot(df['zigzag_line'])
# plt.plot(df['top_line'])
# plt.plot(df['bottom_line'])
# plt.plot(df['regression_line'])
# plt.plot(df['stair'])
# plt.plot(df['trend'])
plt.plot(df['zigzag'])
# plt.plot(df['stair_up'])

# for k in ('fractal_up','fractal_down'):
#     plt.plot(df[k])
# for k in 'max_hb, min_hb, avarege'.split(', '):
# ax1 = plt.gca()
# plt.subplot(2,1,2,sharex=ax1)
# plt.grid() 
# plt.plot(df['ami'])
# plt.plot(df['ami_filter'])
# plt.plot(df['ii'])
# plt.plot(df['market_mode'])


# for k in ( 'trend_up','trend_down'):
# # for k in 'PP, R1, R2, S1, S2'.split(', '):
# #     plt.plot(df[k],color='g')
# for k in 'max_hb, min_hb, avarege'.split(', '):
#     plt.plot(df[k],color='b')
# for k in df.columns:
#     if  'zigzag' in k:
#         plt.plot(df[k])
# for k in 'trend_up_slope, trend_down_slope'.split(', '):
# for k in ('regression_slope',):
# plt.plot(df['rsi'])
print(df.tail())
plt.show()