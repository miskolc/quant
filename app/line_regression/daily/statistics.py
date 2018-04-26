import app.line_regression.daily.lasso_single_stock_daliy as lasso_single_stock_daliy
import app.line_regression.daily.linear_regression_single_stock_daily as linear_regression_single_stock_daily
import app.line_regression.daily.svr_single_stock_daily as svr_single_stock_daily
import tushare as ts

if __name__ == "__main__":
    list = ('600179','000001','000725', '601211', '600000','600050','000651','601398')

    rs = []
    for code in list:
        df = ts.get_realtime_quotes(code)
        svr_price = svr_single_stock_daily.predict(code)
        lr_price = linear_regression_single_stock_daily.predict(code)
        lasso_price = lasso_single_stock_daliy.predict(code)

        str = 'code: {}, name: {}, price: {}, SVR: {}, LR: {}, Lasso: {}'.format(code,df['name'].tail(1)[0],df['price'].tail(1)[0],svr_price[0], lr_price[0], lasso_price[0])
        rs.append(str)

    for str in rs:
        print(str)