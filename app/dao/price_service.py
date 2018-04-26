import tushare as ts
from app.custom_feature_calculating import feature as feature_service


def get_open_price(code):
    df = ts.get_realtime_quotes(code)

    return df['open'][0]


def get_training_data(code, ktype='D'):
    df = ts.get_k_data(code, ktype=ktype, start='2016-01-01')
    df = df.set_index('date')
    df = df.sort_index()
    df['next_open'] = df['open'].shift(-1)

    # add feature to df
    df = feature_service.fill(df, ktype)
    df = df.dropna()
    return df


def get_k_data(code, ktype='D'):
    df = ts.get_k_data(code, ktype=ktype, start='2016-01-01')
    df = df.set_index('date')
    # add feature to df
    df = feature_service.fill(df, ktype)

    df = df.sort_index()
    df = df.dropna()
    return df

get_k_data
if __name__ == "__main__":
    get_training_data('600179', '5')
