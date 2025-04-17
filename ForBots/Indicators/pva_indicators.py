import numpy as np
import pandas as pd
from ForBots.Indicators.help_pva_indicators import add_touch_signals,calculate_changes,calculate_cumulative_changes

def add_benefit(df,all_starts,all_ends,id,period=60):
    """add bl_+id,bs+id"""
    df = add_touch_signals(df,all_starts,all_ends,id)
    df = calculate_changes(df,id)
    df = calculate_cumulative_changes(df,id)
    df['bl_'+id] = df['cum_long_'+id].diff().rolling(period).mean()
    df['bs_'+id] = df['cum_short_'+id].diff().rolling(period).mean()
    df['bl_'+id] = df['bl_'+id].fillna(0)
    df['bs_'+id] = df['bs_'+id].fillna(0)
    drops = []
    for c in ('touch_','change_long_','change_short_','cum_long_','cum_short_'):
        drops.append(c+id)
    df = df.drop(drops,axis=1)
    return df

def add_velcro_indicator(df,period_check=10):
    '''add velcro'''
    df['delta_h'] = df['max_hb'] - df['high']
    df['delta_l'] = df['low'] - df['min_hb']
    df['lis'] = df['delta_l'].rolling(period_check).mean()
    df['his'] = df['delta_h'].rolling(period_check).mean()

    df['sis'] = df['lis'] + df['his']

    df['velcro'] = (df['lis'] / df['sis'])*100
    return df

# TODO
def add_market_mode(df,period_check=10,period_frequency=5):
    '''add market_mode'''
    df['delta_h'] = df['max_hb'] - df['high']
    df['delta_l'] = df['low'] - df['min_hb']
    df['lis'] = df['delta_l'].rolling(period_check).mean()
    df['his'] = df['delta_h'].rolling(period_check).mean()

    df['sis'] = df['lis'] + df['his']

    df['li'] = (df['lis'] / df['sis'])*100

    df['cross_above'] = (df['li'] > 50) & (df['li'].shift(1) <= 50)  # Пересечение снизу вверх
    df['cross_below'] = (df['li'] < 50) & (df['li'].shift(1) >= 50)  # Пересечение сверху вниз

    # Считаем количество пересечений за последние N периодов
    lookback_period = period_frequency # Период для расчета частоты
    df['total_crosses'] = (df['cross_above'] | df['cross_below']).rolling(lookback_period).sum()
    df['cross_frequency'] = df['total_crosses'] / lookback_period  # Нормированная частота

    # Считаем отдельно для бычьих и медвежьих пересечений
    df['bull_crosses'] = df['cross_above'].rolling(lookback_period).sum()
    df['bear_crosses'] = df['cross_below'].rolling(lookback_period).sum()

    # Индикатор "Режим рынка" на основе частоты
    df['market_mode'] = np.select(
        [df['cross_frequency'] > 0.7, df['cross_frequency'] < 0.3],
        [0, 2],
        default=1
    )
    return df

def add_kvas_channel(df:pd.DataFrame,period=20):
    df['delta_p'] = (df['close'] - df['close'].shift(period))
    df['top_kvas'] = df['high'].rolling(period).max() + df['delta_p']
    df['low_kvas'] = df['low'].rolling(period).min() + df['delta_p']
    return df

def add_kefir_channel(df:pd.DataFrame,period=20):
    df['delta_p'] = df['close'] - df['close'].shift(period)
    df['delta_t'] = df['delta_p'].shift(period).rolling(period).max()
    df['delta_l'] = df['delta_p'].shift(period).rolling(period).min()
    df['top_kefir'] = df['high'].rolling(period).max() + df['delta_t']
    df['low_kefir'] = df['low'].rolling(period).min() + df['delta_l']
    return df



def add_hl_stair_fast(df: pd.DataFrame, n=3, period=20):
    df = df.copy()
    high = df['high'].values
    low = df['low'].values

    # Предварительные расчеты
    spread = high - low
    threshold_break = pd.Series(spread).rolling(period).mean().fillna(0).values * n

    # Инициализация массивов
    size = len(df)
    last_dir = np.ones(size, dtype=np.int8)
    last_high = np.zeros(size)
    last_low = np.zeros(size)

    # Начальные значения
    last_high[0] = high[0]
    last_low[0] = low[0]

    # Основной цикл
    for i in range(1, size):
        current_dir = last_dir[i-1]
        current_high = last_high[i-1]
        current_low = last_low[i-1]
        th = threshold_break[i]
        h = high[i]
        l = low[i]

        if current_dir == 1:
            new_high = max(h, current_high)
            if l <= (new_high - th):
                current_dir = -1
                new_low = l
            else:
                new_low = current_low
        else:
            new_low = min(l, current_low)
            if h >= (new_low + th):
                current_dir = 1
                new_high = h
            else:
                new_high = current_high

        last_dir[i] = current_dir
        last_high[i] = new_high
        last_low[i] = new_low

    # Отмечаем точки разворота
    dir_changes = np.diff(last_dir, prepend=0) != 0
    df['stair'] = np.where(dir_changes, np.where(last_dir == -1, high, low), np.nan)
    
    # Заполняем значения вперед
    df['stair'] = df['stair'].ffill()
    return df

def add_pc_stair_fast(df: pd.DataFrame, n=3, period=20):
    df = df.copy()
    close = df['close'].values
    high = df['high'].values
    low = df['low'].values
    
    # Предварительные расчеты
    prev_close = np.roll(close, 1)
    prev_close[0] = close[0]
    
    spread = high - low
    threshold_break = pd.Series(spread).rolling(period).mean().fillna(0).values * n
    
    # Инициализация массивов состояний
    size = len(df)
    last_dir = np.ones(size, dtype=np.int8)
    last_high = np.empty(size)
    last_low = np.empty(size)
    
    # Начальные значения
    last_high[0] = prev_close[0]
    last_low[0] = prev_close[0]
    
    # Основной цикл (оптимизированный)
    for i in range(1, size):
        current_dir = last_dir[i-1]
        current_high = last_high[i-1]
        current_low = last_low[i-1]
        th = threshold_break[i]
        pc = prev_close[i]
        
        if current_dir == 1:
            new_high = max(pc, current_high)
            if pc <= (new_high - th):
                current_dir = -1
                new_low = pc
            else:
                new_low = current_low
        else:
            new_low = min(pc, current_low)
            if pc >= (new_low + th):
                current_dir = 1
                new_high = pc
            else:
                new_high = current_high
        
        last_dir[i] = current_dir
        last_high[i] = new_high
        last_low[i] = new_low
    
    # Построение финального индикатора
    dir_changes = np.where(np.diff(last_dir, prepend=last_dir[0]) != 0)[0]
    stair = np.full(size, np.nan)
    stair[dir_changes] = prev_close[dir_changes]
    
    df['stair'] = pd.Series(stair).ffill()
    return df