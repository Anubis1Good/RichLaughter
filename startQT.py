from time import sleep
from Traders.QuikTrader.work_group import init_trader

bots = init_trader()

for bot in bots:
    print(bot.sec_code)
print('Start trading...')
work = True
while work:
    for bot in bots:
        bot.run()
    sleep(15)
