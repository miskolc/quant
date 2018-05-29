# ae.h - 2018/5/20


exclude_features = ['date','code', ]
addition_features = ['open','close','low','high', ]


def adjust_features(list):

    # 补充额外的features
    list.extend(addition_features)

    # 移除不需要的features
    list = [x for x in list if x not in exclude_features]
    return list
