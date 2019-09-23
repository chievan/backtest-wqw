import tushare as ts


class TickData(object):
    """存储一个数据单元"""
    def __init__(self, symbol, timestamp, last_price=0, total_volume=0):
        """
        :param symbol: 证券标识
        :param timestamp: 时间戳
        :param last_price:收盘价
        :param total_volume: 成交量
        """
        self.symbol = symbol
        self.timestamp = timestamp
        self.open_price = 0
        self.last_price = last_price
        self.total_volume = total_volume


class MarketData(object):
    """数据容器,用于存储和获取上个时间点的价格数据"""
    def __init__(self):
        self.__recent_ticks__ = dict()

    def add_last_price(self, time, symbol, price, volume):
        """
        往数据容器里面增加一条收盘记录
        :param time:时间戳
        :param symbol: 证券标识
        :param price: 价格
        :param volume: 成交量
        :return:
        """
        tick_data = TickData(symbol, time, price, volume)
        self.__recent_ticks__[symbol] = tick_data

    def add_open_price(self, time, symbol, price):
        """
        往数据容器里面增加一条开盘记录
        :param time: 时间戳
        :param symbol: 证券标识
        :param price: 价格
        :return:
        """
        tick_data = self.get_existing_tick_data(symbol, time)
        tick_data.open_price = price

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

    def get_last_price(self, symbol):
        """
        获取数据容器中的收盘数据
        :param symbol: 证券标识
        :return:
        """
        return self.__recent_ticks__[symbol].last_price

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

    def data_read(self):
        if self.source:
            pro = ts.pro_api("3b1f5ca0766e5daa6fec01549bba207f8549ac82db7bbdb91599f499")
            df = pro.daily(ts_code=self.ticker, start_date=self.start, end_date=self.end)
            df = df.set_index("trade_date")
            df = df.sort_index()
        return df

    def start_market_simulation(self):
        """开始模拟市场行情"""
        data = self.data_read()
        for time, row in data.iterrows():
            self.md.add_last_price(time, self.ticker, row["close"], row["vol"])
            self.md.add_open_price(time, self.ticker, row["open"])
            if not self.event_tick is None:  # 进行市场行情数据模拟
                self.event_tick(self.md)


if __name__ == '__main__':
    mds = MarketDataSource()
    mds.source = "tushare"
    mds.ticker = "000001.SZ"
    mds.start = "20180701"
    mds.end = "20180718"
    mds.event_tick = 1
    mds.start_market_simulation()