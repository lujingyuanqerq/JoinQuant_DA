from jqdatasdk import *


# 验证JQ平台的申请认证，以及每日的可调用&剩余可调用次数
def check_jq_auth():
    auth('13818320478', 'Sp920427')
    # {'total': 1000000, 'spare': 1000000} total:当日可调用次数，spare：当日剩余可调用次数
    print(get_query_count())


# 登出JQ平台的申请认证，释放连接数
def logout_jq_auth():
    logout()

# check_jq_auth()
# print(get_trade_days(start_date="2024-04-01", count=3))
# logout()
