# Close price predict
import tushare as ts#
from googlefinance.client import get_price_data, get_prices_data, get_prices_time_data

from sqlalchemy import create_engine
import custom_feature_calculating.BBANDS as featureLibBB
import custom_feature_calculating.CCI as featureLibCCI
import custom_feature_calculating.FI as featureLibFI
import custom_feature_calculating.EMV as featureLibEVM
import custom_feature_calculating.EWMA as featureLibEWMA
import custom_feature_calculating.SMA as featureLibSMA
import custom_feature_calculating.ROC as featureLibROC
import custom_feature_calculating.Square as featureLibSquare
from sklearn.metrics import mean_squared_error, r2_score
import matplotlib.pyplot as plt
from sklearn import linear_model
import time
from datetime import datetime
import pandas as pd
from sklearn import preprocessing

# data collecting
# or extract from db
tick_code = '601211'

def predict():
    engine = create_engine('mysql+pymysql://root:root@localhost:3306/quantitative')
    
    sql = 'SELECT  t1.open, t1.close, t1.high, t1.low, t1.vol as volume,t2.close as rt_sh'\
          ' from tick_data_1min t1'\
          ' LEFT JOIN tick_data_1min t2 on t1.datetime = t2.datetime and t2.code=\'000001\''\
          ' where t1.code in (\'600179\',\'601211\',\'600270\',\'600057\')'

    df = pd.read_sql_query(sql, engine)

    n = 10
    # add feature to df
    df = featureLibBB.BBANDS(df, n)
    df = featureLibCCI.CCI(df, 20)
    df = featureLibFI.ForceIndex(df, n)
    df = featureLibEVM.EVM(df, n)
    df = featureLibEWMA.EWMA(df, n)
    df = featureLibSMA.SMA(df,5)
    df = featureLibSMA.SMA(df,10)
    df = featureLibSMA.SMA(df,20)
    df = featureLibROC.ROC(df,n)
    df = df.dropna()
    print(df.tail(1))
    # Normalization
    df_norm = (df - df.mean()) / (df.max() - df.min())
    df = df_norm
    print(df.tail(1))
    #df.to_csv("result.csv")

    feature = ['open', 'ubb', 'lbb', 'evm', 'ewma', 'fi', 'ma5','ma10','ma20','roc','rt_sh']
    # ^^^^^^^ need more features

    count = len(df.index)
    # traning
    train_count = int(len(df.index) * 0.8)
    # testing
    test_count = int(len(df.index) * 0.2)

    # cross validation miss
    # !!!!!!!!!!!!!!!!!!


    ### !!!!!IMPROVEMENT
    # get all x data 
    df_x_all = df[feature].values

    # get all y data 
    df_y_all = df['close'].values

    # get x traning custome features head n rows
    df_x_train = df[feature].head(train_count).values

    # get traning close price head n rows
    df_y_train = df['close'].head(train_count).values

    # get x testing custome feature tail n rows
    df_x_test = df[feature].tail(test_count).values

    # get y tesing custome close price n rows
    df_y_test = df['close'].tail(test_count).values

    # choose linear regression model
    reg = linear_model.LinearRegression()

    # fit model with data(training)
    reg.fit(df_x_train, df_y_train)

    # test predict
    df_y_test_pred = reg.predict(df_x_test)

    # The Coefficients (系数 auto gen)
    print('Coefficients: \n', reg.coef_)
    # The Intercept(截距/干扰/噪声 auto gen)
    print('Intercept: \n', reg.intercept_)
    # The mean squared error(均方误差)
    print("Mean squared error: %.2f"% mean_squared_error(df_y_test, df_y_test_pred))

    # r2_score - sklearn评分方法
    print('Variance score: %.2f' % r2_score(df_y_test, df_y_test_pred))

    reg.fit(df_x_all, df_y_all)

    # 回测?
    #df_y_all_pred = reg.predict(df_x_all)
    #print('the difference =', np.subtract(df_y_all, df_y_all_pred))

    # 拿最后一个节点的close price去预测价格
    #df_now = df.tail(1)
    #df_now['open'] = df_now['close']
    #df_x_now = df_now[feature].values

    #dt = datetime.now()  
    #print('当前时间:%s, 输入价格:%s' % (dt.strftime( '%Y-%m-%d %H:%M:%S' ) ,df_now[['open']].values))
    #df_y_toady_pred = reg.predict(df_x_now);
    #print('预测价格:%s' % df_y_toady_pred)

    # Plot outputs
    plt.scatter(df_x_test[:, 0], df_y_test, color='black')
    plt.plot(df_x_test[:, 0], df_y_test_pred, color='blue', linewidth=3)
    #plt.xlim((15.5, 15.6))
    #plt.ylim((15.5, 15.6))
    plt.show()


if __name__ == "__main__":
  
    predict()
       
 
   