import os
import traceback
from Optimiztion.Optimizator1 import Optimizator1

def optimization(ws,ts,params,test_folder,min_fee: float = 0.0004,
    max_fee: float = 0.0012):
    list_dir = os.listdir(test_folder)
    optim = Optimizator1(ws,ts,params,min_fee=min_fee,max_fee=max_fee)
    for rw in list_dir:
        raw_file = os.path.join(test_folder,rw)
        print(rw)
        try:
            optim.run(raw_file)
        except Exception as err:
            traceback.print_exc()
            print(rw,'not stocks')

if __name__ == '__main__':
    from strategies.work_strategies.PTA import PTA2_DDCde as ws
    from strategies.test_strategies.universal import universal_test_strategy as ts
    # from strategies.work_strategies.OGTA import OGTA1_Rails as ws
    # from strategies.work_strategies.STA_ca import STA1e as ws
    test_folder = 'DataForTests\DataFromBitget'
    # test_folder = 'DataForTests\DataFromMOEX'
    params = [
        range(5,41,5)
    ]
    min_fee = 0.0004
    max_fee = 0.0012
    # min_fee = 0.0002
    # max_fee = 0.0009
    # params = [
    #     range(5,21,5),
    #     (0.5,1,1.5,2,2.5,3)
    # ]
    # params = [
    #     range(5,61,5),
    #     range(2,4),
    #     range(1,22,5)
    # ]
    optimization(ws,ts,params,test_folder,min_fee,max_fee)