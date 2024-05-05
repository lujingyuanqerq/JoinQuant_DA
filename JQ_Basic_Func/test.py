import jqdatasdk as jqd
import JQ_Basic_Func.connectJoinQuant as conn
import calculate as ca
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from mpl_finance import candlestick_ohlc
import pandas as pd

'''
gk003个股因子:个股KDJ的J线值在MACD同一段蓝柱区间第二次小于0
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

data = jqd.get_price(stock_code[0], end_date='2023-12-31', count=30, frequency='daily',
                     fields=['open', 'high', 'low', 'close', 'volume'])

stock_close_data = jqd.get_price('000300.XSHG', start_date='2023-12-29', end_date='2023-12-31', frequency='1m',
                                 fields=['close'])
print(stock_close_data)
df = stock_close_data['close']
ma10 = stock_close_data.rolling(10).mean()
ma10.plot()
plt.show()

conn.logout()
