import pandas as pd
import numpy as np
import tushare as ts
from option_backtester.OptionTrade import *


class Strategy(object):
    """策略基类"""
    def __init__(self):
        self.event_sendorder = None
        self.option_info = self.option_information()

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

    @staticmethod
    def option_information():
        pro = ts.pro_api("3b1f5ca0766e5daa6fec01549bba207f8549ac82db7bbdb91599f499")
        df = pro.opt_basic(exchange='SSE', fields='ts_code,name,exercise_type,list_date,delist_date')
        return df

    def match_contract(self, time, price, month, is_call, is_in_the_money, gear):
        """
        在当前50ETF价格下对应的实或虚gear个档位的期权合约
        :param time: 交易时间
        :param price: 50ETF价格
        :param month: 合约月份，0-近月，1-下月，2-近季，3-远季
        :param is_call: 实虚
        :param is_in_the_money: 实虚
        :param gear: 挡位
        :return:
        """
        strike_prices = np.array([1.0 + 0.05 * i for i in range(40)] + [3.0 + 0.1 * i for i in range(20)])
        p1 = strike_prices[strike_prices <= price][-1]  # 比标的价格低的最高价
        p2 = strike_prices[strike_prices >= price][0]  # 比标的价格高的最低价
        at_the_money = [p1, p2][(abs(p1-price) >= abs(p2-price))*1]
        # 合约的月份统计
        live_options = self.option_info[(self.option_info.list_date<=time) & (self.option_info.delist_date>=time)].name.tolist()
        chose_month = sorted(list(set([int(item[11:15]) for item in live_options])))[month]
        if is_call:
            strike_price = strike_prices[list(strike_prices).index(at_the_money) - is_in_the_money * gear]
        else:
            strike_price = strike_prices[list(strike_prices).index(at_the_money) + is_in_the_money * gear]
        option_name = "华夏上证50ETF期权" + format(chose_month, '.0f') + ["认沽", "认购"][is_call] + format(strike_price, '.2f')
        return self.option_info[self.option_info.name == option_name].ts_code.tolist()[0]


class StandbyStrategy(Strategy):
    """备兑策略"""
    def __init__(self, symbol, lookback_intervals=1):
        """
        策略基础参数设定
        :param symbol: 证券标识
        :param lookback_intervals:往前追溯数据长度
        """
        Strategy.__init__(self)
        self.symbol = symbol
        self.option_symbol = None
        self.lookback_intervals = lookback_intervals
        self.prices = pd.DataFrame()
        self.option_prices = pd.DataFrame()
        self.is_long, self.is_short = False, False
        self.is_option_long, self.is_option_short = False, False

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
        if self.option_symbol in positions:
            position = positions[self.option_symbol]
            self.is_option_long = True if position.net > 0 else False
            self.is_option_short = True if position.net < 0 else False

    def event_tick(self, market_data):
        """
        模拟市场行情，行情数据作为数据输入
        :param market_data:市场行情数据
        :return:
        """
        self.store_prices(market_data)
        if len(self.prices) < self.lookback_intervals:
            return
        timestamp = market_data.get_timestamp(self.symbol)
        if timestamp == "20190506":
            self.on_buy_signal(timestamp, self.symbol, 10000)
            self.on_sell_signal(timestamp, self.option_symbol, 10000)
        if timestamp == "20190919":
            self.on_sell_signal(timestamp, self.symbol, 10000)
            self.on_buy_signal(timestamp, self.option_symbol, 10000)

    def store_prices(self, market_data):
        """
        策略需要的数据进行存储
        :param market_data: 行情数据
        :return:
        """
        timestamp = market_data.get_timestamp(self.symbol)
        self.prices.loc[timestamp, "close"] = market_data.get_close_price(self.symbol)
        self.prices.loc[timestamp, "open"] = market_data.get_open_price(self.symbol)
        self.option_symbol = self.match_contract(timestamp, self.prices.loc[timestamp, "close"], 0, True, True, 1)
        self.option_prices.loc[timestamp, "close"] = market_data.get_close_price(self.option_symbol)
        self.option_prices.loc[timestamp, "open"] = market_data.get_open_price(self.option_symbol)

    def on_buy_signal(self, timestamp, symbol, qty):
        """
        买-下单函数
        :param timestamp:时间戳
        :param symbol:证券标识
        :param qty:下单数量
        :return:
        """
        if not self.is_long:
            self.send_market_order(symbol, qty, True, timestamp)

    def on_sell_signal(self, timestamp, symbol, qty):
        """
        卖-下单函数
        :param timestamp:时间戳
        :param symbol:证券标识
        :param qty:下单数量
        :return:
        """
        if not self.is_short:
            self.send_market_order(symbol, qty, False, timestamp)


if __name__ == '__main__':
    strategy = StandbyStrategy('5100510.SH')
    print(strategy.match_contract('20190920', 2.879, 0, True, True, 1))
