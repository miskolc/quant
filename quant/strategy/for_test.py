# ae_h - 2018/6/2
import tushare as ts

from quant.common_tools.decorators import exc_time


hs_300 = ts.get_hs300s()
code_list = list(hs_300['code'])

pair_list = []

@exc_time
def for_test_test():

    for i in range(0, len(code_list)):
        for j in range(1, len(code_list)):
            pair_list.append((code_list[i], code_list[j]))

    print(pair_list)



if __name__ == '__main__':

    for_test_test()