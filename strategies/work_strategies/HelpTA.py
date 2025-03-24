from strategies.work_strategies.BaseTA import BaseTABitget

# class LTA_BARASH(BaseTABitget):
#     def __init__(self, symbol="BTCUSDT", granularity="1m", productType="usdt-futures", n_parts=1, period=15,threshold=30):
#         super().__init__(symbol, granularity, productType, n_parts, period)
#         self.threshold = threshold
#     def preprocessing(self, df):
#         df = add_cci(df,self.period)
#         df = add_enter_price2close(df)  
#         df = add_slice_df(df, self.period) 
#         return df

#     def __call__(self, row, *args, **kwds):
#         if row['cci'] < -200+self.threshold:  
#             return 'long_pw'
#         if row['cci'] > 200-self.threshold:  
#             return 'short_pw'