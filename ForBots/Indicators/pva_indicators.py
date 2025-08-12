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

def help_analiz_pattern18(row,threshold=0.2):
    if pd.isna(row['zp1']):
        return 'none_pattern'
    big = 1 + threshold
    small = 1 - threshold
    if row['r12_23'] > big:
        if row['r23_34'] > big:
            if row['p1_2'] > 0:
                return 'weak_short'
            else:
                return 'weak_long'
        elif row['r23_34'] < small:
            if row['p1_2'] > 0:
                return 'strong_short'
            else:
                return 'strong_long'
        else:
            if row['p1_2'] > 0:
                return 'enter_short_range'
            else:
                return 'enter_long_range'
    elif row['r12_23'] < small:
        if row['r23_34'] > big:
            if row['p1_2'] > 0:
                return 'btc'
            else:
                return 'bti'
        elif row['r23_34'] < small:
            if row['p1_2'] > 0:
                return 'sow'
            else:
                return 'sos'
        else:
            if row['p1_2'] > 0:
                return 'upthrust'
            else:
                return 'spring'
    else:
        if row['r23_34'] > big:
            if row['p1_2'] > 0:
                return 'narrowing_up'
            else:
                return 'narrowing_down'
        elif row['r23_34'] < small:
            if row['p1_2'] > 0:
                return 'bui'
            else:
                return 'joc'
        else:
            if row['p1_2'] > 0:
                return 'bottom_range'
            else:
                return 'top_range'
def add_my_pattern_dzz(df:pd.DataFrame, threshold=0.2):
    """add 'pattern18'"""
    # Создаем явную копию DataFrame
    df = df.copy()
    # Создаем копию для работы с пиками
    peacks = df[~df['zigzag_peaks'].isna()].copy()  # Явное копирование
    if len(peacks) < 4:
        df['pattern18'] = 'none_pattern'
        return df
    peacks['zp1'] = peacks['zigzag_peaks'].shift(3)
    peacks['zp2'] = peacks['zigzag_peaks'].shift(2)
    peacks['zp3'] = peacks['zigzag_peaks'].shift(1)
    peacks['zp4'] = peacks['zigzag_peaks']
    peacks['p1_2'] = peacks['zp1'] - peacks['zp2']
    peacks['p2_3'] = peacks['zp2'] - peacks['zp3']
    peacks['p3_4'] = peacks['zp3'] - peacks['zp4']
    peacks['r12_23'] = abs(peacks['p1_2'] / peacks['p2_3'])
    peacks['r23_34'] = abs(peacks['p2_3'] / peacks['p3_4'])
    peacks['pattern'] = peacks.apply(lambda row: help_analiz_pattern18(row,threshold),axis=1)
    df['pattern18'] = peacks['pattern']
    df['pattern18'] = df['pattern18'].ffill()
    
    return df

def add_pattern18_dzz(df: pd.DataFrame, threshold: float = 0.2, buffer_percent: float = 0.1) -> pd.DataFrame:
    """
    add 'pattern18', 'prev_pattern18', 
                'zp1', 'zp2', 'zp3', 'zp4',
                'bzp1', 'bzp2', 'bzp3', 'bzp4',
                'target', 'btarget', 'mzp' \n
    с классификацией паттернов зигзага и буферизованными точками
    patterns:
        'weak_short', 'weak_long',
        'bui', 'joc',
        'double_bottom', 'double_top',
        'btc', 'bti',
        'sow', 'sos',
        'upthrust', 'spring',
        'narrowing_up', 'narrowing_down',
        'bui', 'joc',
        'bottom_range', 'top_range'
    Параметры:
        df - DataFrame с колонкой 'zigzag_peaks'
        threshold - порог для определения соотношения сегментов
        buffer_percent - процент буфера (0.1 = 10%)
    
    Возвращает:
        DataFrame с добавленными колонками
    """
    # Создаем копию DataFrame
    result_df = df.copy()
    
    # Инициализируем колонки
    result_df = result_df.assign(
        pattern18=pd.NA, 
        prev_pattern18=pd.NA,
        bzp1=pd.NA, bzp2=pd.NA, bzp3=pd.NA, bzp4=pd.NA
    )
    
    # Выбираем только точки пиков зигзага
    peaks_mask = ~result_df['zigzag_peaks'].isna()
    peaks = result_df.loc[peaks_mask].copy()
    
    # Недостаточно точек для анализа паттерна
    if len(peaks) < 4:
        return result_df.assign(
            pattern18='none_pattern', 
            prev_pattern18='none_pattern',
            bzp1=pd.NA, bzp2=pd.NA, bzp3=pd.NA, bzp4=pd.NA
        )
    
    # Вычисляем 4 последовательные точки
    peaks = peaks.assign(
        zp1=peaks['zigzag_peaks'].shift(3),
        zp2=peaks['zigzag_peaks'].shift(2),
        zp3=peaks['zigzag_peaks'].shift(1),
        zp4=peaks['zigzag_peaks']
    )
    
    # Удаляем строки с недостаточными данными
    peaks = peaks.loc[~peaks['zp1'].isna()].copy()
    
    # Вычисляем разницы между точками
    peaks = peaks.assign(
        p1_2=peaks['zp1'] - peaks['zp2'],
        p2_3=peaks['zp2'] - peaks['zp3'],
        p3_4=peaks['zp3'] - peaks['zp4']
    )
    
    # Вычисляем буферизованные точки
    peaks = peaks.assign(
        # Внешний буфер для bzp1 (направление зависит от p2_3)
        bzp1=peaks['zp1'] - np.sign(peaks['p2_3']) * np.abs(peaks['p2_3']) * buffer_percent,
        
        # Внешний буфер для bzp2 (направление зависит от p2_3)
        bzp2=peaks['zp2'] + np.sign(peaks['p2_3']) * np.abs(peaks['p2_3']) * buffer_percent,
        
        # Внутренний буфер для bzp3 (направление зависит от p3_4)
        bzp3=peaks['zp3'] - np.sign(peaks['p3_4']) * np.abs(peaks['p3_4']) * buffer_percent,
        
        # Внутренний буфер для bzp4 (направление зависит от p3_4)
        bzp4=peaks['zp4'] + np.sign(peaks['p3_4']) * np.abs(peaks['p3_4']) * buffer_percent
    )
        # Добавляем целевые точки
    peaks = peaks.assign(
        target=peaks['zp4'] - peaks['p2_3'],  # zp4 + (zp3 - zp4) = zp3
        btarget=peaks['zp4'] - peaks['p2_3'] * (1 - buffer_percent/2),
        mzp = (peaks['zp3'] + peaks['zp4']) / 2
    )
    # Остальной код без изменений
    with np.errstate(divide='ignore', invalid='ignore'):
        r12_23 = np.abs(peaks['p1_2'] / peaks['p2_3'])
        r23_34 = np.abs(peaks['p2_3'] / peaks['p3_4'])
    
    big = 1 + threshold
    small = 1 - threshold
    p1_2_pos = peaks['p1_2'] > 0
    
    conditions = [
        (r12_23 > big) & (r23_34 > big) & p1_2_pos,
        (r12_23 > big) & (r23_34 > big) & ~p1_2_pos,
        (r12_23 > big) & (r23_34 < small) & p1_2_pos,
        (r12_23 > big) & (r23_34 < small) & ~p1_2_pos,
        (r12_23 > big) & (r23_34 >= small) & (r23_34 <= big) & p1_2_pos,
        (r12_23 > big) & (r23_34 >= small) & (r23_34 <= big) & ~p1_2_pos,
        (r12_23 < small) & (r23_34 > big) & p1_2_pos,
        (r12_23 < small) & (r23_34 > big) & ~p1_2_pos,
        (r12_23 < small) & (r23_34 < small) & p1_2_pos,
        (r12_23 < small) & (r23_34 < small) & ~p1_2_pos,
        (r12_23 < small) & (r23_34 >= small) & (r23_34 <= big) & p1_2_pos,
        (r12_23 < small) & (r23_34 >= small) & (r23_34 <= big) & ~p1_2_pos,
        (~(r12_23 < small) & ~(r12_23 > big)) & (r23_34 > big) & p1_2_pos,
        (~(r12_23 < small) & ~(r12_23 > big)) & (r23_34 > big) & ~p1_2_pos,
        (~(r12_23 < small) & ~(r12_23 > big)) & (r23_34 < small) & p1_2_pos,
        (~(r12_23 < small) & ~(r12_23 > big)) & (r23_34 < small) & ~p1_2_pos,
        (~(r12_23 < small) & ~(r12_23 > big)) & ~(r23_34 < small) & ~(r23_34 > big) & p1_2_pos,
        (~(r12_23 < small) & ~(r12_23 > big)) & ~(r23_34 < small) & ~(r23_34 > big) & ~p1_2_pos
    ]
    
    choices = [
        'weak_short', 'weak_long',
        'bui', 'joc',
        'double_bottom', 'double_top',
        'btc', 'bti',
        'sow', 'sos',
        'upthrust', 'spring',
        'narrowing_up', 'narrowing_down',
        'bui', 'joc',
        'bottom_range', 'top_range'
    ]
    
    peaks_pattern = pd.Series(
        data=np.select(conditions, choices, default='none_pattern'),
        index=peaks.index,
        dtype='object'
    )
    
    prev_peaks_pattern = peaks_pattern.shift(1)
    prev_peaks_pattern.fillna('none_pattern', inplace=True)
    
    result_df['pattern18'] = peaks_pattern.reindex(result_df.index).ffill()
    result_df['prev_pattern18'] = prev_peaks_pattern.reindex(result_df.index).ffill()
    
    result_df['pattern18'] = result_df['pattern18'].replace(pd.NA, 'none_pattern')
    result_df['prev_pattern18'] = result_df['prev_pattern18'].replace(pd.NA, 'none_pattern')
    
    # Обновляем основной DataFrame всеми колонками
    # Разделяем колонки по типам
    num_cols = ['zp1', 'zp2', 'zp3', 'zp4', 
               'bzp1', 'bzp2', 'bzp3', 'bzp4',
               'target', 'btarget', 'mzp']
    
    # Создаем временный DataFrame с числовыми данными
    num_data = peaks[num_cols].reindex(result_df.index).ffill()
    for col in num_cols:
        # Явное преобразование к float64 через numpy
        result_df[col] = num_data[col].values.astype('float64')
       
    return result_df

def add_pattern18_dzz_shifted(df: pd.DataFrame, threshold: float = 0.2, buffer_percent: float = 0.1) -> pd.DataFrame:
    """
    Версия индикатора, где все значения смещены на 1 пик назад
    """
    # Создаем копию DataFrame
    result_df = df.copy()
    
    # Инициализируем колонки
    result_df = result_df.assign(
        pattern18='none_pattern', 
        prev_pattern18='none_pattern',
        zp1=pd.NA, zp2=pd.NA, zp3=pd.NA, zp4=pd.NA,
        bzp1=pd.NA, bzp2=pd.NA, bzp3=pd.NA, bzp4=pd.NA,
        target=pd.NA, btarget=pd.NA, mzp=pd.NA
    )
    
    # Выбираем только точки пиков зигзага
    peaks_mask = ~result_df['zigzag_peaks'].isna()
    peaks = result_df.loc[peaks_mask].copy()
    
    # Недостаточно точек для анализа паттерна
    if len(peaks) < 4:
        return result_df
    
    # Вычисляем 4 последовательные точки (оригинальный расчет)
    peaks = peaks.assign(
        zp1=peaks['zigzag_peaks'].shift(3),
        zp2=peaks['zigzag_peaks'].shift(2),
        zp3=peaks['zigzag_peaks'].shift(1),
        zp4=peaks['zigzag_peaks']
    )
    
    # Удаляем строки с недостаточными данными
    peaks = peaks.loc[~peaks['zp1'].isna()].copy()
    
    # Вычисляем разницы между точками
    peaks = peaks.assign(
        p1_2=peaks['zp1'] - peaks['zp2'],
        p2_3=peaks['zp2'] - peaks['zp3'],
        p3_4=peaks['zp3'] - peaks['zp4']
    )
    
    # Вычисляем буферизованные точки
    peaks = peaks.assign(
        bzp1=peaks['zp1'] - np.sign(peaks['p2_3']) * np.abs(peaks['p2_3']) * buffer_percent,
        bzp2=peaks['zp2'] + np.sign(peaks['p2_3']) * np.abs(peaks['p2_3']) * buffer_percent,
        bzp3=peaks['zp3'] - np.sign(peaks['p3_4']) * np.abs(peaks['p3_4']) * buffer_percent,
        bzp4=peaks['zp4'] + np.sign(peaks['p3_4']) * np.abs(peaks['p3_4']) * buffer_percent,
        target=peaks['zp4'] - peaks['p2_3'],
        btarget=peaks['zp4'] - peaks['p2_3'] * (1 - buffer_percent/2),
        mzp=(peaks['zp3'] + peaks['zp4']) / 2
    )
    
    # Определяем паттерны
    with np.errstate(divide='ignore', invalid='ignore'):
        r12_23 = np.abs(peaks['p1_2'] / peaks['p2_3'])
        r23_34 = np.abs(peaks['p2_3'] / peaks['p3_4'])
    
    big = 1 + threshold
    small = 1 - threshold
    p1_2_pos = peaks['p1_2'] > 0
    
    conditions = [
        (r12_23 > big) & (r23_34 > big) & p1_2_pos,
        (r12_23 > big) & (r23_34 > big) & ~p1_2_pos,
        (r12_23 > big) & (r23_34 < small) & p1_2_pos,
        (r12_23 > big) & (r23_34 < small) & ~p1_2_pos,
        (r12_23 > big) & (r23_34 >= small) & (r23_34 <= big) & p1_2_pos,
        (r12_23 > big) & (r23_34 >= small) & (r23_34 <= big) & ~p1_2_pos,
        (r12_23 < small) & (r23_34 > big) & p1_2_pos,
        (r12_23 < small) & (r23_34 > big) & ~p1_2_pos,
        (r12_23 < small) & (r23_34 < small) & p1_2_pos,
        (r12_23 < small) & (r23_34 < small) & ~p1_2_pos,
        (r12_23 < small) & (r23_34 >= small) & (r23_34 <= big) & p1_2_pos,
        (r12_23 < small) & (r23_34 >= small) & (r23_34 <= big) & ~p1_2_pos,
        (~(r12_23 < small) & ~(r12_23 > big)) & (r23_34 > big) & p1_2_pos,
        (~(r12_23 < small) & ~(r12_23 > big)) & (r23_34 > big) & ~p1_2_pos,
        (~(r12_23 < small) & ~(r12_23 > big)) & (r23_34 < small) & p1_2_pos,
        (~(r12_23 < small) & ~(r12_23 > big)) & (r23_34 < small) & ~p1_2_pos,
        (~(r12_23 < small) & ~(r12_23 > big)) & ~(r23_34 < small) & ~(r23_34 > big) & p1_2_pos,
        (~(r12_23 < small) & ~(r12_23 > big)) & ~(r23_34 < small) & ~(r23_34 > big) & ~p1_2_pos
    ]
    
    choices = [
        'weak_short', 'weak_long',
        'bui', 'joc',
        'double_bottom', 'double_top',
        'btc', 'bti',
        'sow', 'sos',
        'upthrust', 'spring',
        'narrowing_up', 'narrowing_down',
        'bui', 'joc',
        'bottom_range', 'top_range'
    ]
    
    peaks['pattern18'] = np.select(conditions, choices, default='none_pattern')
    peaks['prev_pattern18'] = peaks['pattern18'].shift(1).fillna('none_pattern')
    
    # Ключевое изменение: смещаем все вычисленные значения на 1 пик назад
    shifted_peaks = peaks.copy()
    shifted_cols = ['pattern18', 'prev_pattern18',
                   'zp1', 'zp2', 'zp3', 'zp4',
                   'bzp1', 'bzp2', 'bzp3', 'bzp4',
                   'target', 'btarget', 'mzp']
    
    for col in shifted_cols:
        shifted_peaks[col] = shifted_peaks[col].shift(1)
    
    # Переносим смещенные значения в основной DataFrame
    for col in shifted_cols:
        # Для числовых колонок используем прямое присвоение
        if col in ['zp1', 'zp2', 'zp3', 'zp4', 'bzp1', 'bzp2', 'bzp3', 'bzp4', 'target', 'btarget', 'mzp']:
            result_df[col] = shifted_peaks[col].reindex(result_df.index).ffill()
        # Для паттернов делаем ffill и заполнение
        else:
            result_df[col] = shifted_peaks[col].reindex(result_df.index).ffill().fillna('none_pattern')
    
    return result_df

def add_pattern18_dzz_czd(df: pd.DataFrame, threshold: float = 0.2, buffer_percent: float = 0.1) -> pd.DataFrame:
    """
    Модифицированная версия индикатора паттернов зигзага.
    Паттерны фиксируются только в момент смены направления зигзага.
    """
    result_df = df.copy()
    
    # Инициализация колонок с правильными типами данных
    # Строковые колонки инициализируем строкой, числовые - np.nan
    result_df = result_df.assign(
        pattern18=pd.NA,  # строка
        prev_pattern18=pd.NA,  # строка
        bzp1=np.nan, bzp2=np.nan, bzp3=np.nan, bzp4=np.nan,
        zp1=np.nan, zp2=np.nan, zp3=np.nan, zp4=np.nan,
        target=np.nan, btarget=np.nan, mzp=np.nan
    )
    
    # Проверка наличия необходимых колонок
    if 'zigzag_direction' not in df.columns:
        raise ValueError("DataFrame must contain 'zigzag_direction' column")
    
    # Находим моменты смены направления зигзага
    direction_changes = result_df['zigzag_direction'].diff().ne(0)
    change_indices = direction_changes[direction_changes].index.tolist()
    
    # Если нет смен направления, возвращаем исходный df
    if len(change_indices) == 0:
        result_df['pattern18'] = result_df['pattern18'].fillna('none_pattern')
        result_df['prev_pattern18'] = result_df['prev_pattern18'].fillna('none_pattern')
        return result_df
    
    # Собираем все пики зигзага
    peaks_mask = ~result_df['zigzag_peaks'].isna()
    peaks = result_df.loc[peaks_mask, 'zigzag_peaks']
    
    # Создаем список для хранения результатов
    results = []
    big = 1 + threshold
    small = 1 - threshold
    # Обрабатываем каждую смену направления
    for i, change_idx in enumerate(change_indices):
        # Получаем последние 4 пика до текущей смены направления
        prev_peaks = peaks[peaks.index <= change_idx].tail(4)
        
        # Если не набралось 4 пика, пропускаем
        if len(prev_peaks) < 4:
            continue
        
        # Извлекаем 4 последних пика
        zp1, zp2, zp3, zp4 = prev_peaks[-4:].values
        
        # Вычисляем разницы между точками
        p1_2 = zp1 - zp2
        p2_3 = zp2 - zp3
        p3_4 = zp3 - zp4
        
        # Вычисляем буферизованные точки
        bzp1 = zp1 - np.sign(p2_3) * abs(p2_3) * buffer_percent
        bzp2 = zp2 + np.sign(p2_3) * abs(p2_3) * buffer_percent
        bzp3 = zp3 - np.sign(p3_4) * abs(p3_4) * buffer_percent
        bzp4 = zp4 + np.sign(p3_4) * abs(p3_4) * buffer_percent
        
        # Вычисляем целевые точки
        target = zp4 - p2_3
        btarget = zp4 - p2_3 * (1 - buffer_percent/2)
        mzp = (zp3 + zp4) / 2
        
        # Вычисляем соотношения сегментов
        with np.errstate(divide='ignore', invalid='ignore'):
            r12_23 = abs(p1_2 / p2_3) if p2_3 != 0 else float('inf')
            r23_34 = abs(p2_3 / p3_4) if p3_4 != 0 else float('inf')
        
        # Условия для классификации паттернов

        p1_2_pos = p1_2 > 0
        
        # Определяем паттерн через последовательную проверку условий
        pattern = 'none_pattern'
        
        if r12_23 > big and r23_34 > big:
            pattern = 'weak_short' if p1_2_pos else 'weak_long'
        elif r12_23 > big and r23_34 < small:
            pattern = 'bui' if p1_2_pos else 'joc'
        elif r12_23 > big and small <= r23_34 <= big:
            pattern = 'double_bottom' if p1_2_pos else 'double_top'
        elif r12_23 < small and r23_34 > big:
            pattern = 'btc' if p1_2_pos else 'bti'
        elif r12_23 < small and r23_34 < small:
            pattern = 'sow' if p1_2_pos else 'sos'
        elif r12_23 < small and small <= r23_34 <= big:
            pattern = 'upthrust' if p1_2_pos else 'spring'
        elif (small <= r12_23 <= big) and r23_34 > big:
            pattern = 'narrowing_up' if p1_2_pos else 'narrowing_down'
        elif (small <= r12_23 <= big) and r23_34 < small:
            pattern = 'bui' if p1_2_pos else 'joc'
        elif (small <= r12_23 <= big) and (small <= r23_34 <= big):
            pattern = 'bottom_range' if p1_2_pos else 'top_range'
        # Предыдущий паттерн
        prev_pattern = 'none_pattern'
        if results:
            prev_pattern = results[-1]['pattern18']
        
        # Сохраняем результаты
        results.append({
            'index': change_idx,
            'pattern18': pattern,
            'prev_pattern18': prev_pattern,
            'zp1': zp1, 'zp2': zp2, 'zp3': zp3, 'zp4': zp4,
            'bzp1': bzp1, 'bzp2': bzp2, 'bzp3': bzp3, 'bzp4': bzp4,
            'target': target, 'btarget': btarget, 'mzp': mzp
        })
    
    # Если нет результатов, возвращаем исходный df
    if not results:
        result_df['pattern18'] = result_df['pattern18'].fillna('none_pattern')
        result_df['prev_pattern18'] = result_df['prev_pattern18'].fillna('none_pattern')
        return result_df
    
    # Создаем DataFrame из результатов
    confirmed_data = pd.DataFrame(results).set_index('index')
    
    # Заполняем результаты в основной DataFrame
    # Для каждой колонки из confirmed_data
    for col in confirmed_data.columns:
        # Обновляем значения только в точках смены направления
        result_df.loc[confirmed_data.index, col] = confirmed_data[col]
    
    # Форвардное заполнение для всех колонок
    # Числовые колонки
    num_cols = ['zp1', 'zp2', 'zp3', 'zp4', 'bzp1', 'bzp2', 'bzp3', 'bzp4', 'target', 'btarget', 'mzp']
    for col in num_cols:
        result_df[col] = result_df[col].ffill().astype(float)
    
    # Строковые колонки
    str_cols = ['pattern18', 'prev_pattern18']
    for col in str_cols:
        result_df[col] = result_df[col].ffill().fillna('none_pattern')
    
    return result_df

def add_stop_loss_p18czd(df,divider=2):
    """add 'lsl','ssl'"""
    df = df.copy()
    df['cur_range'] = (df['zp3'] - df['zp4']).abs()

    # Вычисляем min и max между zp3 и zp4 для каждой строки
    df['min_zp'] = df[['zp3', 'zp4']].min(axis=1)
    df['max_zp'] = df[['zp3', 'zp4']].max(axis=1)

    # Вычисляем lsl и ssl
    df['lsl'] = df['min_zp'] - df['cur_range'] / divider
    df['ssl'] = df['max_zp'] + df['cur_range'] / divider

    # Удаляем временные колонки (опционально)
    df = df.drop(columns=['min_zp', 'max_zp'])
    return df

def add_buffer_dzz(df:pd.DataFrame,period=20):
    """add 'hbzz','lbzz'"""
    df['hdz'] = (df['high'] - df['zigzag']).rolling(period).std()
    df['ldz'] = (df['zigzag'] - df['low']).rolling(period).std()
    df['hbzz'] =  df['zigzag'] + df['hdz']
    df['lbzz'] =  df['zigzag'] - df['ldz']
    return df

def add_stable_ma_direction(df:pd.DataFrame,period=10,kind:str='sma'):
    """add 'dir_ma'"""
    df['diff_ma'] = np.sign(df[kind].diff())
    df['dir_ma'] = df['diff_ma'].rolling(period).mean()
    return df

def add_quantile_params(df:pd.DataFrame,period:int=10,kind:str='rsi',quantile:float=0.1):
    """add 'top_q','bottom_q'"""
    roll = df[kind].rolling(period)
    df['top_q'] = roll.quantile(1-quantile)
    df['bottom_q'] = roll.quantile(quantile)
    return df

def add_mean_dzz_peaks(df: pd.DataFrame, period=2, buffer=0.1):
    """add 'top_mean','bottom_mean','delta_mean'"""
    df = df.copy()
    peaks = df[~pd.isna(df['zigzag_peaks'])].copy()  # Добавляем .copy() здесь
    
    # Создаем копии для top и bottom peaks
    top_peaks = peaks[peaks['zigzag_direction'] == 1].copy()
    bottom_peaks = peaks[peaks['zigzag_direction'] == -1].copy()
    
    # Используем .loc для присвоения значений
    top_peaks.loc[:, 'top_mean'] = top_peaks['high'].rolling(period).mean()
    bottom_peaks.loc[:, 'bottom_mean'] = bottom_peaks['low'].rolling(period).mean()
    
    # Объединяем результаты обратно
    df = df.join(top_peaks[['top_mean']], how='left')
    df = df.join(bottom_peaks[['bottom_mean']], how='left')
    
    df['top_mean'] = df['top_mean'].ffill()
    df['bottom_mean'] = df['bottom_mean'].ffill()
    df['delta_mean'] = df['top_mean'] - df['bottom_mean']
    df['buffer_mean'] = df['delta_mean']  * buffer
    df['top_mean'] = df['top_mean'] - df['buffer_mean']
    df['bottom_mean'] = df['bottom_mean'] + df['buffer_mean']
    
    return df

def add_plusdelta_dzz_peaks(df: pd.DataFrame, period=2, buffer=0.1):
    """add 'top_pd','bottom_pd','delta_pd'"""
    df = df.copy()
    peaks = df[~pd.isna(df['zigzag_peaks'])].copy()  # Добавляем .copy() здесь
    
    # Создаем копии для top и bottom peaks
    top_peaks = peaks[peaks['zigzag_direction'] == 1].copy()
    bottom_peaks = peaks[peaks['zigzag_direction'] == -1].copy()
    
    # Используем .loc для присвоения значений
    top_peaks.loc[:, 'delta'] = top_peaks['high'].diff()
    bottom_peaks.loc[:, 'delta'] = bottom_peaks['low'].diff()
    top_peaks.loc[:, 'delta_mean'] = top_peaks['delta'].rolling(period).mean()
    bottom_peaks.loc[:, 'delta_mean'] = bottom_peaks['delta'].rolling(period).mean()
    top_peaks.loc[:, 'top_pd'] = top_peaks['high'] + top_peaks['delta_mean']
    bottom_peaks.loc[:, 'bottom_pd'] = bottom_peaks['low'] + bottom_peaks['delta_mean']
    # Объединяем результаты обратно
    df = df.join(top_peaks[['top_pd']], how='left')
    df = df.join(bottom_peaks[['bottom_pd']], how='left')
    
    df['top_pd'] = df['top_pd'].ffill()
    df['bottom_pd'] = df['bottom_pd'].ffill()
    df['delta_pd'] = df['top_pd'] - df['bottom_pd']
    df['buffer_mean'] = df['delta_pd']  * buffer
    df['top_pd'] = df['top_pd'] - df['buffer_mean']
    df['bottom_pd'] = df['bottom_pd'] + df['buffer_mean']
    return df

def add_exp_plusdelta_dzz_peaks(df: pd.DataFrame, period=2, buffer=0.1):
    """add 'top_pd','bottom_pd','delta_pd'"""
    df = df.copy()
    peaks = df[~pd.isna(df['zigzag_peaks'])].copy()  # Добавляем .copy() здесь
    
    # Создаем копии для top и bottom peaks
    top_peaks = peaks[peaks['zigzag_direction'] == 1].copy()
    bottom_peaks = peaks[peaks['zigzag_direction'] == -1].copy()
    
    # Используем .loc для присвоения значений
    top_peaks.loc[:, 'delta'] = top_peaks['high'].diff()
    bottom_peaks.loc[:, 'delta'] = bottom_peaks['low'].diff()
    top_peaks.loc[:, 'delta_mean'] = top_peaks['delta'].ewm(period).mean()
    bottom_peaks.loc[:, 'delta_mean'] = bottom_peaks['delta'].ewm(period).mean()
    top_peaks.loc[:, 'top_pd'] = top_peaks['high'] + top_peaks['delta_mean']
    bottom_peaks.loc[:, 'bottom_pd'] = bottom_peaks['low'] + bottom_peaks['delta_mean']
    # Объединяем результаты обратно
    df = df.join(top_peaks[['top_pd']], how='left')
    df = df.join(bottom_peaks[['bottom_pd']], how='left')
    
    df['top_pd'] = df['top_pd'].ffill()
    df['bottom_pd'] = df['bottom_pd'].ffill()
    df['delta_pd'] = df['top_pd'] - df['bottom_pd']
    df['buffer_mean'] = df['delta_pd']  * buffer
    df['top_pd'] = df['top_pd'] - df['buffer_mean']
    df['bottom_pd'] = df['bottom_pd'] + df['buffer_mean']
    return df