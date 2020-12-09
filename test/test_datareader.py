from data_reader.data_reader import DataReader
import pytest


@pytest.fixture(scope="module", autouse=True)
def datareader():
    return DataReader()


def test_get_history_data(datareader):
    print("\n")
    print(datareader.get_history_data())