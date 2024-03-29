import datetime as dt
import pandas as pd
from option_backtester.OptionData import *
from option_backtester.OptionStrategies import *
from option_backtester.OptionTrade import *
from option_backtester.OptionReport import *


class Backtester(object):
    """回测框架主程序"""
    def __init__(self, symbol, start_date, end_date, data_source="tushre"):
        self.target_symbol = symbol
        self.data_source  = data_source
        self.start_dt = start_date
        self.end_dt = end_date
        self.strategy = None
        self.unfilled_orders = []
        self.positions = dict()
        self.current_prices = None
        self.rpnl, self.upnl = pd.DataFrame(), pd.DataFrame()
        self.report = Report(self.rpnl, self.upnl)
        self.net_value = None

    def get_timestamp(self):
        return self.current_prices.get_timestamp(self.target_symbol)

    def get_trade_date(self):
        timestamp = self.get_timestamp()
        return pd.to_datetime(timestamp).strftime("%Y-%m-%d")

    def update_filled_position(self, symbol, qty, is_buy, price, timestamp):
        """
        更新持仓
        :param symbol:证券标识
        :param qty: 交易数量
        :param is_buy: 交易方向
        :param price: 交易价格
        :param timestamp: 交易时间
        :return:
        """
        position = self.get_position(symbol)
        position.event_fill(timestamp, is_buy, qty, price)
        self.strategy.event_position(self.positions)
        # try:  # 根据交易更新已实现盈亏
        #     self.rpnl.loc[timestamp, "rpnl"] = self.rpnl.loc[timestamp, "rpnl"] + position.realized_pnl
        # except Exception:
        #     self.rpnl.loc[timestamp, "rpnl"] = position.realized_pnl
        self.rpnl.loc[timestamp, symbol] = position.realized_pnl
        print(self.get_trade_date(), "交易成功:", "Buy" if is_buy else "Sell", "数量:", qty, "标的:", symbol, "成交价:", price)

    def get_position(self, symbol):
        """
        获取标的的持仓情况
        :param symbol: 证券标识
        :return:
        """
        if symbol not in self.positions:
            position = Position()
            position.symbol = symbol
            self.positions[symbol] = position
        return self.positions[symbol]

    def evthandler_order(self, order):
        """
        收到交易指令
        :param order:交易指令
        :return:
        """
        self.unfilled_orders.append(order)
        print(self.get_trade_date(), "获得交易指令:", "Buy" if order.is_buy else "Sell", "数量:", order.qty, "标的:", order.symbol)

    def match_order_book(self, prices):
        """
        撮合成交
        :param prices:价格数据
        :return:
        """
        if len(self.unfilled_orders) > 0:
            self.unfilled_orders = [order for order in self.unfilled_orders if self.is_order_unmatched(order, prices)]

    def is_order_unmatched(self, order, prices):
        """
        未撮合订单
        :param order:交易指令
        :param prices: 价格数据
        :return:
        """
        symbol = order.symbol
        timestamp = prices.get_timestamp(symbol)
        if order.is_market_order and timestamp > order.timestamp:  # 保证第二天交易
            order.is_filled = True
            open_price = prices.get_open_price(symbol)
            order.filled_timestamp = timestamp
            order.filled_prices = open_price
            # self.strategy.account.fill_margin(self.target_symbol, order, prices, self.positions, self.strategy.option_info) ###新增
            self.update_filled_position(symbol, order.qty, order.is_buy, open_price, timestamp)
            self.strategy.event_order(order)
            return False
        return True

    def print_position_status(self, symbol, prices):
        """
        打印持仓状态
        :param symbol:证券标识
        :param prices: 价格数据
        :return:
        """
        if symbol in self.positions:
            position = self.positions[symbol]
            close_price = prices.get_close_price(symbol)
            position.update_unrealized_pnl(close_price)
            # self.upnl.loc[self.get_timestamp(), "upnl"] = position.unrealized_pnl
            self.upnl.loc[self.get_timestamp(), symbol] = position.unrealized_pnl
            print(self.get_trade_date(), position.symbol, "净头寸:", position.net, "持仓市值:", position.position_value, "未实现盈亏:", position.unrealized_pnl, "实现盈亏:", position.realized_pnl)

    def update_positions(self):
        """更新最新的持仓状态，把持仓为零的合约删除记录"""
        del_symbol_list = []
        for symbol in self.positions.keys():
            if self.positions[symbol].net == 0:
                del_symbol_list.append(symbol)
        for del_symbol in del_symbol_list:
            del self.positions[del_symbol]

    def evthandler_tick(self, prices):
        """
        处理数据
        :param prices: 行情数据
        :return:
        """
        self.current_prices = prices
        self.strategy.store_prices(prices)
        self.match_order_book(prices)
        self.strategy.event_tick(prices)
        self.update_positions()
        for symbol in self.positions.keys():
            self.print_position_status(symbol, prices)

    def start_backtest(self):
        # self.strategy = NecklineStrategy(self.target_symbol)  # 领口策略
        self.strategy = BullSpreadStrategy(self.target_symbol)  # 牛市价差
        # self.strategy = StandbyStrategy(self.target_symbol, self.start_dt)  # 备兑策略
        # self.strategy =LongCall(self.target_symbol, self.start_dt)  # 买入看涨策略
        self.strategy.event_sendorder = self.evthandler_order

        mds = MarketDataSource()
        mds.event_tick = self.evthandler_tick
        mds.ticker = self.target_symbol
        mds.source = self.data_source
        mds.start, mds.end = self.start_dt, self.end_dt
        print("回测开始")
        mds.start_market_simulation()
        print("回测完成")
        print("进行策略分析")
        self.net_value = self.report.analysis()  # 返回策略的浮动盈亏情况
        print("策略分析完毕")


if __name__ == '__main__':
    from option_backtester.OptionStrategies import *
    """需要修改结算的过程，按照平均价结算"""
    backtester = Backtester("510050.SH", "20190101", "20191021")
    backtester.start_backtest()
    backtester.net_value.to_excel(r'E:\\公众号运营\\20191014期权温和看涨策略表现\\牛市价差(买平值当月认购+卖虚2档同月认购).xlsx')
    backtester.net_value.sum(axis=1).plot()

    # import DataAPI
    # all_data = pd.DataFrame()
    # # 获取50ETF行情
    # df1 = DataAPI.MktFunddGet(secID=u"",ticker=u"510050",tradeDate=u"",beginDate=u"20190101", endDate=u"20191021",field=["tradeDate","closePrice"],pandas="1")
    # df1 = df1.set_index("tradeDate")
    # date_list = df1.index.tolist()
    # for date in date_list:
    #     df = DataAPI.MktOptdGet(secID=u"", optID=u"", ticker=u"", tradeDate=date, beginDate=u"", endDate=u"",
    #                             field=["secID","tradeDate", "turnoverVol", "openInt"], pandas="1")
    #     df2 = df.sum(axis=0)
    #     print(date)
    #     df1.loc[date, '成交量'] = df2.turnoverVol
    #     df1.loc[date, '持仓量'] = df2.openInt
    #     df1.to_excel(r'E:\\公众号运营\\20191014期权温和看涨策略表现\\hold_trade.xlsx')
