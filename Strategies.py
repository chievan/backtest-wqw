import pandas as pd
from Trade import *


class Strategy(object):
    """策略基类"""
    def __init__(self):
        self.event_sendorder = None

    def event_tick(self, market_data):
        """
        事件触发函数
        :param market_data:市场行情数据
        :return:
        """
        pass

    def event_order(self, order):
        """
        交易指令触发函数
        :param order: 交易指令对象
        :return:
        """
        pass

    def event_position(self, position):
        """
        持仓更新函数
        :param position:持仓对象
        :return:
        """
        pass

    def send_market_order(self, symbol, qty, is_buy, timestamp):
        """
        市价单报送
        :param symbol:证券标识
        :param qty: 交易数量
        :param is_buy: 交易方向
        :param timestamp: 交易时间戳
        :return:
        """
        if not self.event_sendorder is None:
            order = Order(timestamp, symbol, qty, is_buy, True)
            self.event_sendorder(order)


class MeanRevertingStrategy(Strategy):
    """均值反转策略"""
    def __init__(self, symbol, lookback_intervals=20, buy_threshold=-1.5, sell_threshold=1.5):
        """
        策略基础参数设定
        :param symbol: 证券标识
        :param lookback_intervals:往前追溯日期
        :param buy_threshold: 买入阈值
        :param sell_threshold: 卖出阈值
        """
        Strategy.__init__(self)
        self.symbol = symbol
        self.lookback_intervals = lookback_intervals
        self.buy_threshold = buy_threshold
        self.sell_threshold = sell_threshold
        self.prices = pd.DataFrame()
        self.is_long, self.is_short = False, False

    def event_position(self, positions):
        """
        持仓更新函数
        :param positions:持仓情况
        :return:
        """
        if self.symbol in positions:
            position = positions[self.symbol]
            self.is_long = True if position.net > 0 else False
            self.is_short = True if position.net <0 else False

    def event_tick(self, market_data):
        """
        模拟市场行情
        :param market_data:市场行情数据
        :return:
        """
        self.store_prices(market_data)
        if len(self.prices) < self.lookback_intervals:
            return
        signal_value = self.calculate_z_score()
        timestamp = market_data.get_timestamp(self.symbol)

        if signal_value < self.buy_threshold:
            self.on_buy_signal(timestamp)
        elif signal_value > self.sell_threshold:
            self.on_sell_signal(timestamp)

    def store_prices(self, market_data):
        """
        策略需要的数据进行存储
        :param market_data: 行情数据
        :return:
        """
        timestamp = market_data.get_timestamp(self.symbol)
        self.prices.loc[timestamp, "close"] = market_data.get_last_price(self.symbol)
        self.prices.loc[timestamp, "open"] = market_data.get_open_price(self.symbol)

    def calculate_z_score(self):
        self.prices = self.prices[-self.lookback_intervals:]
        returns = self.prices["close"].pct_change().dropna()
        z_score = ((returns-returns.mean())/returns.std())[-1]
        return z_score

    def on_buy_signal(self, timestamp):
        """
        买-下单函数
        :param timestamp:时间戳
        :return:
        """
        if not self.is_long:
            self.send_market_order(self.symbol, 100, True, timestamp)

    def on_sell_signal(self, timestamp):
        """
        卖-下单函数
        :param timestamp:时间戳
        :return:
        """
        if not self.is_short:
            self.send_market_order(self.symbol, 100, False, timestamp)