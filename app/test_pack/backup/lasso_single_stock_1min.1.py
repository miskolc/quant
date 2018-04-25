# Close price predict
from googlefinance.client import get_price_data
from sklearn.metrics import mean_squared_error, r2_score
import time
from datetime import datetime
from sklearn.linear_model import LassoCV
from sklearn.model_selection import train_test_split

# ^^^^^^^ need more features
feature = ['open', 'high', 'low', 'volume']


def train(tick_code):
    param = {
        'q': tick_code,  # Stock symbol (ex: "AAPL")
        'i': "60",  # Interval size in seconds ("86400" = 1 day intervals)
        'p': "%sY" % '5'  # Period (Ex: "1Y" = 1 year)
    }
    # get price data (return pandas dataframe)
    df = get_price_data(param)
    # rename columns to lowercase
    df = df.rename(columns={"Open": "open", "High": "high", "Low": "low", "Close": "close", "Volume": "volume"})

    df['next_open'] = df['open'].shift(-1)
    df_now = df.tail(1).copy();

    df = df.dropna()

    df_x_train, df_x_test, df_y_train, df_y_test = train_test_split(df[feature], df['next_open'], test_size=.3, random_state=42)

    # choose linear regression model
    reg = LassoCV(alphas=[1, 0.5, 0.25, 0.1, 0.005, 0.0025, 0.001], normalize=True)

    # fit model with data(training)
    reg.fit(df_x_train, df_y_train)

    # test predict
    df_y_test_pred = reg.predict(df_x_test)

    # The Coefficients (系数 auto gen)
    # The Intercept(截距/干扰/噪声 auto gen)
    print('Coefficients:%s, Intercept:%s, Alpha:%s, Mean squared error: %.2f, Variance score: %.2f' % (
        reg.coef_, reg.intercept_, reg.alpha_, mean_squared_error(df_y_test, df_y_test_pred),r2_score(df_y_test, df_y_test_pred)))

    reg.fit(df[feature], df['next_open'])

    return df_now, reg

pre_predict = 0.0

def predict(df, model):
    # 拿最后一个节点的close price去预测价格

    df_x_now = df[feature].values

    dt = datetime.now()
    df_y_now_pred = model.predict(df_x_now);


    global pre_predict
    if pre_predict == 0:

        pre_predict = df_y_now_pred[0]
        print(
            '%s, 输入价格:%s, 预测价格:%s' % (
                dt.strftime('%Y-%m-%d %H:%M:%S'), df['open'].values[0], df_y_now_pred[0]))
    else:
        deviation = pre_predict - df['open'].values[0]
        pre_predict = df_y_now_pred[0]

        if deviation > 0:
            print(
                '%s, 幅度:\033[0;37;41m%.2f ↑\033[0m,当前价格:%s, 预测价格:%s' % (
                dt.strftime('%Y-%m-%d %H:%M:%S'), deviation, df['open'].values[0], df_y_now_pred[0]))
        else:
            print(
                '%s, 幅度:\033[0;37;42m%.2f ↓\033[0m,当前价格:%s, 预测价格:%s' % (
                    dt.strftime('%Y-%m-%d %H:%M:%S'), deviation, df['open'].values[0], df_y_now_pred[0]))


if __name__ == "__main__":
    while 1 == 1:
        df, reg = train('600179')
        predict(df, reg)
        time.sleep(60)
