# coding = utf-8
# ae_h - 2018/6/1

import xgboost as xgb
from sklearn import preprocessing
from sklearn.metrics import accuracy_score
from quant.models.base_model import BaseModel


from sklearn.model_selection import train_test_split, GridSearchCV


from quant.models.pca_model import PCAModel


class XGBoostClassier(BaseModel):
    def training_model(self, code, data, features):
        X = data[features]
        y = data['next_direction']

        # normalization
        X = preprocessing.scale(X)

        # pca缩放
        pca = PCAModel().load(code)
        X = pca.transform(X)

        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=.3,
                                                            shuffle=False)

        parameters_grid = [{'learning_rate': [0.05, 0.1, 0.3], 'max_depth': range(2, 8, 2), 'subsample': [0.7, ], 'min_child_weight': range(1, 6, 2)}]

        gs_search = GridSearchCV(estimator=xgb.XGBClassifier(n_estimators=100, random_state=10, n_jobs=-1), param_grid=parameters_grid, n_jobs=-1)

        gs_result = gs_search.fit(X_train, y_train)
        print(gs_search.best_params_)
        print(gs_search.best_score_)

        # print(gs_result)



    def predict(self, code, data):
        pass



# xgb_search = GridSearchCV(xgb_model, parameters, scoring='roc_auc')
# xgb_search.fit(X, y)
