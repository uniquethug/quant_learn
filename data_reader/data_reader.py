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
        :param kwargs:
            code: ss->prefix code:0, szs->prefix code:1
            start: yyyymmdd
            end:  yyyymmdd
            columns: []
            csv: csv
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
        """
        :return:ss_df, szs_df
        """
        ss_df = pandas.read_csv(os.path.join(os.path.dirname(__file__), "sse.csv"), encoding="GBK").rename(columns={"公司代码 ": "Code", "公司简称 ": "Name"})[["Code", "Name"]]
        #szs = pandas.read_csv(os.path.join(os.path.dirname(__file__), "szse.csv"), encoding="GBK").rename(columns={"公司代码": "Code", "公司简称": "Name"})["Code", "Name"]
        return ss_df

    @staticmethod
    def string2datetime64(date_string):
        """
        :param date_string: yyyy-mm-dd
        :return:
        """
        t = time.strptime(date_string, "%Y-%m-%d")
        y, m, d = t[0:3]
        return numpy.datetime64(datetime.datetime(y, m, d))

    def is_volume_incr(self, datas, start_date, mean_days=10):
        start_date = self.string2datetime64(start_date)
        mean_volume = datas[:start_date].sort_index(ascending=False).head(mean_days)["Volume"].mean()
        volume_incr_flag = 0
        for index, row in datas[start_date::].iterrows():
            if row["Volume"] / mean_volume <= 1:
                volume_incr_flag = 0
            elif row["Volume"] / mean_volume > 1:
                volume_incr_flag += 1

            if volume_incr_flag > 3:
                return True
        return False
    
    def get_volume_incr_stock_list(self, code_list, start_date, end_date, analyze_start_date, mean_days):
        for code in code_list:
            code = str(code)
            if code[0] == "6":
                code = "0" + code
            else:
                code = "1" +code
            if self.is_volume_incr(self.get_history_data(code=code, start=start_date, end=end_date), analyze_start_date, mean_days=mean_days):
                print(code)
    
    def get_history_data_csv_by_code_list(self, code_list, start_date, end_date):
        """
        :param code_list: code list
        :param start_date: yyyymmdd
        :param end_date: yyyymmdd
        :return:
        """
        for code in code_list:
            code = str(code)
            if code[0] == "6":
                code = "0" + code
            else:
                code = "1" +code
            self.get_history_data(code=code, start=start_date, end=end_date)