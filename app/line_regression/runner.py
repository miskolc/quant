import app.line_regression.lasso_single_stock as lasso_single_stock
import app.line_regression.ridge_regression_single_stock as ridge_regression_single_stock
import app.line_regression.svr_single_stock as svr_single_stock
import tushare as ts
import app.line_regression.linear_regression_single_stock as linear_regression_single_stock
from app.dao.price_service import get_training_data, get_k_data

if __name__ == "__main__":
    list = ['002510',]
    #list = ['600',  ]
    ktype = 'D'

    rs = []
    for code in list:
        df = get_training_data(code, ktype)

        df_now = get_k_data(code, ktype)
        df_now.to_csv('result.csv')

        df_rea = ts.get_realtime_quotes(code)
        svr_price, price = svr_single_stock.predict(code, df=df, df_now=df_now)
        #lr_price = linear_regression_single_stock.predict(code, df=df, df_now=df_now)
        lasso_price = lasso_single_stock.predict(code, df=df, df_now=df_now)
        ridge = ridge_regression_single_stock.predict(code, df=df, df_now=df_now)
        str = 'code: {}, name: {}, price: {}, SVR: {}, Lasso: {}, Ride: {}'. \
            format(code, df_rea['name'].tail(1)[0], price, svr_price[0], lasso_price[0], ridge[0])
        rs.append(str)

    for str in rs:
        print(str)
