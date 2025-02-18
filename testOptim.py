import os
import traceback
from Optimiztion.Optimizator1 import Optimizator1
from strategies.work_strategies.PTA import PTA2_UDC as ws
from strategies.test_strategies.universal import universal_test_strategy as ts
# from strategies.work_strategies.STA_ca import STA1e as ws
# from strategies.test_strategies.STA_ca import get_action_STA1e as ts 

# raw_file = 'DataForTests\DataFromBitget\DOGEUSDT_1m_1739819667.csv'
test_folder = 'DataForTests\DataFromBitget'
list_dir = os.listdir(test_folder)
# params = [
#     range(5,121,5)
# ]
params = [
    range(5,41,5),
    range(5,31,2)
]
# params = [
#     range(5,61,5),
#     range(2,4),
#     range(1,22,5)
# ]
optim = Optimizator1(ws,ts,params)
for rw in list_dir:
    raw_file = os.path.join(test_folder,rw)
    print(rw)
    try:
        optim.run(raw_file)
    except Exception as err:
        traceback.print_exc()
        print(rw,'not stocks')