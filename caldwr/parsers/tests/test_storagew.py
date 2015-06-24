import pandas as pd
import pytest

from caldwr.parsers import storagew


@pytest.fixture(scope='module')
def url():
    return 'http://cdec.water.ca.gov/cgi-progs/reservoirs/STORAGEW'


def test_load_storagew(url):
    data = storagew.load_storagew(url)
    assert isinstance(data, pd.DataFrame)


def test_load_storagew_month_and_year(url):
    year = 2015
    month = 'May'
    data = storagew.load_storagew(url, year=year, month=month)

    assert isinstance(data, pd.DataFrame)
    assert 'year' in data
    assert data['year'].iloc[0] == year
    assert 'month' in data
    assert data['month'].iloc[0] == month
