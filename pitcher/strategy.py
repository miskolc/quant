import futuquant as ft

from common_tools.trade_fee_utlis import cal_commission_fee, cal_tax_fee
from config import default_config
from dao.basic.stock_basic_dao import stock_basic_dao
from dao.k_data import fill_market
from dao.k_data.k_data_dao import k_data_dao
from pitcher.domain.order import Order
from pitcher.domain.position import Position
from pitcher.domain.profit import Profit
from common_tools.datetime_utils import get_next_date


class Strategy:
    def init(self, context):
        self.context = context
        self.futu_quote_ctx = ft.OpenQuoteContext(host=default_config.FUTU_OPEND_HOST,
                                                  port=default_config.FUTU_OPEND_PORT)

    '''
    def before_trade(self):
        # 获取code pool的所有的k_data
        self.k_data_dict = k_data_dao.get_multiple_history_kline(code_list=self.context.pool,
                                                            start=get_next_date(days=-60, args=self.context.start),
                                                            end=get_next_date(days=60, args=self.context.end),
                                                            futu_quote_ctx=self.futu_quote_ctx)


        self.basic_data = stock_basic_dao.get_all()
     '''

    def get_k_data(self, code, start, end):

        start = start + " 00:00:00"
        end = end + " 00:00:00"
        code = fill_market(code)
        k_data = self.k_data_dict[code]

        return k_data.loc[(start <= k_data['time_key']) & (k_data['time_key'] <= end)]

    def get_stock_basic(self, code):

        return self.basic_data.loc[self.basic_data['code'] == code]

    def before_handle_data(self):

        if len(self.context.portfolio.positions) == 0:
            # 记录当日收益
            self.context.profits.append(
                Profit(self.context.current_date, self.context.base_capital / self.context.init_capital))
            return

        p_total = 0.0
        for position in self.context.portfolio.positions:
            daily_stock_data = self.get_k_data(code=position.code,
                                                     start=self.context.current_date,
                                                     end=self.context.current_date)

            # 如果当日没有交易数据, 使用上一日的仓位数据填充
            if len(daily_stock_data.index) > 0:
                price = daily_stock_data['close'].tail(1).values[0]
                position.price = price

            total = position.price * position.shares
            p_total += total - self.cal_sell_trade_fee(total)

        # 计算净资产
        net_asset = p_total + self.context.blance
        # 记录当日收益
        self.context.profits.append(Profit(self.context.current_date, net_asset / self.context.init_capital))

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
        total = total + trade_fee

        # 如果总额加上佣金大于账户余额, 总股数减少100股, 再次计算总价格
        if total > amount:
            shares = shares - 100
            if shares <= 0:
                return
            # 交易费用(佣金)
            trade_fee = cal_commission_fee(self.context.commission_rate, total)
            total = total + trade_fee

        # 账户余额扣除交易费用 + 交易金额
        self.context.blance -= total
        # 净资产扣除交易费用
        self.context.base_capital -= trade_fee

        self.add_position(code=code, price=price, shares=shares, total=total, trade_fee=trade_fee)
        self.add_order_book(code=code, action=1, price=price, shares=shares, total=total,
                            date_time=self.context.current_date, trade_fee=trade_fee)

    # 卖出
    def sell_value(self, code, shares):

        position = self.context.portfolio.get_position(code)
        total_shares = position.shares

        if shares < 100:
            raise ValueError('percent invalid')

        if shares > total_shares:
            raise ValueError('shares invalid')

        price_in = position.price_in

        # 卖出金额
        total = shares * position.price
        # 交易费用
        trade_fee = self.cal_sell_trade_fee(total)
        total = total - trade_fee

        self.context.blance += total

        profit = (position.price - price_in) * shares - trade_fee
        self.context.base_capital += profit

        # 如果全部卖出, 清空portfolio对应股票
        if shares == total_shares:
            self.context.portfolio.delete_position(code)
        else:
            position.shares -= shares
            total = shares * position.price
            position.total -= total
            #self.context.portfolio.positions.append(position)

        # 添加卖出记录
        self.add_order_book(code=code, action=0, price=position.price, shares=shares, total=total,
                            date_time=self.context.current_date, trade_fee=trade_fee)

    def cal_sell_trade_fee(self, total):
        trade_fee = cal_tax_fee(self.context.tax_rate, total) + cal_commission_fee(self.context.commission_rate, total)
        return trade_fee

    def add_position(self, code, price, shares, total, trade_fee):

        position = self.context.portfolio.get_position(code)

        if position is not None:
            position.price += price
            position.shares += shares
            position.total += total
            position.trade_fee += trade_fee

        else:
            # 新增投资组合
            position = Position(code, price, shares, total, trade_fee, self.context.current_date)
            # 记录投资组合
            self.context.portfolio.positions.append(position)

        return position

    def add_order_book(self, code, action, price, shares, total, date_time, trade_fee):

        order = Order(code=code, action=action, price=price, shares=shares, total=total, date_time=date_time,
                      trade_fee=trade_fee)

        self.context.order_book.append(order)
