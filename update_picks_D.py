import traceback
from time import time,sleep
from Screening.robots.AgentSmith import AgentSmith

smith = AgentSmith('1.json')

while True:
    try:
        start = time()
        smith.download_all()
        # print('time:',time()-start)
        sleep(60*5)
    except Exception:
        traceback.print_exc()
        sleep(60)