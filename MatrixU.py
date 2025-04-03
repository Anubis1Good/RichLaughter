import os
import traceback
from time import time,sleep
from Screening.robots.Architect import Architect
from Screening.robots.AgentSmith import AgentSmith

archs = (
    Architect(
        'dbs/test_Bitget_FUT.db',
        ('1m','5m','15m','30m','1H'),
        (1,4)
        ),
    Architect(
        'dbs/test_MOEX_FUT.db',
        (1,5),
        (1,4)),
    Architect(
        'dbs/test_MOEX_STOCK.db',
        (1,5),
        (1,4)),
)


while True:
    start=time()
    try:
        for arch in archs:
            arch.run()
        files = os.listdir('Screening/strat_picks')
        for file in files:
            if not file.startswith('u'):
                # print(file,'uploads...')
                AgentSmith(file).upload()
                sleep(10)
    except Exception:
        traceback.print_exc()
        sleep(60)
    print('time:',time()-start)
    # sleep(60*5)