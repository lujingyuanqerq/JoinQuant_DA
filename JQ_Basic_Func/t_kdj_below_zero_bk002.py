import jqdatasdk as jqd
import connectJoinQuant as conn
import calculate as ca

'''
bk002板块因子：个股主营业务所处板块KDJ的J线值小于0
'''

conn.check_jq_auth()
stock_code = jqd.normalize_code(['600602'])  # ['600602.XSHG']
industry_info = jqd.get_industry(stock_code, date='2023-12-31')
print(industry_info)
# TODO:一个股票丛属多个行业怎么办？
stock_lst = jqd.get_industry_stocks('801750', date='2023-12-31')
kdj_dfs = []
for stock in stock_lst:
    df = jqd.get_price(stock, start_date='2023-12-25', end_date='2023-12-31', frequency='daily', fields=['close', 'low', 'high'])
    kdj_df = ca.calculate_kdj(df)
    kdj_dfs.append(kdj_df)

print(kdj_dfs)



conn.logout()
