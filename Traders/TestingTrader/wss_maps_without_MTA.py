from Traders.TestingTrader.wss_groups import wssBitgetFut1,wssBitgetFut5,wssBitgetFut15,wssBitgetFut30,wssBitgetFut60,wssMoexFut1,wssMoexFut5,wssMoexStocks1,wssMoexStocks5

bitgetFutMap = {
    '1m':wssBitgetFut1,
    '5m':wssBitgetFut5,
    '15m':wssBitgetFut15,
    '30m':wssBitgetFut30,
    '1H':wssBitgetFut60,
}

moexFutMap = {
    1:wssMoexFut1,
    5:wssMoexFut5,
}
moexStockMap = {
    1:wssMoexStocks1,
    5:wssMoexStocks5,
}

testTestMap = {
    1:wssBitgetFut60,
    5:wssBitgetFut60,
}