import os
import traceback
from time import time,sleep
from Screening.robots.Architect import Architect
from Screening.robots.AgentSmith import AgentSmith

print('Start Update Picks')

archs = (
    # Architect(
    #     'dbs/test_Bitget_FUT.db',
    #     ('1m','5m','15m','30m','1H'),
    #     (24,100)
    #     ),
    Architect(
        'dbs/test_MOEX_FUT.db',
        (1,5),
        (24,)),
    Architect(
        'dbs/test_MOEX_STOCK.db',
        (1,5),
        (24,)),
)

smith = AgentSmith('_')
first_start = True
start = time()
while True:
    # start=time()
    try:
        for arch in archs:
            arch.run()
    except Exception:
        traceback.print_exc()
        sleep(60)
    try:
        smith.upload_all()
        if first_start:
            print('time:',time()-start)
            first_start = False
    except Exception:
        traceback.print_exc()
        sleep(60)
    # print('time:',time()-start)
    sleep(60*5)