import os
import traceback
from time import time,sleep
from Screening.robots.AgentSmith import AgentSmith

print('Start Send Picks')

smith = AgentSmith('_')
first_start = True
start = time()
while True:
    # start=time()
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