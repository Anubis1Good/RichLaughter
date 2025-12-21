from Loader.BitgetLoader import bitget_loader
from strategies.test_strategies.CheckWSTrader import CheckWSTrader
from strategies.work_strategies.PSTA0 import PSTA6_ADVENTURE as WS


raw_file = 'DataForTests\DataFromMoexFast\\5IMOEXF_1_1752761086.csv'
raw_file = 'DataForTests\DataFromMoexForStepTests\IMOEXF_1_1756718219.csv'

df = bitget_loader(raw_file)

symbol = "IMOEXF"
granularity = "5m"
fee_base = 0.0002
stop_risk = None
stop_risk = 250
close_on_time = True
# close_on_time = False
close_map = ((23,30),(23,30),(23,30),(23,30),(23,30),(17,50),(17,50),)
params = []
params = (62,26,11,2.41,0,)

print(WS)
ws = WS(symbol,granularity,'e',1,*params)

cwt = CheckWSTrader(df,ws,fee_base,symbol,granularity,close_on_time,close_map,True,True,stop_risk)

# cwt.check_strategy_window(window=150,normalization=True)
cwt.check_strategy_child(window=150,normalization=True)

cwt.print_statistics(vtb=True)
# cwt.plot_chart_and_sequtity()
cwt.plot_chart_and_sequtity(convert_tf='5min')
