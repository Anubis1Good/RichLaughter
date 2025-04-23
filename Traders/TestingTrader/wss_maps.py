import copy
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
    # tradeMap = copy.deepcopy(tradeMap)
    newMap = {}
    for g in tradeMap:
        newMap[g] = list()
        for h in hourss:
            filename = f"{h}_{g}_{suffix}"
            newMap[g].append((MTA_SKYNET,(100,filename)))
        filename = f"FC_{g}_{suffix}"
        newMap[g].append((MTA_SKYNET,(100,filename)))
        filename = f"FC5_{g}_{suffix}"
        newMap[g].append((MTA_SKYNET,(100,filename)))
        filename = f"FC5H_{g}_{suffix}"
        newMap[g].append((MTA_SKYNET,(100,filename)))
        filename = f"B24_{g}_{suffix}"
        newMap[g].append((MTA_SKYNET,(100,filename)))
        filename = f"B100_{g}_{suffix}"
        newMap[g].append((MTA_SKYNET,(100,filename)))
        filename = f"BTD_{g}_{suffix}"
        newMap[g].append((MTA_SKYNET,(100,filename)))
        filename = f"C100_{g}_{suffix}"
        newMap[g].append((MTA_SKYNET,(100,filename)))
        filename = f"C500_{g}_{suffix}"
        newMap[g].append((MTA_SKYNET,(100,filename)))
        newMap[g] = tuple(newMap[g])
    return newMap

bitgetMTAFutMap = add_skynet('test_Bitget_FUT',bitgetFutMap,(8,24))
moexMTAFutMap = add_skynet('test_MOEX_FUT',moexFutMap,(8,24))
moexMTAStockMap = add_skynet('test_MOEX_STOCK',moexStockMap,(8,24))