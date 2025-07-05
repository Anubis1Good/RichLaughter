from strategies.work_strategies.GLTA import GLTA_ALFA,GLTA_BETA
from Optimiztion.generation_wss.genetics_wss import Evolutionist

raw_file = 'DataForTests\DataFromMOEX\MMM5_1_1749581140.csv'
# evo = Evolutionist(3,50,raw_file,GLTA_ALFA,[30,60])
evo = Evolutionist(100,raw_file,GLTA_BETA,[30,10,30])
if __name__ == '__main__':
    evo.evolution(100)

