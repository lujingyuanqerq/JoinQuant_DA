import pandas as pd
import numpy as np
import jqdatasdk as jqd
import connectJoinQuant as conn


def calculate_kdj(data, period=9, k_smooth=3, d_smooth=3):
    """
    计算KDJ指标

    data: 包含'high', 'low', 'close'列的DataFrame，代表股票的历史价格数据。
    period: 计算RSV的周期，默认为9。
    k_smooth: K值的平滑参数，默认为3。
    d_smooth: D值的平滑参数，默认为3。
    return 包含k,d,j指标的Dataframe
    """
    # data['high'] = data['high'].astype(float)
    # data['low'] = data['low'].astype(float)
    # data['close'] = data['close'].astype(float)
    # print(f"high:{data['high']} ; low:{data['low']} ; close:{data['close']}")

    # 计算RSV（未成熟随机值）
    low_min = data['low'].rolling(window=period).min()
    high_max = data['high'].rolling(window=period).max()
    # data['RSV'] = (data['close'] - low_min) / (high_max - low_min) * 100

    # 初始化K、D列
    prev_k = 50  # 初始值可以根据实际情况调整
    prev_d = 50  # 初始值可以根据实际情况调整

    # 计算K、D指标
    for i in range(1, len(data)):
        current_rsv = (data.loc[data.index[i], 'close'] - low_min.loc[data.index[i]]) / (
                high_max.loc[data.index[i]] - low_min.loc[data.index[i]]) * 100 if not np.isnan(
            low_min.loc[data.index[i]]) else np.nan
        if not np.isnan(current_rsv):  # 如果RSV不是NaN，进行K和D的计算
            current_k = (prev_k * (k_smooth - 1) + current_rsv) / k_smooth
            current_d = (prev_d * (d_smooth - 1) + current_k) / d_smooth
        else:
            current_k = prev_k
            current_d = prev_d

            # 更新DataFrame和前一日的值
        data.loc[data.index[i], 'K'] = current_k
        data.loc[data.index[i], 'D'] = current_d
        data.loc[data.index[i], 'J'] = 3 * current_k - 2 * current_d

        prev_k = current_k
        prev_d = current_d

    return data


def calculate_kdj_below_zero(data, period=9, k_smooth=3, d_smooth=3):
    """
    计算KDJ指标小于0。

    参数:
    data: 包含'high', 'low', 'close'列的DataFrame，代表股票的历史价格数据。
    period: 计算RSV的周期，默认为9。
    k_smooth: K值的平滑参数，默认为3。
    d_smooth: D值的平滑参数，默认为3。
    return kdj的j值<0的dataframe
    """
    # data['high'] = data['high'].astype(float)
    # data['low'] = data['low'].astype(float)
    # data['close'] = data['close'].astype(float)
    # print(f"high:{data['high']} ; low:{data['low']} ; close:{data['close']}")

    # 计算RSV（未成熟随机值）
    low_min = data['low'].rolling(window=period).min()
    high_max = data['high'].rolling(window=period).max()
    # data['RSV'] = (data['close'] - low_min) / (high_max - low_min) * 100

    # 初始化K、D列
    prev_k = 50  # 初始值可以根据实际情况调整
    prev_d = 50  # 初始值可以根据实际情况调整

    # 计算K、D指标
    for i in range(1, len(data)):
        current_rsv = (data.loc[data.index[i], 'close'] - low_min.loc[data.index[i]]) / (
                high_max.loc[data.index[i]] - low_min.loc[data.index[i]]) * 100 if not np.isnan(
            low_min.loc[data.index[i]]) else np.nan
        if not np.isnan(current_rsv):  # 如果RSV不是NaN，进行K和D的计算
            current_k = (prev_k * (k_smooth - 1) + current_rsv) / k_smooth
            current_d = (prev_d * (d_smooth - 1) + current_k) / d_smooth
        else:
            current_k = prev_k
            current_d = prev_d

            # 更新DataFrame和前一日的值
        data.loc[data.index[i], 'K'] = current_k
        data.loc[data.index[i], 'D'] = current_d
        data.loc[data.index[i], 'J'] = 3 * current_k - 2 * current_d

        prev_k = current_k
        prev_d = current_d

    # 计算J
    kdj_below_zero = data[data['J'] < 0]

    return kdj_below_zero


def calculate_macd(data, short_window=12, long_window=26, signal_window=9):
    """
    计算macd指标
    data: 包含'close'列的DataFrame，代表股票的历史价格数据。
    short_window：快速EMA
    long_window：慢速EMA
    signal_window：信号线市场
    return 包含MACD线、信号线、MACD柱状图的Dataframe
    """
    # 计算短期和长期的指数移动平均
    short_ema = data['close'].ewm(span=short_window, adjust=False).mean()
    long_ema = data['close'].ewm(span=long_window, adjust=False).mean()

    # 计算MACD线和信号线
    data['MACD'] = short_ema - long_ema
    data['Signal_Line'] = data['MACD'].ewm(span=signal_window, adjust=False).mean()

    # 计算MACD柱状图
    data['Histogram'] = data['MACD'] - data['Signal_Line']

    return data


def identify_macd_blue_zones(data):
    """
    识别MACD蓝柱区域
    调用此方法前需要先计算MACD相关的几个指标（MACD线、信号线、柱状图）
    data：包含MACD线、信号线、柱状图）列的DataFrame，代表股票的历史价格数据。
    return 包含每个蓝柱区间起始和结束索引的列表
    """
    # 首先确保数据中已有MACD相关列，如果没有则先计算
    if 'MACD' not in data.columns or 'Signal_Line' not in data.columns or 'Histogram' not in data.columns:
        data = calculate_macd(data)

    # 标记蓝柱区间的开始和结束
    data['Blue_Zone'] = (data['Histogram'] > 0)

    # 寻找蓝柱区间的起始点和结束点
    blue_zones = []
    in_blue_zone = False
    for i in range(1, len(data)):
        if data['Blue_Zone'][i] and not in_blue_zone:
            start = data.index[i]
            in_blue_zone = True
        elif not data['Blue_Zone'][i] and in_blue_zone:
            end = data.index[i - 1]
            blue_zones.append((start, end))
            in_blue_zone = False
    # 处理最后一个区间（如果在蓝柱区间内结束）
    if in_blue_zone:
        blue_zones.append((start, data.index[-1]))

    return blue_zones


def find_j_below_zero_during_macd_blue(data):
    """
    MACD蓝柱区间内J线第二次小于0
    遍历数据集，跟踪MACD蓝柱的开始和结束，同时记录每个蓝柱区间内J线值小于0的次数

    data：需要经过macd和kdj计算的dataframe
    return：蓝柱区间内J线第二次下跌至0以下的数据点
    """
    # 假设data已包含计算好的'macd_histogram', 'K', 'D', 'J'列
    data['macd_blue'] = data['Histogram'] > 0  # 标记MACD蓝柱区间
    data['j_below_zero'] = data['J'] < 0  # 标记J线小于0

    # 初始化辅助列
    data['blue_zone'] = 0  # MACD蓝柱区间ID
    data['j_below_zero_count'] = 0  # 记录J线小于0的次数

    blue_zone_id = 0
    for i in range(1, len(data)):
        if data.loc[data.index[i], 'macd_blue']:
            if not data.loc[data.index[i - 1], 'macd_blue']:
                blue_zone_id += 1  # 新的MACD蓝柱区间
            data.loc[data.index[i], 'blue_zone'] = blue_zone_id

            if data.loc[data.index[i], 'j_below_zero']:
                # 累计J线小于0的次数
                data.loc[data.index[i], 'j_below_zero_count'] = data.loc[data.index[i - 1], 'j_below_zero_count'] + 1
        else:
            data.loc[data.index[i], 'j_below_zero_count'] = 0  # 重置计数器
    # 筛选出MACD蓝柱区间内J线第二次小于0的情况
    second_j_below_zero_during_blue = data[(data['j_below_zero_count'] == 2) & (data['macd_blue'])]

    return second_j_below_zero_during_blue


def analyze_money_flow_changes(data, column):
    """
    计算资金流出状态，正值开始变小或者负值开始变大
    data：包含以下内容的Dataframe
        change_pct	涨跌幅(%)
        net_amount_main	主力净额(万)	主力净额 = 超大单净额 + 大单净额
        net_pct_main	主力净占比(%)	主力净占比 = 主力净额 / 成交额
        net_amount_xl	超大单净额(万)	超大单：大于等于50万股或者100万元的成交单
        net_pct_xl	超大单净占比(%)	超大单净占比 = 超大单净额 / 成交额
        net_amount_l	大单净额(万)	大单：大于等于10万股或者20万元且小于50万股或者100万元的成交单
        net_pct_l	大单净占比(%)	大单净占比 = 大单净额 / 成交额
        net_amount_m	中单净额(万)	中单：大于等于2万股或者4万元且小于10万股或者20万元的成交单
        net_pct_m	中单净占比(%)	中单净占比 = 中单净额 / 成交额
        net_amount_s	小单净额(万)	小单：小于2万股或者4万元的成交单
        net_pct_s	小单净占比(%)	小单净占比 = 小单净额 / 成交额
    column：入参枚举类型为，分别对应不同类型资金'net_amount_xl', 'net_amount_l', 'net_amount_m', 'net_amount_s'

    return 资金流向的正值开始变小或负值开始变大的Dataframe
    """
    # 计算每种资金流向的变化
    data['net_amount_xl_change'] = data['net_amount_xl'].diff()
    data['net_amount_l_change'] = data['net_amount_l'].diff()
    data['net_amount_m_change'] = data['net_amount_m'].diff()
    data['net_amount_s_change'] = data['net_amount_s'].diff()

    # 正值变小
    positive_to_smaller = data[(data[column] > 0) & (data[f'{column}_change'] < 0)]
    # 负值变大
    negative_to_larger = data[(data[column] < 0) & (data[f'{column}_change'] > 0)]

    return positive_to_smaller, negative_to_larger


def find_macd_blue_zones_within_600_seconds(df):
    """
    个股MACD蓝柱区600秒内
    调用此方法前需要先计算MACD相关的几个指标（MACD线、信号线、柱状图）
    df：包含MACD相关的几个指标（MACD线、信号线、柱状图）的dataframe
    return 600秒内是否全是蓝柱的dataframe
    """

    # df需要是每分钟的数据，600秒为最近10个数据点
    window_size = 10

    # 标记MACD蓝柱区间
    df['macd_blue'] = df['Histogram'] > 0

    # 初始化一个列表来存储蓝柱区间
    blue_zones_within_600 = []

    for i in range(window_size - 1, len(df)):
        # 检查最近600秒内是否全是蓝柱
        if df.iloc[i - window_size + 1:i + 1]['macd_blue'].all():
            blue_zones_within_600.append(df.index[i])

    return blue_zones_within_600


def find_break_box(df, window_size):
    """
    分析股价是否跌破箱体底部。

    :param df: 包含价格数据的DataFrame
    :param window_size: 箱体计算的窗口大小，以分钟为单位
    :return: 包含跌破箱体时刻的DataFrame
    """
    # 计算每个窗口的最低价格作为箱体底部
    df['rolling_min'] = df['low'].rolling(window=window_size, min_periods=1).min()

    # 标记跌破箱体底部的时刻
    df['break_box'] = df['low'] < df['rolling_min'].shift(1)  # 使用shift(1)以避免当前价格参与箱体底部的计算

    # 返回跌破箱体的时刻
    break_box_df = df[df['break_box']]

    return break_box_df


def find_macd_blue_bar_lows(df):
    """
    识别当前MACD蓝柱区低点低于前低的时刻。
    df：包含代表MACD柱状图值的'Histogram'列。
    """
    df['macd_histogram_positive'] = df['Histogram'] > 0
    df['macd_low'] = np.where(df['macd_histogram_positive'], df['Histogram'], np.nan)
    df['rolling_macd_low'] = df['macd_low'].rolling(min_periods=1, window=len(df), center=False).min()
    df['prev_rolling_macd_low'] = df['rolling_macd_low'].shift(1)
    df['macd_blue_bar_new_low'] = np.where(
        (df['macd_histogram_positive']) &
        (df['Histogram'] < df['prev_rolling_macd_low']),
        'New Low', np.nan
    )
    return df[df['macd_blue_bar_new_low'] == 'New Low']


def find_macd_divergence(df):
    """
    MACD隔堆顶背离
    股价新高，但MACD未创新高。
    df：包含MACD相关的几个指标（MACD线、信号线、柱状图）的dataframe
    window=26代表通过比较当前价格是否高于过去26个交易日的最高价来判断是否创出新高
    """
    # 计算价格新高
    df['price_new_high'] = df['close'] > df['close'].rolling(window=26, min_periods=1).max().shift(1)

    # 计算MACD新高
    df['macd_new_high'] = df['MACD'] > df['MACD'].rolling(window=26, min_periods=1).max().shift(1)

    # 寻找背离：股价创新高，但MACD未创新高
    df['divergence'] = df['price_new_high'] & (~df['macd_new_high'])

    # 筛选出背离的记录
    divergence_df = df[df['divergence']]

    return divergence_df


# TODO 主程序里面考虑因子的组合
# TODO 数据加密
# TODO 组合信息后台传输