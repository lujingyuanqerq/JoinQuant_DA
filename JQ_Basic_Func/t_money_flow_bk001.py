import jqdatasdk as jqd
import pandas

import connectJoinQuant as conn
import calculate as ca

'''
gk001个股因子：个股资金流出状态，正值开始变小或者负值开始变大
'''

pandas.set_option('display.max_columns', None)
pandas.set_option('display.max_rows', None)
conn.check_jq_auth()
stock_code = jqd.normalize_code(['600602'])  # ['600602.XSHG']
# print(f"dict1:{dict1}")

df = jqd.get_money_flow_pro(security_list='000001.XSHG', start_date='2023-12-01', end_date='2023-12-29',
                            frequency='1d',
                            fields=['inflow_xl', 'inflow_l', 'inflow_m', 'inflow_s', 'outflow_xl', 'outflow_l',
                                    'outflow_m', 'outflow_s', 'netflow_xl', 'netflow_l', 'netflow_m', 'netflow_s'])

# 应用函数到不同类型的资金流向
results = {}
money_flow_types = ['net_amount_xl', 'net_amount_l', 'net_amount_m', 'net_amount_s']
for flow_type in money_flow_types:
    pos_smaller, neg_larger = ca.analyze_money_flow_changes(df, flow_type)
    results[flow_type] = {
        'positive_to_smaller': pos_smaller,
        'negative_to_larger': neg_larger
    }

# 输出分析结果
for flow_type, data in results.items():
    print(f"对于 {flow_type} 类型资金流向:")
    print("正值变小的情况:")
    print(data['positive_to_smaller'])
    print("\n负值变大的情况:")
    print(data['negative_to_larger'])
    print("\n" + "-" * 50 + "\n")
