

class Order(object):
    def __init__(self, code, action, shares, price, total, date_time, trade_fee):
        self.code = code
        self.action = action
        self.shares = shares
        self.price =price
        self.total = total
        self.date_time = date_time
        self.trade_fee = trade_fee

