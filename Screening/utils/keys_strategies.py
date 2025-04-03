from Traders.TestingTrader.wss_maps_without_MTA import bitgetFutMap,moexFutMap,moexStockMap

def get_dict_strategies(botMap):
    keys_strategies = {}

    for g in botMap:
        for ws in botMap[g]:
            name_key = str(ws[0]).split('.')[-1].replace("'>","")
            name_list = [g,name_key,*ws[1]]
            name_list = list(map(str,name_list))
            name_key = '_'.join(name_list)
            keys_strategies[name_key] = ws 
    return keys_strategies

bitgetFutDC = get_dict_strategies(bitgetFutMap)
moexFutDC = get_dict_strategies(moexFutMap)
moexStockDC = get_dict_strategies(moexStockMap)

allDC = {
    'Bitget_FUT':bitgetFutDC,
    'MOEX_FUT':moexFutDC,
    'MOEX_STOCK':moexStockDC
}