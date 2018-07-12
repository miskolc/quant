# ae_h - 2018/7/8
from models.base_model import BaseModel
from common_tools import exc_time
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn import svm
import math
from dao.basic.stock_basic_dao import stock_basic_dao


class MultiFactorSVRModel(BaseModel):
    @exc_time
    def training_model(self, code, data, features, *args):
        data['IND'] = 1
        data['b'] = data['total_assets'] - data['total_liabilities']
        data['retained_profits'] = data['retained_profits'].map(lambda x: math.log(abs(x)) * 1) if data['retained_profits'].values < 0 else data['retained_profits'].map(lambda x: math.log(abs(x)))
        data['lev'] = data['total_assets']/data['total_liabilities']
        data['rd'] = 0
        data = data.fillna(method='ffill')

        features = ['IND', 'b', 'retained_profits', 'lev', 'income_yoy']
        X = data[features]
        print(X)
        y = data['total_market']
        print(y)

        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=.3, shuffle=False, random_state=10)
        tuned_parameters = [
            {'kernel': ['rbf'], 'gamma': [1e-3, 1e-4], 'C': [1, 10, 100, 1000]}
        ]

        svr_model = GridSearchCV(svm.SVR(), tuned_parameters, n_jobs=-1)
        svr_model.fit(X_train, y_train)

        test_score = svr_model.score(X_test, y_test)

        print(test_score)
        return svr_model

    def predict(self, code, data):
        pass


if __name__ == '__main__':
    features = ['IND', 'b', 'retained_profits', 'lev', 'income_yoy']
    svr_model = MultiFactorSVRModel()
    data = stock_basic_dao.get_by_code(code='600196')
    svr_model.training_model(code='600196', data=data, features=features)
