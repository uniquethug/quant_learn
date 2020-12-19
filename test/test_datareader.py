from data_reader.data_reader import DataReader
import pytest
import config


@pytest.fixture(scope="module", autouse=True)
def datareader():
    return DataReader()


def test_get_history_data(datareader):
    print("\n")
    df = datareader.get_history_data()
    print(df.index)


def test_get_history_data_with_csv(datareader):
    print("\n")
    df = datareader.get_history_data(csv=config.PROJECT_DIR + r"\tmp\stock_csv\0600099.csv")
    print(df)


def test_string2datetime64(datareader):
    print(datareader.string2datetime64("2018-01-01"))


def test_volume_analysis(datareader):
    df = datareader.get_history_data(csv=config.PROJECT_DIR + r"\tmp\stock_csv\0600099.csv")
    print(datareader.is_volume_incr(df, "2018-05-28"))


def test_stock_list(datareader):
    datareader.get_stock_list()


def test_get_history_data_csv_by_code_list(datareader):
    code_list = datareader.get_stock_list()["Code"].to_list()
    datareader.get_history_data_csv_by_code_list(code_list=code_list, start_date="20200101", end_date="20201218")


def test_get_volume_incr_stock_list(datareader):
    code_list = datareader.get_stock_list()["Code"].to_list()
    datareader.get_volume_incr_stock_list(code_list, start_date="20200901", end_date="20201218", analyze_start_date="2020-12-01", mean_days=10)