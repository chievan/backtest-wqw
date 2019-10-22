import pandas as pd


class Report(object):
    """对策略的已实现盈亏和未实现盈亏进行分析"""
    def __init__(self, rpnl, upnl):
        """
        初始化设置
        :param rpnl:已实现盈亏
        :param upnl: 未实现盈亏
        """
        self.rpnl, self.upnl = rpnl, upnl
        self.prices = None

    def analysis(self):
        """
        对盈亏进行分析
        :return:
        """
        print(self.rpnl.head())
        print(self.upnl.head())
        # 根据两张盈亏表格合成总持仓盈亏表
        net_value = pd.DataFrame(index=sorted(list(set(self.upnl.index.tolist() + self.rpnl.index.tolist()))),
                                 columns=self.upnl.columns)
        df_rpnl = self.rpnl.cumsum()  # 多次交易的结果求和
        for symbol in df_rpnl.columns:
            net_value[symbol] = df_rpnl[symbol]
        net_value = net_value.fillna(method="ffill")
        net_value = net_value.fillna(0)
        df_upnl = pd.DataFrame(index=net_value.index,columns=self.upnl.columns)
        for symbol in df_upnl.columns:
            df_upnl[symbol] = self.upnl[symbol]
        net_value = net_value + df_upnl.fillna(0)
        return net_value  # net_value.sum(axis=1)
