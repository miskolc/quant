# ae_h - 2018/7/13
from judger.back_test_judger import BackTestJudger
from pitcher.kdj_st import kdj_strategy

bt = BackTestJudger()

bt.context.start = 5

bt.execute(kdj_strategy(bt.context))







