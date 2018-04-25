import tushare as ts


#  add pre price feature
def fill(df):
    df['pre_close'] = df['close'].shift(-2)
    return df;


if __name__ == "__main__":
    df = ts.get_hist_data('600179')
    df['pre_close'] = df['close'].shift(-2)
    print(df[["pre_close", "close"]])


