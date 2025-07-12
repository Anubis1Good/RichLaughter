from strategies.work_strategies.GLTA import GLTA_ALPHA,GLTA2_BETA,GLTA_GAMMA
from Optimiztion.RLs.agents.QAgent1 import QAgent1
from Optimiztion.RLs.envs.QEnv1 import QEnv1

raw_file = 'DataForTests\DataFromMOEX\MMM5_1_1749581140.csv'
# raw_file = 'DataForTests/DataFromMoexFast/5MMM5_1_1749581140.csv'

# env = QEnv1(raw_file,GLTA_ALPHA,[20,])
env = QEnv1(raw_file,GLTA2_BETA,[95,35,30])
# agent = QAgent1(env,n_episodes=100)
agent = QAgent1(env,n_episodes=500,start_q='TestNewResults\QLearning\GLTA2_BETA\QTables\QTable_1752317722.094099.npy')

if __name__ == '__main__':
    agent.train()

    # pass