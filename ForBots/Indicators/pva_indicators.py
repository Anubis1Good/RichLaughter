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