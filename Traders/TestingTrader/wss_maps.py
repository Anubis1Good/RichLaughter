from Traders.TestingTrader.wss_maps_without_MTA import bitgetFutMap,moexFutMap,moexStockMap
from strategies.work_strategies.MTA import MTA_LORD,MTA_LORD2,MTA_SKYNET

wssMoexSkynet1 = (
    (MTA_SKYNET,(100,'u1_1_test_MOEX_FUT')),
    (MTA_SKYNET,(100,'u4_1_test_MOEX_FUT')),
)

wssMoexSkynet5 = (
    (MTA_SKYNET,(100,'u1_5_test_MOEX_FUT')),
    (MTA_SKYNET,(100,'u4_5_test_MOEX_FUT')),
)

skynetTestMap = {
    1:wssMoexSkynet1,
    5:wssMoexSkynet5
}

def add_skynet(suffix,tradeMap,hourss):
    for g in tradeMap:
        tradeMap[g] = list(tradeMap[g])
        for h in hourss:
            filename = f"{h}_{g}_{suffix}"
            tradeMap[g].append((MTA_SKYNET,(100,filename)))
        filename = f"FC_{g}_{suffix}"
        tradeMap[g].append((MTA_SKYNET,(100,filename)))
        tradeMap[g] = tuple(tradeMap[g])
    return tradeMap

bitgetFutMap = add_skynet('test_Bitget_FUT',bitgetFutMap,(1,4,8))
moexFutMap = add_skynet('test_MOEX_FUT',moexFutMap,(1,4,8))
moexStockMap = add_skynet('test_MOEX_STOCK',moexStockMap,(1,4,8))