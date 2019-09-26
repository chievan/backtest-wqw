import tushare as ts


class TickData(object):
    """存储一个数据单元"""
    def __init__(self,
                 symbol,
                 timestamp,
                 pre_settle=0,
                 pre_close=0,
                 open_price=0,
                 high_price=0,
                 low_price=0,
                 close_price=0,
                 settle_price=0,
                 volume=0,
                 amount=0,
                 oi=0):
        """
        单个期权合约行情的数据
        :param symbol: 期权代码
        :param timestamp: 时间错
        :param pre_settle: 昨日结算价
        :param pre_close: 昨日收盘价
        :param open_price: 开盘价
        :param high_price: 最高价
        :param low_price: 最低价
        :param close_price: 收盘价
        :param settle_price:结算价
        :param volume: 成交金额
        :param amount: 成交量
        :param oi: 持仓量
        """
        self.symbol = symbol
        self.timestamp = timestamp
        self.pre_settle = pre_settle
        self.pre_close = pre_close
        self.open_price = open_price
        self.high_price = high_price
        self.low_price = low_price
        self.close_price = close_price
        self.settle_price = settle_price
        self.volume = volume
        self.amount = amount
        self.oi = oi


class MarketData(object):
    """数据函数，用于行情数据的存储和获取过程"""
    def __init__(self):
        self.__recent_ticks__ = dict()

    def add_close_data(self,
                       symbol,
                       timestamp,
                       pre_settle,
                       pre_close,
                       open_price,
                       high_price,
                       low_price,
                       close_price,
                       settle_price,
                       volume,
                       amount,
                       oi):
        """
        往数据容器里面增加一条收盘记录
        :param symbol: 期权代码
        :param timestamp: 时间错
        :param pre_settle: 昨日结算价
        :param pre_close: 昨日收盘价
        :param open_price: 开盘价
        :param high_price: 最高价
        :param low_price: 最低价
        :param close_price: 收盘价
        :param settle_price:结算价
        :param volume: 成交金额
        :param amount: 成交量
        :param oi: 持仓量
        :return:
        """
        tick_data = TickData(symbol,
                             timestamp,
                             pre_settle,
                             pre_close,
                             open_price,
                             high_price,
                             low_price,
                             close_price,
                             settle_price,
                             volume,
                             amount,
                             oi)
        self.__recent_ticks__[symbol] = tick_data

    def get_existing_tick_data(self, symbol, time):
        """
        向前获取价格数据
        :param symbol: 证券标识
        :param time: 时间戳
        :return:
        """
        if not symbol in self.__recent_ticks__:
            tick_data = TickData(symbol, time)
            self.__recent_ticks__[symbol] = tick_data
        return self.__recent_ticks__[symbol]

    def get_close_price(self, symbol):
        """
        获取数据容器中的收盘数据
        :param symbol: 证券标识
        :return:
        """
        return self.__recent_ticks__[symbol].close_price

    def get_open_price(self, symbol):
        """
        获取数据容器中的开盘数据
        :param symbol: 证券标识
        :return:
        """
        return self.__recent_ticks__[symbol].open_price

    def get_timestamp(self, symbol):
        """
        获取数据容器中的时间戳
        :param symbol: 证券标识
        :return:
        """
        return self.__recent_ticks__[symbol].timestamp


class MarketDataSource(object):
    """下载数据资源"""
    def __init__(self):
        self.event_tick = None
        self.ticker, self.source = None, None
        self.start, self.end = None, None
        self.md = MarketData()

    def data_read_option(self, time):
        """
        获取莫一交易日期权行情数据
        :param time: 交易日期
        :return:
        """
        if self.source:
            import tushare as ts
            pro = ts.pro_api("3b1f5ca0766e5daa6fec01549bba207f8549ac82db7bbdb91599f499")
            df = pro.opt_daily(trade_date=time, exchange='SSE')
            df = df.set_index("ts_code")
        return df

    def data_read_50etf(self):
        """
        获取所有交易日50ETF行情数据
        :return:
        """
        if self.source:
            pro = ts.pro_api("3b1f5ca0766e5daa6fec01549bba207f8549ac82db7bbdb91599f499")
            df = pro.fund_daily(ts_code=self.ticker, start_date=self.start, end_date=self.end)
            df = df.set_index("trade_date")
            df = df.sort_index()
        return df

    def start_market_simulation(self):
        """开始模拟市场行情"""
        data = self.data_read_50etf()
        for time, row in data.iterrows():
            self.md.add_close_data(self.ticker,
                                   time,
                                   0,
                                   row['pre_close'],
                                   row['open'],
                                   row['high'],
                                   row['low'],
                                   row['close'],
                                   0,
                                   row['vol'],
                                   row['amount'],
                                   0)
            option_data = self.data_read_option(time)
            for ticker, option_row in option_data.iterrows():
                self.md.add_close_data(ticker,
                                       time,
                                       option_row['pre_settle'],
                                       option_row['pre_close'],
                                       option_row['open'],
                                       option_row['high'],
                                       option_row['low'],
                                       option_row['close'],
                                       option_row['settle'],
                                       option_row['vol'],
                                       option_row['amount'],
                                       option_row['oi'])
            if not self.event_tick is None:  # 进行市场行情数据模拟
                self.event_tick(self.md)


class DataCatcher(object):
    """用于存储所有行情用到的数据"""
    def __init__(self):
        pass


if __name__ == '__main__':
    mds = MarketDataSource()
    mds.source = "tushare"
    mds.ticker = "510050.SH"
    mds.start = "20190701"
    mds.end = "20190920"
    mds.event_tick = 1
    mds.start_market_simulation()
