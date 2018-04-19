# ae.h - 2018/4/19
import tushare as ts


antong_df = ts.get_hist_data('600179')

antong_df.to_csv('/Users/yw.h/Documents/antong_hist/antong_hist.csv', columns=[columns_name for columns_name in antong_df.columns])

print(antong_df)