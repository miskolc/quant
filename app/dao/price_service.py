import tushare as ts


def get_open_price(code):
    df = ts.get_realtime_quotes(code)

    return df['open'][0]


if __name__ == "__main__":
    get_open_price('600179')
