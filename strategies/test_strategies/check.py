import pandas as pd
def check_strategy(df,test_strategy,work_strategy):
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
    df.apply(lambda row: test_strategy(row,trades,shorts,longs,closes,equity,work_strategy),axis=1)
    return trades,longs,shorts,closes,equity


class TradeTracker:
    def __init__(self):
        self.pos = 0
        self.open_price = 0
        self.total = 0
        self.count = 0


def check_strategy_fast(df:pd.DataFrame, test_strategy, work_strategy):
    """
    Быстрая функция для проверки стратегии.
    """
    trades = {
        'pos':0,
        'open_price':0,
        'total':0,
        'count':0,
        'signal':None
    }
    # Векторизованная обработка данных
    df.apply(lambda row: test_strategy(row,trades,work_strategy),axis=1)
    row = df.iloc[-1]
    if trades['pos'] == 1:
        trades['pos'] = 0
        trades['total'] += row['close'] - trades['open_price']
        trades['count'] += 1  
    if trades['pos'] == -1:
        trades['pos'] = 0
        trades['total'] += trades['open_price'] - row['close']
        trades['count'] += 1 
    trades['open_price'] = df['middle'].median()
    return trades

