# ae_h - 2018/6/1
from talib import abstract
import tushare as ts
import pandas as pd


# 三日形态
# 出现看跌
# 立即卖出
def cal_twoCrow_down_n_sell(data):
    twocrow_func = abstract.Function('CDL2CROWS')
    twocrow = twocrow_func(data)
    return twocrow


# 三日形态
# 出现看跌
def cal_threeCrow_down(data):
    threecrow_func = abstract.Function('CDL3BLACKCROWS')
    threecrow = threecrow_func(data)
    return threecrow


# 三日形态
# 出现看涨
def cal_threeInside_up(data):
    threeinside_func = abstract.Function('CDL3INSIDE')
    threeinside = threeinside_func(data)
    return threeinside


# 三日形态
# 出现看涨
def cal_threeOutside(data):
    threeOutside_func = abstract.Function('CDL3OUTSIDE')
    threeOutside = threeOutside_func(data)
    return threeOutside


# 三日形态
# 出现看跌
def cal_threeLineStrike_down(data):
    threeLineStrike_func = abstract.Function('CDL3LINESTRIKE')
    threeLineStrike = threeLineStrike_func(data)
    return threeLineStrike


# 三日形态
# 出现看涨, 反转跌势
def cal_threeStarInSouth_turn_n_up(data):
    threeStarInSouth_func = abstract.Function('CDL3STARSINSOUTH')
    threeStarInSouth = threeStarInSouth_func(data)
    return threeStarInSouth


# 三日形态
# 出现看涨
def cal_threeWhiteSoldier_up(data):
    threeWhiteSoldier_func = abstract.Function('CDL3WHITESOLDIERS')
    threeWhiteSoldier = threeWhiteSoldier_func(data)
    return threeWhiteSoldier


# 三日形态
# 出现预示反转
# 发生在顶部看跌
# 发生在底部看涨
def cal_abandonedBaby(data):
    abandonedBaby_func = abstract.Function('CDLABANDONEDBABY')
    abandonedBaby = abandonedBaby_func(data)
    return abandonedBaby


# 三日形态
# 仙人指路by greg
def cal_advanceBlcok_unkown(data):
    advanceBlcok_func = abstract.Function('CDLADVANCEBLOCK')
    advanceBlcok = advanceBlcok_func(data)
    return advanceBlcok


# 二日形态
# 出现看涨
def cal_beltHold_up(data):
    beltHold_func = abstract.Function('CDLBELTHOLD')
    beltHold = beltHold_func(data)
    return beltHold


# 五日形态
# 出现看涨
def cal_breakAway_up(data):
    breakAway_func = abstract.Function('CDLBREAKAWAY')
    breakAway = breakAway_func(data)
    return breakAway


# 一日形态
# 出现预示趋势持续
def cal_closingMarubozu_trend_keep(data):
    closingMarubozu_func = abstract.Function('CDLCLOSINGMARUBOZU')
    closingMarubozu = closingMarubozu_func(data)
    return closingMarubozu


# 四日形态
# 出现预示底部反转
def cal_concealingBabySwallow_turn_on_bottom(data):
    concealingBabySwallow_func = abstract.Function('CDLCONCEALBABYSWALL')
    concealingBabySwallow = concealingBabySwallow_func(data)
    return concealingBabySwallow


# 二日形态
# 看涨?
def cal_couterAttack_may_up(data):
    couterAttack_func = abstract.Function('CDLCOUNTERATTACK')
    couterAttack = couterAttack_func(data)
    return couterAttack


# 二日形态
# 出现看跌
def cal_cloudOver_down(data):
    cloudOver_func = abstract.Function('CDLDARKCLOUDCOVER')
    cloudOver = cloudOver_func(data)
    return cloudOver


# 一日形态
# 出现预示open与close基本相同
def cal_doji_same_daily_price(data):
    doji_func = abstract.Function('CDLDOJI')
    doji = doji_func(data)
    return doji


# 一日形态
# 出现预示open与close基本相同,趋势反转
def cal_dojiStar_same_daily_price_but_turn_trend(data):
    dojiStar_func = abstract.Function('CDLDOJISTAR')
    dojiStar = dojiStar_func(data)
    return dojiStar


# 一日形态
# 开盘一路走跌之后收复, open与close基本相同
def cal_dragonflyDoji_opendown_n_turn_up_to_same_daily(data):
    dragonflyDoji_func = abstract.Function('CDLDOJISTAR')
    dragonflyDoji = dragonflyDoji_func(data)
    return dragonflyDoji


# 二日形态
# 多头吞噬或空头吞噬
def cal_engulfing_unkown(data):
    engulfing_func = abstract.Function('CDLENGULFING')
    engulfing = engulfing_func(data)
    return engulfing


# 三日形态
# 顶部反转
def cal_eveningDojiStar_top_turn(data):
    eveningDojiStar_func = abstract.Function('CDLEVENINGDOJISTAR')
    eveningDojiStar = eveningDojiStar_func(data)
    return eveningDojiStar


# 三日形态
# 顶部反转
def cal_eveningStar_top_turn(data):
    eveningStar_func = abstract.Function('CDLEVENINGSTAR')
    eveningStar = eveningStar_func(data)
    return eveningStar


# 二日形态
# 向上或向下跳空, 趋势持续
def cal_gapSideWhite_jump_or_keep(data):
    eveningStar_func = abstract.Function('CDLGAPSIDESIDEWHITE')
    eveningStar = eveningStar_func(data)
    return eveningStar


# 一日形态
# 底部反转
def cal_graveStoneDoji_bottom_turn(data):
    graveStoneDoji_func = abstract.Function('CDLGRAVESTONEDOJI')
    graveStoneDoji = graveStoneDoji_func(data)
    return graveStoneDoji


# 一日形态
# 底部反转
def cal_hammer_bottom_turn(data):
    hammer_func = abstract.Function('CDLHAMMER')
    hammer = hammer_func(data)
    return hammer


# 一日形态
# 趋势反转
def cal_hangingMan_trend_turn(data):
    hangingMan_func = abstract.Function('CDLHANGINGMAN')
    hangingMan = hangingMan_func(data)
    return hangingMan


# 二日形态
# 反转看涨
def cal_harami_turn_up(data):
    harami_func = abstract.Function('CDLHARAMI')
    harami = harami_func(data)
    return harami


# 二日形态
# 趋势反转
def cal_haramiCross_trend_turn(data):
    haramiCross_func = abstract.Function('CDLHARAMICROSS')
    haramiCross = haramiCross_func(data)
    return haramiCross


# 三日形态
# 趋势反转
def cal_highWave_trend_turn(data):
    highWave_func = abstract.Function('CDLHIGHWAVE')
    highWave = highWave_func(data)
    return highWave


# 三日形态
# 反转失败,趋势继续
def cal_hikkake_trend_failed_trend_keep(data):
    hikkake_func = abstract.Function('CDLHIKKAKE')
    hikkake = hikkake_func(data)
    return hikkake


# 三日形态
# 反转失败,趋势继续
def cal_hikkakeMod_trend_failed_trend_keep(data):
    hikkakeMod_func = abstract.Function('CDLHIKKAKEMOD')
    hikkakeMod = hikkakeMod_func(data)
    return hikkakeMod


# 二日形态
# 趋势反转
def cal_homePigeon_trend_turn(data):
    homePigeon_func = abstract.Function('CDLHOMINGPIGEON')
    homePigeon = homePigeon_func(data)
    return homePigeon


# 三日形态
# 看跌
def cal_identicalThreeCrow_down(data):
    identicalThreeCrow_func = abstract.Function('CDLIDENTICAL3CROWS')
    identicalThreeCrow = identicalThreeCrow_func(data)
    return identicalThreeCrow


# 二日形态
# 看持续跌
def cal_inNeck_going_down(data):
    inNeck_func = abstract.Function('CDLINNECK')
    inNeck = inNeck_func(data)
    return inNeck


# 一日形态
# 趋势
def cal_invertedHammer_trend_turn(data):
    invertedHammer_func = abstract.Function('CDLINVERTEDHAMMER')
    invertedHammer = invertedHammer_func(data)
    return invertedHammer


# 五日形态
# 底部反转
def cal_ladderBottom_bottom_turn(data):
    ladderBottom_func = abstract.Function('CDLLADDERBOTTOM')
    ladderBottom = ladderBottom_func(data)
    return ladderBottom


# 二日形态
# 底部确认, 该价格为支撑位
def cal_matchingLow_bottom_confirm_supoort_price(data):
    matchingLow_func = abstract.Function('CDLMATCHINGLOW')
    matchingLow = matchingLow_func(data)
    return matchingLow


# 五日形态
# 趋势持续
def cal_matchHold_trend_keep(data):
    matchHold_func = abstract.Function('CDLMATHOLD')
    matchHold = matchHold_func(data)
    return matchHold


# 三日形态
# 底部反转
def cal_morningDojiStar_bottom_turn(data):
    morningDojiStar_func = abstract.Function('CDLMORNINGDOJISTAR')
    morningDojiStar = morningDojiStar_func(data)
    return morningDojiStar


# 三日形态
# 底部反转
def cal_morningStar_bottom_turn(data):
    morningStar_func = abstract.Function('CDLMORNINGSTAR')
    morningStar = morningStar_func(data)
    return morningStar


# 五日形态
# 看涨
def cal_rfThreeMethod_up(data):
    rfThreeMethod_func = abstract.Function('CDLMORNINGSTAR')
    rfThreeMethod = rfThreeMethod_func(data)
    return rfThreeMethod


# 一日形态
# 看跌
def cal_shootingStar_down(data):
    shootingStar_func = abstract.Function('CDLSHOOTINGSTAR')
    shootingStar = shootingStar_func(data)
    return shootingStar


# 三日形态
# 上涨结束
def cal_stalled_up_end(data):
    stalled_func = abstract.Function('CDLSTALLEDPATTERN')
    stalled = stalled_func(data)
    return stalled


# 三日形态
# 持续上升
def cal_tasukiGap_going_up(data):
    tasukiGap_func = abstract.Function('CDLTASUKIGAP')
    tasukiGap = tasukiGap_func(data)
    return tasukiGap


# 五日形态
# 看涨
def cal_udgThreeMethod_up(data):
    udgThreeMethod_func = abstract.Function('CDLXSIDEGAP3METHODS')
    udgThreeMethod = udgThreeMethod_func(data)
    return udgThreeMethod
