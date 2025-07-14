from strategies.work_strategies.GLTA import GLTA2_ALPHA,GLTA2_BETA,GLTA2_GAMMA
from Optimiztion.RLs.agents.QAgent1 import QAgent1,QAgent1GPU
from Optimiztion.RLs.envs.QEnv1 import QEnv1

raw_file = 'DataForTests\DataFromMOEX\MMM5_1_1749581140.csv'
# raw_file = 'DataForTests/DataFromMoexFast/5MMM5_1_1749581140.csv'

# env = QEnv1(raw_file,GLTA2_ALPHA,[20,10])
env = QEnv1(raw_file,GLTA2_BETA,[30,15,30])
# env = QEnv1(raw_file,GLTA2_GAMMA,[30,100,30,60,30,50])
# agent = QAgent1(env,n_episodes=100)
agent = QAgent1(env,n_episodes=3000,start_q=None)
# agent = QAgent1GPU(env,n_episodes=500,start_q=None)

if __name__ == '__main__':
    agent.train()

    # pass