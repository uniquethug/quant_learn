from data_reader.data_reader import DataReader
import pytest


@pytest.fixture(scope="module", autouse=True)
def datareader():
    return DataReader()


def test_get_history_data(datareader):
    print("\n")
    df = datareader.get_history_data()
    print(df)
    print(df.index)


def test_string2datetime64(datareader):
    print(datareader.string2datetime64("2018-01-01"))