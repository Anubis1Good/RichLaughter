import requests

def get_history_candles(symbol="BTCUSDT",granularity="1m",productType="usdt-futures",limit="200",startTime="0",endTime="0"):
    """K-line particle size
    - 1m(1 minute)
    - 3m(3 minutes)
    - 5m(5 minutes)
    - 15m(15 minutes)
    - 30m(30 minutes)
    - 1H( 1 hour)
    - 4H(4 hours)
    - 6H(6 hours)
    - 12H(12 hours)
    - 1D(1 day)
    - 3D ( 3 days)
    - 1W (1 week)
    - 1M (monthly line)
    - 6Hutc (UTC 6 hour line)
    - 12Hutc (UTC 12 hour line)
    - 1Dutc (UTC 1-day line)
    - 3Dutc (UTC 3-day line)
    - 1Wutc (UTC weekly line)
    - 1Mutc (UTC monthly line)
    """
    url_req = f"https://api.bitget.com/api/v2/mix/market/history-candles?symbol={symbol}&granularity={granularity}&limit={limit}&productType={productType}"
    if startTime != "0":
        url_req += "&startTime="+str(startTime)
    if endTime != "0":
        url_req += "&endTime="+str(endTime)
    res = requests.get(url_req).json()
    return res['data']

def get_candles(symbol="BTCUSDT",granularity="1m",productType="usdt-futures",limit="200"):
    """K-line particle size
    - 1m(1 minute)
    - 3m(3 minutes)
    - 5m(5 minutes)
    - 15m(15 minutes)
    - 30m(30 minutes)
    - 1H( 1 hour)
    - 4H(4 hours)
    - 6H(6 hours)
    - 12H(12 hours)
    - 1D(1 day)
    - 3D ( 3 days)
    - 1W (1 week)
    - 1M (monthly line)
    - 6Hutc (UTC 6 hour line)
    - 12Hutc (UTC 12 hour line)
    - 1Dutc (UTC 1-day line)
    - 3Dutc (UTC 3-day line)
    - 1Wutc (UTC weekly line)
    - 1Mutc (UTC monthly line)
    """
    url_req = f"https://api.bitget.com/api/v2/mix/market/candles?symbol={symbol}&granularity={granularity}&limit={limit}&productType={productType}"
    res = requests.get(url_req).json()
    return res['data']

def get_ticks(symbol="BTCUSDT",productType="usdt-futures",limit="1000",startTime="0",endTime="0"):
    url_req = f"https://api.bitget.com/api/v2/mix/market/fills-history?symbol={symbol}&productType={productType}&limit={limit}"
    if startTime != "0":
        url_req += "&startTime="+str(startTime)
    if endTime != "0":
        url_req += "&endTime="+str(endTime)
    res = requests.get(url_req).json()
    return res['data']