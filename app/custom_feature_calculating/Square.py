import pandas as pd


# 某一列的平方
def Square(data, name):
    data['square_%s' % name] = data[name] ** 2
    return data
