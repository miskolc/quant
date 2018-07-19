
'''
    仓位类
'''
class Position(object):

    def __init__(self, code, price, shares, total):
        # 股票代码
        self.code = code
        # 价格
        self.price = price
        # 股数
        self.shares = shares
        # 总金额
        self.total = total


    def __str__(self):
        # Override to print a readable string presentation of your object
        # below is a dynamic way of doing this without explicity constructing the string manually
        return ', '.join(['{key}={value}'.format(key=key, value=self.__dict__.get(key)) for key in self.__dict__])
