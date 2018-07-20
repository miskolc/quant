from common_tools.datetime_utils import get_current_date
from common_tools.trade_fee_utlis import cal_commission_fee, cal_tax_fee
from config import default_config
import futuquant as ft

from pitcher.domain.order import Order
from pitcher.domain.position import Position
from dao.k_data.k_data_dao import k_data_dao
from log.quant_logging import logger
from pitcher.domain.profit import Profit


class Strategy:
    def init(self, context):
        self.context = context
        self.futu_quote_ctx = ft.OpenQuoteContext(host=default_config.FUTU_OPEND_HOST,
                                                          port=default_config.FUTU_OPEND_PORT)

    def before_handle_data(self):

        if len(self.context.portfolio.positions) == 0:
            # 记录当日收益
            self.context.profits.append(Profit(self.context.current_date, 0))
            return

        p_total = 0.0
        for code, position in self.context.portfolio.positions.items():
            daily_stock_data = k_data_dao.get_k_data(code=code,
                                                     start=self.context.current_date,
                                                     end=self.context.current_date,
                                                     futu_quote_ctx=self.futu_quote_ctx)

            price = daily_stock_data['close'].tail(1).values[0]

            p_total += price * position.shares
        # 计算净资产
        net_asset = p_total + self.context.blance
        # 记录当日收益
        self.context.profits.append(Profit(self.context.current_date, net_asset/self.context.init_capital))



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
        total = shares * price

        # 交易费用(佣金)
        trade_fee = cal_commission_fee(self.context.commission_rate, total)

        # 账户余额扣除交易费用 + 交易金额
        self.context.blance -= total + trade_fee
        # 净资产扣除交易费用
        self.context.base_capital -= trade_fee

        self.add_portfolio(code=code, price=price, shares=shares, total=total)
        self.add_order_book(code=code, action=1, price=price, shares=shares, total=total,
                            date_time=self.context.current_date, trade_fee=trade_fee)

    def sell_value(self, code, shares):

        position = self.context.portfolio.positions[code]
        total_shares = self.context.portfolio.positions[code].shares

        if shares < 100:
            raise ValueError('percent invalid')

        if shares > total_shares:
            raise ValueError('shares invalid')

        daily_stock_data = k_data_dao.get_k_data(code=code,
                                                 start=self.context.current_date,
                                                 end=self.context.current_date,
                                                 futu_quote_ctx=self.futu_quote_ctx)

        price_in = position.price
        price_out = daily_stock_data['close'].tail(1).values[0]

        # 卖出金额
        total = shares * price_out

        # 交易费用
        trade_fee = cal_tax_fee(self.context.tax_rate, total) + cal_commission_fee(self.context.commission_rate, total)

        self.context.blance += total - trade_fee

        profit = (price_out - price_in) * shares - trade_fee
        self.context.base_capital += profit

        # 如果全部卖出, 清空portfolio对应股票
        if shares == total_shares:
            del self.context.portfolio.positions[code]
        else:
            position.shares -= shares
            total = shares * position.price
            position.total -= total
            self.context.portfolio.positions[code] = position

        # 添加卖出记录
        self.add_order_book(code=code, action=0, price=price_out, shares=shares, total=total,
                            date_time=self.context.current_date, trade_fee=trade_fee)

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
            position = Position(code, price, shares, total, self.context.current_date)
            # 记录投资组合
            self.context.portfolio.positions[code] = position

    def add_order_book(self, code, action, price, shares, total, date_time, trade_fee):

        order = Order(code=code, action=action, price=price, shares=shares, total=total, date_time=date_time, trade_fee=trade_fee)

        self.context.order_book.append(order)
