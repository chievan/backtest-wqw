import os
import tushare as ts
import pandas as pd
"""
df0 = pd.read_excel(r'E:\20191014期权温和看涨策略表现\备兑策略(现货+卖平值档当月认购).xlsx',index_col=0)
df1 = pd.read_excel(r'E:\20191014期权温和看涨策略表现\备兑策略(现货+卖虚一档当月认购).xlsx',index_col=0)
df2 = pd.read_excel(r'E:\20191014期权温和看涨策略表现\备兑策略(现货+卖虚两档当月认购).xlsx',index_col=0)
net_value0 = df0.sum(axis=1)
net_value1 = df1.sum(axis=1)
net_value2 = df2.sum(axis=1)
df0 = pd.DataFrame(index=df0.T.index)
df1 = pd.DataFrame(index=df1.T.index)
df2 = pd.DataFrame(index=df2.T.index)
move_list = ['20190103', '20190122', '20190226', '20190326', '20190423',
             '20190521', '20190625', '20190723', '20190827', '20190924']
for time in move_list:
    pro = ts.pro_api("3b1f5ca0766e5daa6fec01549bba207f8549ac82db7bbdb91599f499")
    dfm = pro.opt_daily(trade_date=time, exchange='SSE')
    dfm = dfm.set_index("ts_code")
    df0[time] = dfm['open']
    df1[time] = dfm['open']
    df2[time] = dfm['open']
    # df0 = df0.drop('510050.SH')
    # df1 = df1.drop('510050.SH')
    # df2 = df2.drop('510050.SH')
    # dff = pro.fund_daily(ts_code='510050.SH', start_date=time, end_date=time)
    # df0.loc['510050.SH', time] = dff.loc[0, 'open']
    # df1.loc['510050.SH', time] = dff.loc[0, 'open']
    # df2.loc['510050.SH', time] = dff.loc[0, 'open']

l0, l1, l2 = [], [], []
for i, d in enumerate(move_list):
    l0.append(df0.iloc[i+1][d])
    l1.append(df1.iloc[i+1][d])
    l2.append(df2.iloc[i+1][d])
c0 = (2.255 + max(l0)) * 10000
c1 = (2.255 + max(l0)) * 10000
c2 = (2.255 + max(l0)) * 10000
net_value0 = (net_value0 + c0)/c0
net_value1 = (net_value1 + c1)/c1
net_value2 = (net_value2 + c2)/c2
net_value = pd.DataFrame()
net_value['平值'] = net_value0
net_value['虚一档'] = net_value1
net_value['虚两档'] = net_value2
net_value.index = [pd.to_datetime(str(d)).date() for d in net_value.index.tolist()]
net_value.to_excel(r'E:\20191014期权温和看涨策略表现\备兑策略净值曲线.xlsx')
"""
df0 = pd.read_excel(r'E:\20191014期权温和看涨策略表现\买入认购(买平值当月认购).xlsx',index_col=0)
df1 = pd.read_excel(r'E:\20191014期权温和看涨策略表现\买入认购(买虚一档当月认购).xlsx',index_col=0)
df2 = pd.read_excel(r'E:\20191014期权温和看涨策略表现\买入认购(买虚二档当月认购).xlsx',index_col=0)
net_value0 = df0.sum(axis=1)
net_value1 = df1.sum(axis=1)
net_value2 = df2.sum(axis=1)
df0 = pd.DataFrame(index=df0.T.index)
df1 = pd.DataFrame(index=df1.T.index)
df2 = pd.DataFrame(index=df2.T.index)
move_list = ['20190103', '20190122', '20190226', '20190326', '20190423',
             '20190521', '20190625', '20190723', '20190827', '20190924']
for time in move_list:
    pro = ts.pro_api("3b1f5ca0766e5daa6fec01549bba207f8549ac82db7bbdb91599f499")
    dfm = pro.opt_daily(trade_date=time, exchange='SSE')
    dfm = dfm.set_index("ts_code")
    df0[time] = dfm['open']
    df1[time] = dfm['open']
    df2[time] = dfm['open']
    # df0 = df0.drop('510050.SH')
    # df1 = df1.drop('510050.SH')
    # df2 = df2.drop('510050.SH')
    # dff = pro.fund_daily(ts_code='510050.SH', start_date=time, end_date=time)
    # df0.loc['510050.SH', time] = dff.loc[0, 'open']
    # df1.loc['510050.SH', time] = dff.loc[0, 'open']
    # df2.loc['510050.SH', time] = dff.loc[0, 'open']

l0, l1, l2 = [], [], []
for i, d in enumerate(move_list):
    l0.append(df0.iloc[i+1][d])
    l1.append(df1.iloc[i+1][d])
    l2.append(df2.iloc[i+1][d])
c0 = (2.255 + max(l0)) * 10000
c1 = (2.255 + max(l0)) * 10000
c2 = (2.255 + max(l0)) * 10000
net_value0 = (net_value0 + c0)/c0
net_value1 = (net_value1 + c1)/c1
net_value2 = (net_value2 + c2)/c2
net_value = pd.DataFrame()
net_value['平值'] = net_value0
net_value['虚一档'] = net_value1
net_value['虚两档'] = net_value2
net_value.index = [pd.to_datetime(str(d)).date() for d in net_value.index.tolist()]
net_value.to_excel(r'E:\20191014期权温和看涨策略表现\买入认购策略净值曲线.xlsx')