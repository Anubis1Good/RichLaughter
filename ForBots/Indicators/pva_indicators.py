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

#TAKE THIS
def add_kvas_channel(df:pd.DataFrame,period=20):
    """add 'top_kvas','low_kvas'"""
    df['delta_p'] = (df['close'] - df['close'].shift(period))
    df['top_kvas'] = df['high'].rolling(period).max() + df['delta_p']
    df['low_kvas'] = df['low'].rolling(period).min() + df['delta_p']
    return df

#NEED EXPERIMENT
def add_kefir_channel(df:pd.DataFrame,period=20):
    """add 'top_kefir','low_kefir'"""
    df['delta_p'] = df['close'] - df['close'].shift(period)
    df['delta_t'] = df['delta_p'].shift(period).rolling(period).max()
    df['delta_l'] = df['delta_p'].shift(period).rolling(period).min()
    df['top_kefir'] = df['high'].rolling(period).max() + df['delta_t']
    df['low_kefir'] = df['low'].rolling(period).min() + df['delta_l']
    return df



def add_hl_stair_fast(df: pd.DataFrame, n=3, period=20):
    """ add 'stair'
    """
    df = df.copy()
    df = df.reset_index(drop=True)
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
    """ add 'stair'
    """
    df = df.copy()
    df = df.reset_index(drop=True)
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

def add_integrity_index(df:pd.DataFrame,period:int=14):
    """add 'ii'"""
    df['spred'] = df['high'] - df['low']
    df['integrity'] = np.where(df['direction'] == 1, df['spred'],-df['spred'])
    df['ii'] = (df['integrity'].rolling(period).sum() / np.abs(df['integrity']).rolling(period).sum()) * 100
    df = df.drop(['spred','integrity'],axis=1)
    return df

def add_cascade_channel(df: pd.DataFrame, n=3, period=20,period_smooth=100):
    """ add 'stair','top_line','bottom_line'
    """
    df = df.copy()
    df = df.reset_index(drop=True)
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
    df['top_line'] = (df['stair'] + threshold_break).rolling(period_smooth,1).median()
    df['bottom_line'] = (df['stair'] - threshold_break).rolling(period_smooth,1).median()
    
    return df

def add_static_channel(df:pd.DataFrame,period=60):
    """add 'center_line', 'top_line', 'bottom_line'"""
    df['center_line'] = df['close'].rolling(period,1).quantile(0.5)
    df['top_line'] = df['close'].rolling(period,1).quantile(0.9)
    df['bottom_line'] = df['close'].rolling(period,1).quantile(0.1)
    return df

#check thos
def add_assessment_motion_index(df:pd.DataFrame,period=100,period_filter=50):
    """add 'ami', 'ami_filter'"""
    df['ami'] = (((df['avarege'].diff().rolling(period,1).sum())/ np.abs(df['avarege'].diff()).rolling(period).sum())*100).round(2)
    df['ami_filter'] = df['ami'].rolling(period_filter).mean()
    return df

def add_hope_channel(df: pd.DataFrame, n=3, period=100,shift=10):
    """ add 'stair','top_line','bottom_line'
    """
    df = df.copy()
    df = df.reset_index(drop=True)
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
    df['stair'] = pd.Series(stair).shift(shift)
    df['top_line'] = df['stair'] + threshold_break
    df['bottom_line'] = df['stair'] - threshold_break
    df['stair'] = df['stair'].ffill()
    df['top_line'] = df['top_line'].ffill()
    df['bottom_line'] = df['bottom_line'].ffill()
    return df

def add_delta_fractals(df: pd.DataFrame, period=1, period_fractals=5):
    """Оптимизированная версия с расчетом верхних и нижних фракталов"""
    
    # Создаем копии для безопасного изменения
    df = df.copy()
    
    # Обработка верхних фракталов
    up_mask = df['fractal_up']
    df['h_up'] = df.loc[up_mask, 'high'].reindex(df.index).ffill()
    
    up_points = df[up_mask].copy()
    up_deltas = (up_points['high'].diff() / up_points.index.to_series().diff()).rolling(period).mean()
    df['delta_up'] = up_deltas.reindex(df.index)
    
    # Кумулятивная сумма с reset по новым delta_up
    df['cum_temp_up'] = df['delta_up'].ffill()
    df['cum_temp_up'] = df.groupby(df['delta_up'].notna().cumsum())['cum_temp_up'].cumsum()
    df['fd_up'] = (df['h_up'] + df['cum_temp_up']).shift(period_fractals)
    
    # Обработка нижних фракталов
    down_mask = df['fractal_down']
    df['l_down'] = df.loc[down_mask, 'low'].reindex(df.index).ffill()
    
    down_points = df[down_mask].copy()
    down_deltas = (down_points['low'].diff() / down_points.index.to_series().diff()).rolling(period).mean()
    df['delta_down'] = down_deltas.reindex(df.index)
    
    # Кумулятивная сумма с reset по новым delta_down
    df['cum_temp_down'] = df['delta_down'].ffill()
    df['cum_temp_down'] = df.groupby(df['delta_down'].notna().cumsum())['cum_temp_down'].cumsum()
    df['fd_down'] = (df['l_down'] + df['cum_temp_down']).shift(period_fractals)
    
    # Удаляем промежуточные колонки
    cols_to_drop = ['h_up', 'l_down', 'delta_up', 'delta_down', 'cum_temp_up', 'cum_temp_down']
    return df.drop(columns=cols_to_drop)

# good indicator
def add_std_fractals_channel(df:pd.DataFrame, period=5,period_sma=10):
    """add 'std_up', 'std_down', 'sma'"""
    df['sma'] = df['middle'].rolling(period_sma).mean()
    up_points = df[df['fractal_up']]
    df['std_up'] = up_points['high'].rolling(window=period).std()
    df['std_up'] = df['std_up'].ffill() + df['sma']
    down_points = df[df['fractal_down']]
    df['std_down'] = down_points['low'].rolling(window=period).std()
    df['std_down'] = df['sma'] - df['std_down'].ffill() 
    return df

#good indicator
def add_mean_on_fractals(df,period=5,kind='rsi'):
    """add 'top_mean', bottom_mean'"""
    ups = df[df['fractal_up']]
    df['top_mean'] = ups[kind].rolling(period).mean()
    df['top_mean'] = df['top_mean'].ffill()
    downs = df[df['fractal_down']]
    df['bottom_mean'] = downs[kind].rolling(period).mean()
    df['bottom_mean'] = df['bottom_mean'].ffill()
    return df

#?good indicator
def add_diffmean_fractals_channel(df,period=2,kind='sma'):
    """add 'dmu', 'dmd'"""
    ups = df[df['fractal_up']]
    top_mean = ups[kind].rolling(period).mean()
    df['dmu'] = top_mean - ups['high']
    df['dmu'] = df['dmu'].ffill()
    df['dmu'] = df[kind] - df['dmu'] 
    downs = df[df['fractal_down']]
    bottom_mean = downs[kind].rolling(period).mean()
    df['dmd'] = bottom_mean - downs['low']
    df['dmd'] = df['dmd'].ffill()
    df['dmd'] = df[kind] - df['dmd'] 
    return df
#?good indicator
def add_sdiffmean_fractals_channel(df,period=2,kind='sma',period_smooth=20):
    """add 'sdmu', 'sdmd'"""
    df = add_diffmean_fractals_channel(df,period,kind)
    df['sdmu'] = df['dmu'].rolling(period_smooth).mean()
    df['sdmd'] = df['dmd'].rolling(period_smooth).mean()
    return df

#good indicator
def add_ext_on_fractals(df,period=5,kind='rsi'):
    """add 'top_ext', bottom_ext'"""
    ups = df[df['fractal_up']]
    df['top_ext'] = ups[kind].rolling(period).max()
    df['top_ext'] = df['top_ext'].ffill()
    downs = df[df['fractal_down']]
    df['bottom_ext'] = downs[kind].rolling(period).min()
    df['bottom_ext'] = df['bottom_ext'].ffill()
    return df

#good indicator
def add_analys_dzz(df, period_sma=3):
    """add 'trend','trend_sma'"""
    # Создаем явную копию DataFrame
    df = df.copy()
    df['trend'] = np.nan
    
    # Создаем копию для работы с пиками
    peacks = df[~df['zigzag_peaks'].isna()].copy()  # Явное копирование
    
    if len(peacks) < 4:
        df['trend'] = 0
        df['trend_sma'] = 0
        return df
    
    # Условия для тренда
    up_condition = (peacks['zigzag_peaks'] > peacks['zigzag_peaks'].shift(2)) & \
                  (peacks['zigzag_peaks'].shift(1) > peacks['zigzag_peaks'].shift(3))
    down_condition = (peacks['zigzag_peaks'] < peacks['zigzag_peaks'].shift(2)) & \
                    (peacks['zigzag_peaks'].shift(1) < peacks['zigzag_peaks'].shift(3))
    
    # Используем .loc для безопасного присвоения
    peacks.loc[:, 'trend'] = 0  # Инициализация через .loc
    peacks.loc[up_condition, 'trend'] = 1
    peacks.loc[down_condition, 'trend'] = -1
    
    # Считаем SMA
    peacks.loc[:, 'trend_sma'] = peacks['trend'].rolling(period_sma).mean()
    
    # Заполняем основной DataFrame
    df['trend'] = peacks['trend'].reindex(df.index).ffill().fillna(0)
    df['trend_sma'] = peacks['trend_sma'].reindex(df.index).ffill().fillna(0)
    
    return df

def add_smooth_channel(df:pd.DataFrame,period=20,smooth_features=('max_hb', 'min_hb', 'avarege'),variant_smooth='mean'):
    for sf in smooth_features:
        df[sf] = df[sf].rolling(period).agg([variant_smooth])
    return df

def add_plus_delta_fc(df:pd.DataFrame, period=1):
    """add 'pdf_up', 'pdf_down'
    \n plus delta fractal channel
    """
    up_points = df[df['fractal_up']].copy()
    up_points['delta_high'] = up_points['high'].diff()
    up_points['dhm'] = up_points['delta_high'].rolling(period).mean()
    df['pdf_up'] = up_points['high'] + up_points['dhm']
    df['pdf_up'] = df['pdf_up'].ffill()
    down_points = df[df['fractal_down']].copy()
    down_points['delta_low'] = down_points['low'].diff()
    down_points['dlm'] = down_points['delta_low'].rolling(period).mean()
    df['pdf_down'] = down_points['low'] + down_points['dlm']
    df['pdf_down'] = df['pdf_down'].ffill()
    return df

def add_exp_pdfc(df:pd.DataFrame, period=1):
    """add 'pdf_up', 'pdf_down'
    \n exponential plus delta fractal channel
    """
    up_points = df[df['fractal_up']].copy()
    up_points['delta_high'] = up_points['high'].diff()
    up_points['dhm'] = up_points['delta_high'].ewm(period).mean()
    df['pdf_up'] = up_points['high'] + up_points['dhm']
    df['pdf_up'] = df['pdf_up'].ffill()
    down_points = df[df['fractal_down']].copy()
    down_points['delta_low'] = down_points['low'].diff()
    down_points['dlm'] = down_points['delta_low'].ewm(period).mean()
    df['pdf_down'] = down_points['low'] + down_points['dlm']
    df['pdf_down'] = df['pdf_down'].ffill()
    return df