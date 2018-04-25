import tushare as ts


#  加入上证指数特征
def fill(df):
    df_sh = ts.get_hist_data("sh")

    df['sh_open'] = df_sh['open']
    df['sh_close'] = df_sh['close']
    pass


if __name__ == "__main__":

    pass
