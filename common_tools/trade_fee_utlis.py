
# 计算交易佣金
def cal_commission_fee(rate, total):

    min_amount = rate * 10000

    fee = total * rate

    if fee < min_amount:
        return min_amount

    return fee

# 计算印花税
def cal_tax_fee(rate, total):

    return total * rate
