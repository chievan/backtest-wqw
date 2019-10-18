import pandas as pd


class Order(object):
    """策略发给回测引擎的单个交易指令"""
    def __init__(self, timestamp, symbol, qty, is_buy, is_market_order, price=0):
        """
        单个交易指令所需的元素
        :param timestamp: 时间戳
        :param symbol: 证券标识
        :param qty: 交易数量
        :param is_buy: 交易方向
        :param is_market_order:市价单
        :param price: 交易价格
        :return:
        """
        self.timestamp = timestamp
        self.symbol = symbol
        self.qty = qty
        self.price = price
        self.is_buy = is_buy
        self.is_market_order = is_market_order
        self.is_filled = False
        self.filled_price = 0
        self.filled_timestamp = None
        self.filled_qty = 0


class Position(object):
    """账户证券持仓和现金变动情况"""
    """1、需要增加资金管理模块"""
    """2、需要增加希腊字母计算模块"""
    def __init__(self):
        """账户的基础要素"""
        self.symbol = None
        self.buys, self.sells, self.net = 0, 0, 0
        self.realized_pnl = 0
        self.unrealized_pnl = 0
        self.position_value = 0

    def event_fill(self, timestamp, is_buy, qty, price):
        if is_buy:
            self.buys += qty
        else:
            self.sells += qty

        self.net = self.buys - self.sells
        changed_value = qty * price * (-1 if is_buy else 1)
        self.position_value += changed_value  # 更新持仓市值

        if self.net == 0:
            self.realized_pnl = self.position_value  # 没有头寸，实现盈利等于持仓市值

    def update_unrealized_pnl(self, price):
        """
        更新未实现盈利
        :param price:最新价格数据
        :return:
        """
        if self.net == 0:
            self.unrealized_pnl = 0
        else:
            self.unrealized_pnl = price * self.net + self.position_value
        return self.unrealized_pnl