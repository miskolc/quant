from googlefinance.client import get_price_data, get_prices_data, get_prices_time_data

param_sh = {
    'q': '000001', # Stock symbol (ex: "AAPL")
    'i': "60", # Interval size in seconds ("86400" = 1 day intervals)
    'p': "%sY" % '5' # Period (Ex: "1Y" = 1 year)
}
# get price data (return pandas dataframe)
df_sh = get_price_data(param_sh)


param = {
    'q': '600179', # Stock symbol (ex: "AAPL")
    'i': "60", # Interval size in seconds ("86400" = 1 day intervals)
    'p': "%sY" % '5' # Period (Ex: "1Y" = 1 year)
}
    # get price data (return pandas dataframe)
df = get_price_data(param)

df['sh_open'] = df_sh['Open']

print(df.head())


#rename cloumns to lowercase
df = df.rename(columns={"Open": "open", "High": "high","Low":"low", "Close":"close", "Volume":"volume"})


df = df.rename(columns={"Open": "open", "High": "high", "Close":"close", "Volume":"volume"})
