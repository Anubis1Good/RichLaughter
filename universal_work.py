from strategies.test_strategies.CheckWSTrader import CheckWSTrader
# from strategies.work_strategies.PTAXX import PTA26_ as WS
from strategies.work_strategies.NLSTA import NLSTA1_UNION as WS
from utils.work_with_dataframe.load_df import simple_load_df
# from Loader.BitgetLoader import bitget_loader


# raw_file = 'DataForTests\DataFromMoexFast\\5IMOEXF_1_1752761086.csv'
# raw_file = 'DataForTests\DataFromMoexForStepTests\IMOEXF_1_1756718219.csv'
# raw_file = 'DataForTests\DataMoexFutP\IMOEXF_1_1766374056.parquet'
raw_file = 'DataForTests\DataMoexFut5P\_5IMOEXF_1_1766374056.parquet'
# raw_file = 'DataForTests\DataMoexStock5P\_5MTLR_1_1766405408.parquet'
# raw_file = 'DataForTests\DataMoexFut5P\_5GZZ5_1_1766374097.parquet'

# df = bitget_loader(raw_file)
df = simple_load_df(raw_file)

symbol = "IMOEXF"
# symbol = "MTRL"
# symbol = "GZZ5"
granularity = "5m"
fee_base = 0.0002
stop_risk = None
# stop_risk = 350
window = 150
close_on_time = True
close_on_time = False
normalization=True
# normalization=False
vtb = True
# vtb = False
close_map = ((23,30),(23,30),(23,30),(23,30),(23,30),(17,50),(17,50),)
params = []
# params = (62,26,11,2.41,0,)

print(WS)
# ws = WS(symbol,granularity,'e',1,*params)
ws = WS(symbol,granularity,'e',1,policy_model='modelML\_nls_models\\total_1784p00_count_378.pth',cparams={
            'period': 50,
        })

cwt = CheckWSTrader(df,ws,fee_base,symbol,granularity,close_on_time,close_map,True,True,stop_risk)

use_fast = 1
use_window = 0
use_child = 0

new_tf = '5min'

if use_fast:
    cwt.check_strategy_fast()

if use_window:
    cwt.check_strategy_window(window=window,normalization=normalization)

if use_child:
    cwt.check_strategy_child(window=window,normalization=normalization)

convert_tf = new_tf if use_child else None

cwt.print_statistics(vtb=vtb)
print(cwt.get_statistics(vtb))
cwt.plot_chart_and_sequtity(convert_tf=convert_tf,vtb=vtb)
