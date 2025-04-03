import os 
import json
from Screening.utils.db_analisys_func import get_best_strategies

class Architect:
    def __init__(self,db_path,granularities,hourss):
        self.db_path = db_path
        self.granularities = granularities
        self.hourss = hourss
        self.folder_picks = 'Screening/strat_picks/'

    def save_file(self,ticker_bot_dict,hours,granularity):
        filename = str(hours) + '_' + str(granularity) + '_' + self.db_path.split('/')[-1].replace('.db','') +  '.json'
        filename = os.path.join(self.folder_picks,filename)
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(ticker_bot_dict, f, ensure_ascii=False, indent=2)
    
    def run(self):
        for granularity in self.granularities:
            for hours in self.hourss:
                res = get_best_strategies(self.db_path,granularity,hours)
                if not res.empty:
                    ticker_bot_dict = res.set_index('ticker')['bot'].to_dict()
                    self.save_file(ticker_bot_dict,hours,granularity)

# if __name__ == "__main__":
#     arch = Architect('dbs/test_MOEX_FUT.db',(1,5),(1,4))
#     arch.run()