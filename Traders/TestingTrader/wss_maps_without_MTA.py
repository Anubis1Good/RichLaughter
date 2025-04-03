from Traders.TestingTrader.wss_groups import wssBitgetFut1,wssBitgetFut5,wssBitgetFut15,wssBitgetFut30,wssBitgetFut60,wssMoexFut,wssMoexStocks

bitgetFutMap = {
    '1m':wssBitgetFut1,
    '5m':wssBitgetFut5,
    '15m':wssBitgetFut15,
    '30m':wssBitgetFut30,
    '1H':wssBitgetFut60,
}

moexFutMap = {
    1:wssMoexFut,
    5:wssMoexFut,
}
moexStockMap = {
    1:wssMoexStocks,
    5:wssMoexStocks,
}

testTestMap = {
    1:wssBitgetFut60,
    5:wssBitgetFut60,
}