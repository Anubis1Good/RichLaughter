from Traders.QuikTrader.QuikFuncs import *

# print(get_active_order('MMM5'))
# print(get_pos_futures('MMM5'))
while True:
    df = get_bars('MMM5')
    print(df.iloc[-1]['ms'])