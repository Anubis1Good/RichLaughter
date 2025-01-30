import requests
from pprint import pprint
from datetime import datetime

url_req = "https://api.bitget.com/api/v2/mix/market/history-candles?symbol=BTCUSDT&granularity=1m&limit=200&productType=usdt-futures"
# url_req = "https://api.bitget.com/api/v2/mix/market/candles?symbol=BTCUSDT&granularity=1m&limit=100&productType=usdt-futures"

res = requests.get(url_req).json()
pprint(res)
print(res['data'][-1][0][:-3])
print(datetime.fromtimestamp(float(res['data'][-1][0][:-3])))
# print(res['data'])