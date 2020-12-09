import pandas
import urllib
import os
import config
import requests

class DataReader:

    def __init__(self):
        pass

    def get_history_data(self, *args, **kwargs):
        code = kwargs.get("code", "0600099")
        start = kwargs.get("start", "20180101")
        end = kwargs.get("end", "20191230")
        columns = kwargs.get("columns", ["code", "close", "open", "high", "low", "volume"])

        url = "http://quotes.money.163.com/service/chddata.html?code=%s&start=%s&end=%s" % (code, start, end)
        csv_path = os.path.join(config.PROJECT_DIR, "tmp", "stock_csv", code + '.csv')
        urllib.request.urlretrieve(url, csv_path)
        df = pandas.read_csv(csv_path, encoding="GBK")
        df = df.rename(columns={"日期": "date", "股票代码": "code", "名称": "name", "收盘价": "close", "最高价": "high", "最低价": "low",
                                "开盘价": "open", "涨跌额": "limit", "换手率": "turnover", "成交量": "volume", "成交金额": "amount",
                                "总市值": "total_value", "流通市值": "circulation", "成交笔数": "number"})
        return df[columns]

    def get_stock_list(self):
        pass
