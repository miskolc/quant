import tushare as ts


#  add pre price feature
def fill(df):
    df['pre_close'] = df['close'].shift(1)
    return df;


if __name__ == "__main__":
    df = ts.get_hist_data('600179')
    df = df.sort_index()
    df['pre_close'] = df['close'].shift(1)
    df['next_open'] = df['open'].shift(-1)
    print(df[["open", "close",'pre_close',"next_open"]])


