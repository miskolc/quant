# ae_h - 2018/6/2
import tushare as ts

from quant.common_tools.decorators import exc_time

hs_300 = ts.get_hs300s()
code_list = list(hs_300['code'])




@exc_time
def for_test_test():
    temp_set = set()
    for i in range(0, len(code_list)):
        for j in range(1, len(code_list)):
            code1 = code_list[i]
            code2 = code_list[j]
            code_tuple = sorted((code1, code2))
            temp_set.add((code_tuple[0], code_tuple[1]))

    print(len(temp_set))


if __name__ == '__main__':
    for_test_test()
