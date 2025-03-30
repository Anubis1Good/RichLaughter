import os
import traceback
from Optimiztion.Optimizator1 import Optimizator1,Optimizator2

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

def optimization_multi(ws,ts,params,test_folder,min_fee: float = 0.0004,
    max_fee: float = 0.0012):
    list_dir = os.listdir(test_folder)
    optim = Optimizator2(ws,ts,params,min_fee=min_fee,max_fee=max_fee)
    for rw in list_dir:
        raw_file = os.path.join(test_folder,rw)
        print(rw)
        try:
            optim.run(raw_file)
        except Exception as err:
            traceback.print_exc()
            print(rw,'not stocks')

if __name__ == '__main__':
    # from strategies.work_strategies.PTA import PTA2_ALKASH as ws
    from strategies.test_strategies.universal import universal_test_strategy as ts
    # from strategies.work_strategies.PTAX import PTA14_RWDDCr as ws
    # from strategies.work_strategies.LTA2 import LTA2_OVERLORD as ws
    from strategies.work_strategies.PTAX import PTA15_WIDOWMAKER as ws
    # from strategies.work_strategies.STA_ca import STA1e as ws
    # from strategies.work_strategies.STA_ml2 import STAML2_LEGACY as ws
    test_folder = 'DataForTests\DataFromBitget'
    test_folder = 'DataForTests\DataFromMOEX'
    params = [
        range(5,106,5),
        (10,20,30,40)
    ]
    # params = [
    #     [5]+list(range(10,51,10)),
    #     range(20,61,10),
    #     [5]+list(range(10,101,10)),
    #     range(1,4),
    #     [5]+list(range(10,51,10)),
    # ]
    # params = [
    #     range(5,106,5),
    #     (0,0.1,0.2,0.3,0.5),
    #     (5,),
    #     (0.5,1,1.5,2)
    # ]
    min_fee = 0.0004
    max_fee = 0.0012
    min_fee = 0.0002
    max_fee = 0.0009
    # params = [
    #      [2,3,4,6]+list(range(5,21,5)),
    #     (0.5,1,1.5)
    # ]
    # params = [
    #     (range(5,11,5)),
    #     (0.5,1,1.5,2),
    #     list(range(5,21,5)),
    #     (0.5,)
    # ]
    # params = [
    #     range(5,61,5),
    #     range(2,4),
    #     range(1,22,5)
    # ]
    optimization_multi(ws,ts,params,test_folder,min_fee,max_fee)
    # optimization(ws,ts,params,test_folder,min_fee,max_fee)