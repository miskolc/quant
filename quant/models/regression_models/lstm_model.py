# ae_h - 2018/6/6
import numpy as np  # linear algebra
import pandas as pd  # data processing, CSV file I/O (e.g. pd.read_csv)

from subprocess import check_output
from keras.layers.core import Dense, Activation, Dropout
from keras.layers.recurrent import LSTM
from keras.models import Sequential
from sklearn.model_selection import train_test_split
import time  # helper libraries
from sklearn.preprocessing import MinMaxScaler
import matplotlib.pyplot as plt
from numpy import newaxis
from quant.models.base_model import BaseModel
import numpy as np


class LSTMModel(BaseModel):
    def training_model(self, code, data, features, *args):
        stock_price = data['close']

        stock_price = stock_price.reshape((stock_price.shape[0], 1))

        # MinMaxScaler

        scaler = MinMaxScaler(feature_range=(0, 1))
        X = scaler.fit_transform(stock_price)

        train_size = int(len(stock_price) * 0.80)
        test_size = len(stock_price) - train_size
        train, test = stock_price[0:train_size, :], stock_price[train_size:len(stock_price), :]

        print(type(train))
        print(type(test))

        trainX, trainY = self.create_dataset(train, look_back=1)
        testX, testY = self.create_dataset(test, look_back=1)

        trainX = np.reshape(trainX, (trainX.shape[0], 1, trainX.shape[1]))
        testX = np.reshape(testX, (testX.shape[0], 1, testX.shape[1]))

        lstm_model = Sequential()
        lstm_model.add(LSTM(
            input_dim=1,
            output_dim=50,
            return_sequences=True))
        lstm_model.add(Dropout(0.2))

        lstm_model.add(LSTM(
            100,
            return_sequences=False))
        lstm_model.add(Dropout(0.2))

        lstm_model.add(Dense(
            output_dim=1))
        lstm_model.add(Activation('linear'))

        lstm_model.compile(optimizer='rmsprop', loss='mse', metrics=['accuracy'])

        lstm_model.fit(trainX, trainY, batch_size=100, epochs=150, validation_split=0.05)

    def create_dataset(self, dataset, look_back=1):
        dataX, dataY = [], []
        for i in range(len(dataset) - look_back - 1):
            a = dataset[i:(i + look_back), 0]
            dataX.append(a)
            dataY.append(dataset[i + look_back, 0])
        return np.array(dataX), np.array(dataY)

    def predict(self, code, data):
        pass
