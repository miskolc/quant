# coding = utf-8
# ae_h - 2018/5/29

import os

from keras import Sequential
from keras.layers import Dense, Dropout
from keras.models import load_model
from sklearn import preprocessing
from sklearn.model_selection import train_test_split

from quant.common_tools.decorators import exc_time
from quant.dao.k_data_model_log_dao import k_data_model_log_dao
from quant.log.quant_logging import logger
from quant.models.base_model import BaseModel
from quant.models.pca_model import PCAModel
import gc

class SequantialNeural(BaseModel):
    model_name = 'sequantial_neural'

    @exc_time
    def training_model(self, code, data, features):
        X = data[features]
        y = data['next_direction']

        # normalization
        X = preprocessing.scale(X)

        # pca缩放
        pca = PCAModel().load(code)
        X = pca.transform(X)

        X_train, x_test, y_train, y_test = train_test_split(X, y, test_size=.3)

        # normalization
        X_train = preprocessing.scale(X_train)
        x_test = preprocessing.scale(x_test)

        input_dim_len = len(features)

        sequantial_model = Sequential()

        sequantial_model.add(Dense(512, input_dim=input_dim_len, activation='relu'))
        sequantial_model.add(Dropout(0.5))
        sequantial_model.add(Dense(128, activation='relu'))
        sequantial_model.add(Dropout(0.5))

        sequantial_model.add(Dense(1, activation='tanh'))
        sequantial_model.compile(optimizer='sgd', loss='binary_crossentropy', metrics=['accuracy'])

        # traning performance
        sequantial_model.fit(X_train, y_train, epochs=10, batch_size=128)
        train_model_score = sequantial_model.evaluate(X_train, y_train, batch_size=128)

        # test performance
        test_model_score = sequantial_model.evaluate(x_test, y_test, batch_size=128)
        logger.debug('test model score: %s' % test_model_score)

        full_model_score = sequantial_model.evaluate(data[features], data['next_direction'])
        logger.debug('full model score: %s' % full_model_score)

        # 记录日志
        k_data_model_log_dao.insert(code=code, name=self.model_name
                                    , best_estimator=None,
                                    train_score=train_model_score[1], test_score=test_model_score[1]
                                    , desc="full_model_score:%s" % full_model_score[1])
        # 输出模型, 使用h5的格式保存起来
        sequantial_model.save(self.get_model_path(code, self.model_name, 'h5'))


    @exc_time
    def predict(self, code, data):

        model_path = self.get_model_path(code, self.model_name, 'h5')

        if not os.path.exists(model_path):
            logger.error('model not found, code is %s:' % code)
            return

        X = preprocessing.scale(data)

        pac = PCAModel().load(code)
        X = pac.transform(X)

        sequantial_model = load_model(model_path)

        y_pred = sequantial_model.predict(X)

        return int(y_pred[0][0])
