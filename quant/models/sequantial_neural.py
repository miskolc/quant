# coding = utf-8
# ae_h - 2018/5/29
from datetime import datetime

from keras import Sequential
from keras.layers import Dense, Dropout
from sklearn import preprocessing
from sklearn.model_selection import train_test_split

from quant.dao.k_data_dao import k_data_dao
from quant.feature_utils.feature_collector import collect_features
from quant.models.base_model import BaseModel


class SequantialNeural(BaseModel):

    def training_model(self, code):
        data = k_data_dao.get_k_data(code, '2015-01-01', datetime.now().strftime("%Y-%m-%d"))

        data, features = collect_features(data)

        X_train, x_test, Y_train, y_test = train_test_split(data[features], data['next_direction'], test_size=.3)

        # normalization
        X_train = preprocessing.scale(X_train)
        x_test = preprocessing.scale(x_test)

        input_dim_len = len(features)

        sequantial_model = Sequential()

        sequantial_model.add(Dense(512, input_dim=input_dim_len, activation='relu'))
        sequantial_model.add(Dropout(0.5))
        sequantial_model.add(Dense(128, activation='relu'))
        sequantial_model.add(Dropout(0.5))
        # sequantial_model.add(Dense(64, activation='relu'))
        # sequantial_model.add(Dropout(0.5))
        # sequantial_model.add(Dense(16, activation='relu'))
        # sequantial_model.add(Dropout(0.5))
        sequantial_model.add(Dense(1, activation='tanh'))
        sequantial_model.compile(optimizer='sgd', loss='binary_crossentropy', metrics=['accuracy'])

        # sequantial_model.summary()

        # traning performance
        sequantial_model.fit(X_train, Y_train, epochs=10, batch_size=128)

        # test performance
        test_model_score = sequantial_model.evaluate(x_test, y_test, batch_size=128)
        print('test model score: %s' % test_model_score)

        # whole data performance
        # sequantial_model.fit(data[features], data['next_direction'])

        full_model_score = sequantial_model.evaluate(data[features], data['next_direction'])
        print('full model score: %s' % full_model_score)

        # summary
        sequantial_model.summary()