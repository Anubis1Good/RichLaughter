import requests

def get_bybit_candles(symbol="BTCUSDT", interval="1", limit=200, category="linear"):
    """
    Получение свечей с Bybit
    
    Параметры:
    - symbol: торговый символ (например "BTCUSDT")
    - interval: таймфрейм (в минутах):
      - 1 (1 минута)
      - 3 (3 минуты)
      - 5 (5 минут)
      - 15 (15 минут)
      - 30 (30 минут)
      - 60 (1 час)
      - 120 (2 часа)
      - 240 (4 часа)
      - 360 (6 часов)
      - 720 (12 часов)
      - D (1 день)
      - W (1 неделя)
      - M (1 месяц)
    - limit: количество свечей (макс. 1000)
    - category: тип контракта:
      - spot (спот)
      - linear (USDT фьючерсы)
      - inverse (обратные фьючерсы)
      - option (опционы)
    
    Возвращает список свечей в формате:
    [timestamp, open, high, low, close, volume, turnover]
    """
    base_url = "https://api.bybit.com"
    endpoint = "/v5/market/kline"
    
    params = {
        "symbol": symbol,
        "interval": interval,
        "limit": limit,
        "category": category
    }
    
    try:
        response = requests.get(f"{base_url}{endpoint}", params=params)
        response.raise_for_status()
        data = response.json()
        
        if data["retCode"] != 0:
            raise Exception(f"Bybit API error: {data['retMsg']}")
        
        return data["result"]["list"]
    except Exception as e:
        print(f"Error fetching candles: {e}")
        return None

def get_bybit_history_candles(
    symbol="BTCUSDT",
    interval="1",
    category="linear",
    limit=200,
    startTime=0,
    endTime=0
):
    """
    Получение исторических свечей с Bybit (аналог Bitget API)
    
    Параметры:
    - symbol: торговая пара (BTCUSDT)
    - interval: таймфрейм:
      - 1,3,5,15,30,60,120,240,360,720 (минуты)
      - D, W, M (день, неделя, месяц)
    - category: spot/linear/inverse/option
    - limit: количество свечей (макс. 1000)
    - startTime/endTime: timestamp в миллисекундах (0 - не задано)
    
    Возвращает список свечей в формате:
    [timestamp, open, high, low, close, volume, turnover]
    """
    base_url = "https://api.bybit.com/v5/market/kline"
    
    params = {
        "symbol": symbol,
        "interval": interval,
        "category": category,
        "limit": limit
    }
    
    if startTime != 0:
        params["start"] = startTime
    if endTime != 0:
        params["end"] = endTime
    
    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()
        data = response.json()
        
        if data["retCode"] != 0:
            raise Exception(f"Bybit API error: {data['retMsg']}")
        
        return data["result"]["list"]
    except Exception as e:
        print(f"Error fetching candles: {e}")
        return None