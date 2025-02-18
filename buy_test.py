from Traders.BitgetTrader import BitgetTrader
from pprint import pprint
trader = BitgetTrader()

# trader.open_long("DOGEUSDT",50,10)
trader.close_long("DOGEUSDT",3)
# trader.close_short("DOGEUSDT",3)
# pprint(trader.check_position("DOGEUSDT"))
# trader.clear_order("DOGEUSDT")
# print(trader.fetch_firts_orders("DOGEUSDT",10))