# ae.h - 2018/5/14
from keras import Sequential
from keras.layers import Dense, Activation, Dropout
from sklearn.model_selection import train_test_split
import pandas as pd
import numpy as np
import tushare as ts

df = ts.get_hist_data('600179', start='2017-01-01', end='2018-04-04', ktype='D')

pred_df = ts.get_hist_data('600179', start='2018-05-10', end='2018-05-10', ktype='D')

n_features = list(df.columns.values)

df['direction'] = np.where(df['price_change'].shift(-1) > 0, 1, 0)

X_train, x_test, Y_train, y_test = train_test_split(df[n_features], df['direction'], test_size=.3)

feature_len = len(n_features)
model = Sequential()
model.add(Dense(64, input_dim=feature_len, activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(64, activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(32, activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(16, activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(1, activation='sigmoid'))
model.compile(optimizer='rmsprop', loss='binary_crossentropy', metrics=['accuracy'])

model.summary()

model.fit(X_train, Y_train, epochs=20, batch_size=32)
score = model.evaluate(x_test, y_test, batch_size=128)

prediction = model.predict(pred_df)

print(prediction)
