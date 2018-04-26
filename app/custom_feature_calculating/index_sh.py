import tushare as ts


#  加入上证指数特征
def fill(df, ktype='D'):
    df_sh = ts.get_k_data("sh",ktype=ktype)
    df_sh = df_sh.set_index('date')

    df['sh_open'] = df_sh['open']
    df['sh_close'] = df_sh['close']

    return df


if __name__ == "__main__":
    df_sh = ts.get_k_data("sh")
    print(df_sh.tail(1))
    pass
