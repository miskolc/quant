# ae_h - 2018/7/13

class Context:

    def __init__(self, start, end, base_capital):
        self.start = start
        self.end = end
        self.base_capital = base_capital

    def __getattr__(self, item):
        return item
