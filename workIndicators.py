import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from Loader.BitgetLoader import bitget_loader
from utils.draw_utils import draw_lite_chart,draw_chart_channel,draw_hb_chart_fast,draw_bollinger,draw_dynamics,draw_rails
from ForBots.Indicators.classic_indicators import *
from ForBots.Indicators.vsa_indicators import *
from ForBots.Indicators.rare_indicators import *
from scipy.stats import linregress

raw_file = 'DataForTests\DataFromBitget\DOGEUSDT_1m_1739873922.csv'
raw_file = 'DataForTests\DataFromMOEX\MMH5_1_1739993452.csv'
period = 10
df = bitget_loader(raw_file)
# df = df.iloc[-100:]
win = 240
df = df.iloc[win:win+200]
# df['mean_volume'] = df['volume'].rolling(10).mean()
# df['top_zone'] = np.where(df['volume'] > df['mean_volume']*2,df['high'],np.nan)
# df['bottom_zone'] = np.where(df['volume'] > df['mean_volume']*2,df['low'],np.nan)
# df['top_zone'] = df['top_zone'].ffill()
# df['bottom_zone'] = df['bottom_zone'].ffill()
import numpy as np
import pandas as pd
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
    Находит похожий паттерн и добавляет к последнему бару:
    - forecast_high: максимум прогноза.
    - forecast_low: минимум прогноза.
    """
    close_prices = df['close'].values
    
    # Проверка данных
    if len(df) < window + forecast_length:
        raise ValueError(f"Нужно минимум {window + forecast_length} баров, есть {len(df)}")
    
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
        raise ValueError("Не найдено подходящего паттерна.")
    
    # Масштабируем прогноз
    scale = current_std / best_past_std if best_past_std != 0 else 1
    forecast = (best_future - best_past_mean) * scale + current_mean
    
    # Записываем только highs/lows в последний бар
    df.loc[df.index[-1], 'forecast_high'] = np.max(forecast)
    df.loc[df.index[-1], 'forecast_low'] = np.min(forecast)
    df['per_fs'] = (((df['forecast_high'] - df['forecast_low']) / df['forecast_high']) * 100).round(2)
    return df

# df = add_find_similar_pattern(df)
df = add_find_similar_pattern_lite(df)
# df = add_donchan_channel(df,20)

# df = add_slice_df(df,14)
# plt.subplot(2,1,1)
# plt.grid() 
draw_hb_chart_fast(df)
plt.scatter(df.iloc[-1].name,df.iloc[-1]['forecast_high'])
plt.scatter(df.iloc[-1].name,df.iloc[-1]['forecast_low'])
print(df.tail())


def plot_pattern_forecast(df:pd.DataFrame, window=30):
    df = df.copy()
    df = df.reset_index(drop=True)
    fig, ax = plt.subplots(figsize=(15, 7))
    # Цена
    ax.plot(df.index, df['close'], label='Цена', color='black', lw=1.5)
    
    # Текущий паттерн
    current_start = df.index[-window]
    ax.axvspan(current_start, df.index[-1], color='red', alpha=0.1, label='Текущий паттерн')
    
    # Похожий паттерн
    if 'similar_pattern' in df.columns:
        similar_idx = df['similar_pattern'].first_valid_index()
        if similar_idx:
            similar_values = df.loc[similar_idx:similar_idx+window-1, 'similar_pattern']
            ax.plot(similar_values.index, similar_values, 'b-', label='Похожий паттерн', lw=2)
    
    # Прогноз
    if 'forecast' in df.columns:
        forecast_values = df['forecast'].dropna()
        ax.plot(forecast_values.index, forecast_values, 'g--', label='Прогноз', lw=2)
    
    ax.set_title('Прогноз на основе похожих паттернов')
    ax.legend()
    plt.show()
# plot_pattern_forecast(df)
# ax1 = plt.gca()
# plt.subplot(2,1,2,sharex=ax1)
# plt.grid() 
# for k in ('regression_slope',):
#     plt.plot(df[k])
# for k in ( 'regression_line','upper_channel','lower_channel'):
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
plt.show()