def check_strategy(df,strategy):
    """
    trades,longs,shorts,closes,equity
    """
    trades = {
        'pos':0,
        'open_price':0,
        'total':0,
        'count':0
    }
    longs = []
    shorts = []
    closes = []
    equity = []
    df.apply(lambda row: strategy(row,trades,shorts,longs,closes,equity),axis=1)
    return trades,longs,shorts,closes,equity