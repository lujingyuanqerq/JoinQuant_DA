import jqdatasdk as jqd
import connectJoinQuant as conn
import calculate as ca

'''
dk002大盘因子：个股所处大盘KDJ的J线值小于0
'''

conn.check_jq_auth()
stock_code = jqd.normalize_code(['600602'])  # ['600602.XSHG']

stock_security_info = jqd.get_security_info(stock_code[0])

print(f"""
display_name:{stock_security_info.display_name},
name:{stock_security_info.name},
start_date(上市日期):{stock_security_info.start_date},
end_date(退市日期):{stock_security_info.end_date},
type:{stock_security_info.type},
parent:{stock_security_info.parent}
    """)

stock_data = jqd.get_price('000300.XSHG', end_date='2023-12-31', count=6, frequency='daily',
                           fields=['open', 'high', 'low', 'close', 'volume'])
stock_close_data = jqd.get_price(stock_code[0], end_date='2023-12-31', frequency='daily', count=1,
                                 fields=['close'])

print(ca.calculate_kdj_below_zero(data=stock_data))

conn.logout()
