import tushare as ts
from app.custom_feature_calculating import feature as feature_service


def get_open_price(code):
    df = ts.get_realtime_quotes(code)

    return df['open'][0]


def get_training_data(code, ktype='D', start=None, end=None):
    df =None
    if start== None and end == None:
        df = ts.get_k_data(code, ktype=ktype)
    else:
        df = ts.get_k_data(code, ktype=ktype, start=start, end=end)

    df = df.set_index('date')
    df = df.sort_index()
    df['next_open'] = df['close'].shift(-1)
    # add feature to df
    df = feature_service.fill(df, ktype)
    df = df.dropna()
    return df


def get_k_data(code, ktype='D', ):
    df = ts.get_k_data(code, ktype=ktype)
    df = df.set_index('date')
    df = df.sort_index()
    # add feature to df
    df = feature_service.fill(df, ktype)

    df = df.dropna()
    return df


if __name__ == "__main__":
    get_training_data('000001', 'D')
