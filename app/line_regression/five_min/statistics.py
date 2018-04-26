import app.line_regression.five_min.lasso_single_stock_5min as lasso_single_stock_5min
import app.line_regression.five_min.linear_regression_single_stock_5min as linear_regression_single_stock_5min
import app.line_regression.five_min.svr_single_stock_5min as svr_single_stock_5min
import tushare as ts

if __name__ == "__main__":
    list = ('600179','000001','000725', '601211', '600000','600050','000651')

    rs = []
    for code in list:
        df = ts.get_realtime_quotes(code)
        svr_price = svr_single_stock_5min.predict(code)
        lr_price = linear_regression_single_stock_5min.predict(code)
        lasso_price = lasso_single_stock_5min.predict(code)

        str = 'code: {}, name: {}, price: {}, SVR: {}, LR: {}, Lasso: {}'.format(code,df['name'].tail(1)[0],df['price'].tail(1)[0],svr_price[0], lr_price[0], lasso_price[0])
        rs.append(str)

    for str in rs:
        print(str)