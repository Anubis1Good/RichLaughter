import requests

import apimoex
import pandas as pd


with requests.Session() as session:
    data = apimoex.get_board_candles(session, 'SNGSP',1,'2025-02-01')
    df = pd.DataFrame(data)
    # df.set_index('TRADEDATE', inplace=True)

    print(df.head(), '\n')
    print(df.tail(), '\n')
    df.info()