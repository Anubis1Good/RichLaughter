import pandas as pd
def get_direction(row):
    if row['open'] < row['close']:
        return 1
    return -1
def change_dt(dt):
    hour = int(dt[-5:-3])
    minute = round(int(dt[-2:])/60,2)
    return hour + minute
def quik_loader(raw_file):
    df = pd.read_csv(raw_file,sep='\t')
    df = df.drop_duplicates()
    df['direction'] = df.apply(get_direction,axis=1)
    df = df.reset_index()
    df['x'] = df.index
    df['hour'] = df['datetime'].apply(change_dt)
    df = df.drop(['index','datetime','open','close'],axis=1)
    return df

raw_file = 'DataForTests\DataFromQuik\SPBFUT.MMU4_T1.txt'


df = quik_loader(raw_file)

print(df.sample(5))