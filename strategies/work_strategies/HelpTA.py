from strategies.work_strategies.BaseTA import BaseTABitget

class CloseTA(BaseTABitget):
    def __init__(self, symbol="BTCUSDT", granularity="1m", productType="usdt-futures", n_parts=1, period=15):
        super().__init__(symbol, granularity, productType, n_parts, period)
    def preprocessing(self, df):
        return df
    def __call__(self, row, *args, **kwds):
        return 'close_all_pw'