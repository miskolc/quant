# ae.h - 2018/5/4
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from sklearn import preprocessing
import time

df = pd.read_csv('/Users/yw.h/Downloads/result.csv')
# print(df['date'])
df = df.set_index('date')

df['datetime'] = df.index
# df = df.set_index(df['date'])

df['time'] = [t[11:][:5] for t in df.index.values]

df.index = pd.to_datetime(df.index)
df.index = df.index.strftime('%Y-%m-%d')
# df['datetime'] = df.index.values

# df = df.set_index(pd.MultiIndex.from_arrays([df.index.values, df['datetime'].values], names=['date', 'datetime']))


# df = df.sort_values(by=['datetime'])

date_index = (pd.DataFrame(df.index).drop_duplicates())[0].values
# print(date_index)
date_index = list(date_index)

print(date_index)
df['time'] = df.sort_values(by=['datetime'])

start = pd.Timestamp('9:30')
end = pd.Timestamp('15:30')


# print('done')
fig, ax = plt.subplots(figsize=(18, 10))
#
for date in date_index[:10]:
    ax.plot(df['time'][:len(df.ix[date]['macd'])], df.ix[date]['macd'], label=date)
    ax.xaxis.set_major_locator(ticker.MultipleLocator(5))

ax.grid(True)
plt.xlabel('time(from 9:30 to 15:00)')
plt.ylabel('MACD curve')
plt.xticks([])
plt.legend()
plt.show()



# ndf = df.ix['2018-01-02']
# print(len(df.ix['2018-01-02']['macd']))
# print(len(df.ix['2018-01-02']['time']))
#
# ax.plot(ndf['time'], ndf['macd'], label='2018-01-02')




# ax.plot(df['time'][:len(df.ix['2018-01-02']['macd'])], df.ix['2018-01-02']['macd'], label='2018-01-02')
# ax.grid(True)
# plt.xticks(rotation=60)
# plt.legend()
# plt.show()
