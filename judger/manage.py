# ae_h - 2018/7/13
from judger.back_test_judger import DailyBackTestJudger
from pitcher.kdj_st import KDJStrategy

# daily
kdj_strategy = KDJStrategy()
daily_bt = DailyBackTestJudger(start='2017-01-01', end='2018-07-01', base_capital=50000)

daily_bt.execute(kdj_strategy)


# weekly
