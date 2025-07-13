from strategies.work_strategies.GLTA import GLTA_ALPHA,GLTA_BETA,GLTA_GAMMA,GLTA2_ALPHA,GLTA2_BETA,GLTA2_GAMMA
from Optimiztion.generation_wss.genetics_wss import Evolutionist,Evolutionist2

raw_file = 'DataForTests\DataFromMOEX\MMM5_1_1749581140.csv'
raw_file = 'DataForTests/DataFromMoexFast/5MMM5_1_1749581140.csv'
# raw_file = 'DataForTests\DataFromMoexFast\\5CRM5_1_1749581146.csv'
# evo = Evolutionist2(50,raw_file,GLTA2_ALPHA,[30,60],step_save=10)
# evo = Evolutionist2(100,raw_file,GLTA2_BETA,[20,10,30],step_save=10)
# evo = Evolutionist(100,raw_file,GLTA_BETA,[95,35,30],init_policy='TestNewResults\Evolutionist\GLTA_BETA\BP_1751726635.9605374.json')
evo = Evolutionist2(100,raw_file,GLTA2_GAMMA,[30,100,30,60,30,50],n_save_cores=2,step_save=10,init_policy='TestNewResults\QLearning\GLTA2_GAMMA\Policies\LP_1752353219.json')
if __name__ == '__main__':
    evo.evolution(1000)

