from quant.dao.basic.stock_pool_dao import stock_pool_dao
from quant.dao.k_data.k_data_tech_feature_dao import k_data_tech_feature_dao
from quant.feature_utils.momentum_indicators import acc_kdj
from quant.dao.k_data.k_data_dao import k_data_dao
from quant.common_tools.datetime_utils import get_current_date

def cal_signal(code="600196"):
    data = k_data_tech_feature_dao.get_k_data(code, '2018-07-01',  get_current_date())
    df_k_data = k_data_dao.get_k_data(code, start='2018-06-01', end=get_current_date())

    price = df_k_data['close'].tail(1).values[0]

    ma10 = data['ma10'].values[-1]
    if price < ma10:
        return

    if price < 4:
        return

    k_pre = data['k_value'].values[-2]
    d_pre = data['d_value'].values[-2]

    k = data['k_value'].values[-1]
    d = data['d_value'].values[-1]

    # 上穿, 金叉
    if k_pre < d_pre and abs(k - d) < 1:
        return "up"

    # 下穿, 死叉
    if k_pre > d_pre and abs(k -d) < 1:
        return "down"

    return "hold";



if __name__ == '__main__':

    df_pool = stock_pool_dao.get_list()

    list = []
    for index, row in df_pool.iterrows():
        code = row['code']

        try:
            label = cal_signal(code)

            if label == 'up':
                df_k_data = k_data_dao.get_k_data(code, start='2018-06-01', end='2018-07-05')




                list.append(code)
        except:
            pass
    print(list)

    '''
    label = cal_signal(600017)

    print(label)
    '''