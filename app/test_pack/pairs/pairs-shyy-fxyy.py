import tushare as ts
import pandas as pd
from sklearn.linear_model import LinearRegression
from app.test_pack.pairs.hurst import hurst
import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import datetime
from app.common_tools.GBM_verify import gmb_test

def plot_res_series(df, ts1):
    months = mdates.MonthLocator()  # every month
    fig, ax = plt.subplots()
    ax.plot(df['date'], df[ts1], label=ts1)
    #ax.xaxis.set_major_locator(months)
    #ax.xaxis.set_major_formatter(mdates.DateFormatter('%b %Y'))
    #ax.set_xlim(datetime.datetime(2017, 4, 1), datetime.datetime(2018, 4, 1))
    ax.grid(True)
    fig.autofmt_xdate()

    plt.xlabel('差值')
    plt.ylabel('Price ($)')
    plt.title('601607 / 600196')
    plt.legend()
    plt.show()

def plot_price_series(df, ts1, ts2):
    months = mdates.MonthLocator()  # every month
    fig, ax = plt.subplots()
    ax.plot(df['date'], df[ts1], label=ts1)
    ax.plot(df['date'], df[ts2], label=ts2)
    ax.xaxis.set_major_locator(months)
    #ax.xaxis.set_major_formatter(mdates.DateFormatter('%b %Y'))
    #ax.set_xlim(datetime.datetime(2017, 4, 1), datetime.datetime(2018, 4, 1))
    ax.grid(True)
    fig.autofmt_xdate()

    plt.xlabel('Month/Year')
    plt.ylabel('Price ($)')
    plt.title('%s and %s Daily Prices' % (ts1, ts2))
    plt.legend()
    plt.show()


df_g = ts.get_k_data("600196", start='2017-01-01')
df_m = ts.get_k_data("601607", start='2017-01-01')

#df_g["date"] = pd.to_datetime(df_g["date"])
df_g = df_g.set_index('date')

#df_m["date"] = pd.to_datetime(df_m["date"])
df_m = df_m.set_index('date')


#df = pd.DataFrame()
#mean = (df_m["close"] / df_g["close"]).mean()
#std = (df_g["close"] / df_m["close"]).std()
#window = (mean - std, mean + std)

# print(mean)
# print(std)
#print(window)


df = pd.DataFrame( index=df_m.index,columns=['601607', '600196', 'date'])


df["600196"] = df_g["close"]
df["601607"] = df_m["close"]

df["date"] = pd.to_datetime(df.index)
df = df.dropna()



#reg = LinearRegression()
#reg.fit(df["600196"].values.reshape(-1, 1), df["601607"].values.reshape(-1, 1))
#x = reg.coef_[0][0]


df["close"] = df["601607"] /df["600196"]
df.to_csv('result.csv')
print("平均值",df["close"].mean())
print("方差",df["close"].std())
print("区间",df["close"].mean() + df["close"].std(), df["close"].mean() -df["close"].std() )
# H<0.5 The time series is mean revert
#hres = hurst(df["close"])
#print("hres:"+hres)

gmb_test(df)

print(df.tail(50))

plot_price_series(df, "600196", "601607")
plot_res_series(df, "close")