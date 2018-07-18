from common_tools.datetime_utils import get_current_date
from config import default_config
import futuquant as ft

from pitcher.domian.order import Order
from pitcher.domian.position import Position
from dao.k_data.k_data_dao import k_data_dao
from log.quant_logging import logger


class Strategy:
    def init(self, context):
        self.context = context
        self.context.futu_quote_ctx = ft.OpenQuoteContext(host=default_config.FUTU_OPEND_HOST,
                                                          port=default_config.FUTU_OPEND_PORT)

    # 买入
    # percent range is 0~1
    def buy_in_percent(self, code, price, percent):
        if percent > 1:
            raise ValueError('invalid percent')

        if price <= 0:
            raise ValueError('invalid price')
        # 计算最大购买金额
        amount = self.context.base_capital * percent
        # 如果账户余额不足, 退出
        if amount > self.context.blance:
            return

        # 计算购买股数
        shares = int(amount / price / 100) * 100

        # 购买金额
        total = round(shares * price, 2)
        # 扣除账户余额
        self.context.blance -= total

        self.add_portfolio(code=code, price=price, shares=shares, total=total)
        self.add_order_book(code=code, action=1, price=price, shares=shares, total=total,
                            date_time=self.context.current_date)

    def sell_value(self, code, shares):

        position = self.context.portfolio.positions[code]
        total_shares = self.context.portfolio.positions[code].shares

        if shares < 100:
            raise ValueError('percent invalid')

        if shares > total_shares:
            raise ValueError('shares invalid')

        daily_stock_data = k_data_dao.get_k_data(code=code,
                                                 start=get_current_date(self.context.current_date),
                                                 end=get_current_date(self.context.current_date),
                                                 futu_quote_ctx=self.context.futu_quote_ctx)

        price_in = position.price
        price_out = round(daily_stock_data['close'].tail(1).values[0], 2)

        # 卖出金额
        total = round(shares * price_out, 2)
        self.context.blance += total

        profit = round((price_out - price_in) * shares, 2)
        self.context.base_capital += profit

        # 如果全部卖出, 清空portfolio
        if shares == total_shares:
            del self.context.portfolio.positions[code]
        else:
            position.shares -= shares
            total = round(shares * position.price, 2)
            position.total -= total
            self.context.portfolio.positions[code] = position

        # 添加卖出记录
        self.add_order_book(code=code, action=0, price=price_out, shares=shares, total=total,
                            date_time=self.context.current_date)


    def get_portfolio(self, code):

        self.context.protofolio_df.loc(self.context.protofolio_df['code'] == code).head(1)

    def add_portfolio(self, code, price, shares, total):

        if self.context.portfolio.positions.__contains__(code):
            position = self.context.portfolio.positions[code]
            position.price += price
            position.shares += shares
            position.total += total
        else:
            # 新增投资组合
            position = Position(code, price, shares, total)
            # 记录投资组合
            self.context.portfolio.positions[code] = position

    def add_order_book(self, code, action, price, shares, total, date_time):

        order = Order(code=code, action=action, price=price, shares=shares, total=total, date_time=date_time)

        self.context.order_book.append(order)
