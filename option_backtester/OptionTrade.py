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


class CashManagement(object):
    """资金管理"""
    def __init__(self, cash, date):
        """
        策略开始日期
        :param cash:策略起始资金
        :param date: 策略开始日期
        """
        self.cash = pd.DataFrame()
        self.cash.loc[date, cash] = 0  # 记录策略初始资金
        self.stock_assets = pd.DataFrame()  # 记录股票资产
        self.option_assets = pd.DataFrame()  # 记录期权资产
        self.option_margin = pd.DataFrame()  # 记录期权保证金

    @staticmethod
    def open_margin(symbol, prices, is_call, option_info):
        """
        计算开仓保证金
        :param symbol:标的证券
        :param prices: 行情数据
        :param is_call: 认购/认沽
        :param option_info: 期权合约信息
        :return:
        """
        if is_call:
            margin = (price[symbol].pre_settle + max(0.12 * prices[symbol].pre_close - max(option_info[option_info.ts_code == symbol].exercise_price.tolist()[0] - prices[symbol].open，0),
                                                      0.07 * prices[symbol].pre_close)) * 10000
        else:
            margin = 0
        return margin


    def maintain_margin(self):
        pass

# 开仓保证金最低标准
# 认购期权义务仓开仓保证金＝[合约前结算价 + Max（12 %×合约标的前收盘价 - 认购期权虚值，7 %×合约标的前收盘价）]×合约单位
# 认沽期权义务仓开仓保证金＝Min[合约前结算价 + Max（12 %×合约标的前收盘价 - 认沽期权虚值，7 %×行权价格），行权价格] ×合约单位
# 维持保证金最低标准
# 认购期权义务仓维持保证金＝[合约结算价 + Max（12 %×合约标的收盘价 - 认购期权虚值，7 %×合约标的收盘价）]×合约单位
# 认沽期权义务仓维持保证金＝Min[合约结算价 + Max（12 %×合标的收盘价 - 认沽期权虚值，7 %×行权价格），行权价格]×合约单位
    def update_fund(self, order):
        pass

    def get_cash(self):
        pass

    def get_assets(self):
        pass

class Greeks(object):
    """希腊字母计算"""
    def __init__(self):
        pass

    def delta(self):
        pass

    def gamma(self):
        pass

    def vega(self):
        pass

    def theta(self):
        pass

    def rho(self):
        pass

    def sse_risk(self):
        pass

    def broker_risk(self):
        pass
