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