from strategies.work_strategies.GLTA import GLTA_ALPHA,GLTA_BETA,GLTA_GAMMA
from Optimiztion.generation_wss.genetics_wss import Evolutionist

raw_file = 'DataForTests\DataFromMOEX\MMM5_1_1749581140.csv'
# evo = Evolutionist(50,raw_file,GLTA_ALPHA,[30,60],step_save=1)
# evo = Evolutionist(100,raw_file,GLTA_BETA,[95,35,30],init_policy='TestNewResults\Evolutionist\GLTA_BETA\BP_1751726635.9605374.json')
evo = Evolutionist(100,raw_file,GLTA_GAMMA,[20,100,30,60,30,50],n_save_cores=1,step_save=3)
if __name__ == '__main__':
    evo.evolution(1000)

