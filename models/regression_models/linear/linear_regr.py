# ae_h - 2018/7/17
from sklearn import linear_model
from sklearn.model_selection import train_test_split
from config import default_config
from dao.k_data.k_data_dao import k_data_dao
import futuquant as ft

ft_ctx = ft.OpenQuoteContext(host=default_config.FUTU_OPEND_HOST,
                                                                       port=default_config.FUTU_OPEND_PORT)

dataframe, feature = k_data_dao.get_k_training_data(code='601398', start='2015-01-01', end='2018-01-01',
                                    futu_quote_ctx=ft_ctx)

# basic data


X = dataframe[feature]

y = dataframe['next_direction']
y = y.fillna(0)

lr_model = linear_model.LinearRegression()

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=.3, shuffle=False, random_state=10)


lr_model.fit(X_train, y_train)

print(lr_model.score(X_test, y_test))





ft_ctx.close()