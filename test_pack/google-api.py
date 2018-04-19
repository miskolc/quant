from googlefinance.client import get_price_data, get_prices_data, get_prices_time_data

param = {
    'q': '600000', # Stock symbol (ex: "AAPL")
    'i': "60" # Interval size in seconds ("86400" = 1 day intervals)
    #'p': "%sY" % '1' # Period (Ex: "1Y" = 1 year)
}
# get price data (return pandas dataframe)
df = get_price_data(param)
df = df.rename(columns={"Open": "open", "High": "high", "Close":"close", "Volume":"volume"})
print(df)