import pandas
import urllib
import os
import config
import requests
import time
import datetime
import numpy


class DataReader:

    def __init__(self):
        pass

    def get_history_data(self, *args, **kwargs):
        """
        :param args:
        :param kwargs:code, start, end, columns, csv
        :return:
        """
        code = kwargs.get("code", "0600099")
        start = kwargs.get("start", "20180101")
        end = kwargs.get("end", "20191230")
        columns = kwargs.get("columns", ["Open", "High", "Low", "Close", "Volume"])
        csv = kwargs.get("csv", "")
        if csv:
            csv_path = csv
        else:
            url = "http://quotes.money.163.com/service/chddata.html?code=%s&start=%s&end=%s" % (code, start, end)
            csv_path = os.path.join(config.PROJECT_DIR, "tmp", "stock_csv", code + '.csv')
            urllib.request.urlretrieve(url, csv_path)

        df = pandas.read_csv(csv_path, encoding="GBK")
        df = df.rename(columns={"日期": "Date", "股票代码": "Code", "名称": "Name", "收盘价": "Close", "最高价": "High", "最低价": "Low",
                                "开盘价": "Open", "涨跌额": "Limit", "换手率": "Turnover", "成交量": "Volume", "成交金额": "Amount",
                                "总市值": "Total_value", "流通市值": "Circulation", "成交笔数": "Number"})

        df["Date"] = df["Date"].map(lambda x: self.string2datetime64(x))  # change to datetime64 to match backtrader
        df = df.set_index("Date")

        return df[columns].sort_index()

    def get_stock_list(self):
        pass

    @staticmethod
    def string2datetime64(date_string):
        """
        :param date_string: y-m-d
        :return:
        """
        t = time.strptime(date_string, "%Y-%m-%d")
        y, m, d = t[0:3]
        return numpy.datetime64(datetime.datetime(y, m, d))
