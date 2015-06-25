import pandas as pd
import pytest

from caldwr.parsers import storagew


@pytest.fixture(scope='module')
def url():
    return 'http://cdec.water.ca.gov/cgi-progs/reservoirs/STORAGEW'


def test_load_storagew(url):
    data = storagew.load_storagew(url)
    assert isinstance(data, pd.DataFrame)


def test_load_storagew_month(url):
    month = 'May'
    data = storagew.load_storagew(url, month=month)

    assert isinstance(data, pd.DataFrame)
    assert 'month' in data
    assert data['month'].iloc[0] == month
