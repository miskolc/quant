# # ae.h - 2018/4/25
# import tushare as ts
# import numpy as np
# import matplotlib.pyplot as plt
# from sklearn import cross_validation
# import pandas as pd
# from sklearn import linear_model
#
# df = ts.get_hist_data('600179')
#
# x = np.array(df[['open']])
# y = np.array(df['close'])
#
#
# # plt.scatter(x, y)
# # plt.show()
# x_train, x_test, y_train, y_test = cross_validation.train_test_split(x, y, test_size=0.3, random_state=0)
#
# LR_model = linear_model.LinearRegression()
# LR_model.fit(x_train, y_train)
# print(LR_model.score(x_train, y_train))
#
#
# predict_list = list(LR_model.predict(x_test))
#
# temp_list = []
# for item in predict_list:
#     temp_list.append(np.format_float_positional(np.float16(item)))
#
# fin_list = []
# for item in temp_list:
#     fin_list.append(float(item))
#
# print(fin_list)
# print(len(fin_list))
# print(list(y_test))
# print(len(y_test))
#
# print(sum((y_test - LR_model.predict(x_test)) **2))
