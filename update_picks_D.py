import traceback
from time import time,sleep
from Screening.robots.AgentSmith import AgentSmith

print('Start Download Update Picks')

smith = AgentSmith('1.json')
first_start = True
start = time()
while True:
    try:
        smith.download_all()
        if first_start:
            print('time:',time()-start)
            first_start = False
        sleep(60*5)
    except Exception:
        traceback.print_exc()
        sleep(60)