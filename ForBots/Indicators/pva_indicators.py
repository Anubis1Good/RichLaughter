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