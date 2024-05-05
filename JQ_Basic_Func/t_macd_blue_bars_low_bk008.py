import jqdatasdk as jqd
import pandas
import connectJoinQuant as conn
import calculate as ca

'''
bk008板块因子：板块分时图当前MACD蓝柱区低点过前底
'''

pandas.set_option('display.max_columns', None)
pandas.set_option('display.max_rows', None)
conn.check_jq_auth()
stock_code = jqd.normalize_code(['600602'])  # ['600602.XSHG']
stock_industry = jqd.get_industry(stock_code, date='2023-12-29')

print(f"stock_industry:{stock_industry}")
industry_stocks = jqd.get_industry_stocks('801104', date='2023-12-29')
# TODO：根据可配置的industry获取对应的industry_stocks
print(industry_stocks)

# stock_security_info = jqd.get_security_info(stock_code[0])

# print(f"""
# display_name:{stock_security_info.display_name},
# name:{stock_security_info.name},
# start_date(上市日期):{stock_security_info.start_date},
# end_date(退市日期):{stock_security_info.end_date},
# type:{stock_security_info.type},
# parent:{stock_security_info.parent}
#     """)

stock_data = jqd.get_price('000300.XSHG', end_date='2023-12-31', count=10, frequency='daily',
                           fields=['open', 'high', 'low', 'close', 'volume'])
stock_close_data = jqd.get_price('000300.XSHG', end_date='2023-12-31', frequency='daily', count=1,
                                 fields=['close'])
macd_data = ca.calculate_macd(stock_data)

macd_new_lows = ca.find_macd_blue_bar_lows(macd_data)

print(macd_new_lows[['Histogram', 'macd_blue_bar_new_low']])
conn.logout()
