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

def draw_chart_channel(df):
    plt.plot(df['max_hb'])
    plt.plot(df['min_hb'])
    plt.plot(df['avarege'])