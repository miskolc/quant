import tushare as ts


#  add pre code price feature
def fill(data):
    pass


if __name__ == "__main__":
    df = ts.get_hist_data('600179')
    df['pre_close'] = df['close'].shift(-1)
    print(df[["pre_close", "close"]])


