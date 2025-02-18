import os
from Optimiztion.Optimizator1 import Optimizator1
# from strategies.work_strategies.PTA import PTA2_BDDC as ws
# from strategies.test_strategies.PTA import get_action_PTA2_BDDC as ts
from strategies.work_strategies.STA_ca import STA1e as ws
from strategies.test_strategies.STA_ca import get_action_STA1e as ts 

# raw_file = 'DataForTests\DataFromBitget\DOGEUSDT_1m_1739819667.csv'
test_folder = 'DataForTests\DataFromBitget'
list_dir = os.listdir(test_folder)
# params = [
#     range(5,201,5)
# ]
params = [
    range(5,201,5),
    range(1,4),
    range(1,21)
]
optim = Optimizator1(ws,ts,params)
for rw in list_dir:
    raw_file = os.path.join(test_folder,rw)
    print(rw)
    try:
        optim.run(raw_file)
    except:
        print(rw,'not stocks')