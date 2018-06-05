# ae_h - 2018/6/5

from keras.layers import SimpleRNN, Dense, Activation,Flatten
import os

from keras import Sequential
from keras.layers import Dense, Dropout
from keras.models import load_model
from sklearn import preprocessing
from sklearn.model_selection import train_test_split

from quant.common_tools.decorators import exc_time
from quant.dao.k_data.k_data_model_log_dao import k_data_model_log_dao
from quant.log.quant_logging import logger
from quant.models.base_model import BaseModel
from quant.models.pca_model import PCAModel
from quant.models.k_data import MODULE_NAME


class RecurrentNeurakClassifier(BaseModel):
    module_name = MODULE_NAME
    model_name = 'recurrent_neural_classifier'

    @exc_time
    def training_model(self, code, data, features):

        X = data[features]
        y = data['next_direction']

        # normalization
        X = preprocessing.scale(X)

        # pca缩放
        pca = PCAModel(self.module_name).load(code)
        X = pca.transform(X)

        X_train, x_test, y_train, y_test = train_test_split(X, y, test_size=.3)

        input_dim_len = len(features)

        # input_shape = X.shape
        rnn_classifier = Sequential()

        rnn_classifier.add(SimpleRNN(units=1, batch_input_shape=(None, 1, input_dim_len)))
        # rnn_classifier.add(Flatten())
        rnn_classifier.add(Dense(1))
        rnn_classifier.add(Activation('softmax'))
        rnn_classifier.compile(optimizer='sgd', loss='binary_crossentropy', metrics=['accuracy'])

        rnn_classifier.fit(X_train, y_train)

        test_model_score = rnn_classifier.evaluate(x_test, y_test)
        logger.debug('test score %s' % test_model_score)



    @exc_time
    def predict(self, code, data):
        pass


