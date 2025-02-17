import os
from Optimiztion.Optimizator1 import Optimizator1
from strategies.work_strategies.PTA import PTA2_BDDC
from strategies.test_strategies.PTA import get_action_PTA2_BDDC

# raw_file = 'DataForTests\DataFromBitget\DOGEUSDT_1m_1739819667.csv'
test_folder = 'DataForTests\DataFromBitget'
list_dir = os.listdir(test_folder)
params = [
    range(5,201,5)
]
optim = Optimizator1(PTA2_BDDC,get_action_PTA2_BDDC,params)
for rw in list_dir:
    raw_file = os.path.join(test_folder,rw)
    print(rw)
    try:
        optim.run(raw_file)
    except:
        print(rw,'not stocks')