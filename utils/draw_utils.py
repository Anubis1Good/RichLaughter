import matplotlib.pyplot as plt

def draw_chart(df):
    plt.subplot(2,1,1)
    plt.plot(df['high'])
    plt.plot(df['low'])
    plt.subplot(2,1,2)
    plt.plot(df['volume'])

def draw_lite_chart(df):
    plt.plot(df['high'])
    plt.plot(df['low'])

def draw_hb_chart(row):
    clr = '#b7ea00' if row['direction'] == 1 else '#ff0013'
    plt.vlines(row.name,row['low'],row['high'],colors=clr)


def draw_hbwv_chart(row):
    clr = '#b7ea00' if row['direction'] == 1 else '#ff0013'
    plt.subplot(2,1,1)
    plt.vlines(row.name,row['low'],row['high'],colors=clr)
    plt.subplot(2,1,2)
    plt.vlines(row.name,0,row['volume'],colors='#6c6eff')


def draw_chart_channel(df):
    plt.plot(df['max_hb'])
    plt.plot(df['min_hb'])
    plt.plot(df['avarege'])

def draw_bollinger(df,clr='blue'):
    plt.plot(df['bbu'],color=clr)
    plt.plot(df['bbd'],color=clr)
    plt.plot(df['sma'],color=clr)

def draw_dynamics(df,clr='red'):
    df.apply(lambda row: plt.text(row.name,row['low'],round(row['dynamics_ma'],1), fontsize=10,rotation='vertical'),axis=1)